"""
WebSocket 매니저 - 실시간 데이터 전송 관리
클라이언트와의 WebSocket 연결을 관리하고 실시간 데이터를 브로드캐스트
"""
import json
import asyncio
from typing import List, Dict, Any
from fastapi import WebSocket

try:
    import numpy as np
except ImportError:
    np = None


def _json_default(obj):
    """JSON 직렬화 불가 타입 처리: numpy·ndarray·bytes·datetime 등."""
    if np is not None:
        if isinstance(obj, np.ndarray):
            return None
        if isinstance(obj, (np.integer, np.int64, np.int32, np.uint8, np.uint16, np.uint32)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
    if isinstance(obj, (bytes, bytearray)):
        return None
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    try:
        return str(obj)
    except Exception:
        return None


def _sanitize_for_json(obj, _depth=0):
    """재귀적으로 payload 정제: ndarray·bytes·numpy 스칼라 제거/변환. 순환·과심도 방지."""
    if _depth > 50:
        return None
    if obj is None or obj is True or obj is False:
        return obj
    if isinstance(obj, (int, float, str)):
        return obj
    if np is not None:
        if isinstance(obj, np.ndarray):
            return None
        if isinstance(obj, (np.integer, np.int64, np.int32, np.uint8, np.uint16, np.uint32)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
    if isinstance(obj, (bytes, bytearray)):
        return None
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {str(k): _sanitize_for_json(v, _depth + 1) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize_for_json(v, _depth + 1) for v in obj]
    try:
        return str(obj)
    except Exception:
        return None


class WebSocketManager:
    """WebSocket 연결 관리 및 실시간 데이터 브로드캐스트"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_count = 0
    
    async def connect(self, websocket: WebSocket):
        """새 WebSocket 연결 수락"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_count += 1
        
        print(f"🔗 WebSocket 연결됨 (총 {self.connection_count}개)")
        
        # 연결 확인 메시지 전송
        await self.send_personal_message({
            "type": "connection",
            "message": "WebSocket 연결이 성공했습니다",
            "timestamp": self._get_timestamp()
        }, websocket)
    
    def disconnect(self, websocket: WebSocket):
        """WebSocket 연결 해제"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            self.connection_count -= 1
            print(f"🔌 WebSocket 연결 해제됨 (총 {self.connection_count}개)")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """특정 클라이언트에게 메시지 전송"""
        try:
            await websocket.send_text(json.dumps(message, ensure_ascii=False))
        except Exception as e:
            print(f"⚠️ 개별 메시지 전송 오류: {e}")
            self.disconnect(websocket)
    
    async def broadcast_data(self, sensor_data: Dict[str, Any]):
        """모든 연결된 클라이언트에게 센서 데이터 브로드캐스트"""
        if not self.active_connections:
            return

        try:
            # 재귀 정제: ndarray·bytes·numpy 스칼라 제거. 실패 시 원본으로 직렬화 시도.
            try:
                data_clean = _sanitize_for_json(sensor_data)
            except Exception as e:
                print(f"⚠️ _sanitize_for_json 오류: {type(e).__name__}: {e}")
                data_clean = sensor_data
            message = {
                "type": "sensor_data",
                "data": data_clean,
                "timestamp": self._get_timestamp(),
                "connection_count": self.connection_count
            }
            message_json = json.dumps(message, ensure_ascii=False, default=_json_default)

            disconnected_connections = []
            # 스냅샷으로 순회 (순회 중 disconnect로 리스트 변경 시 RuntimeError 방지)
            for connection in list(self.active_connections):
                try:
                    await connection.send_text(message_json)
                except Exception as e:
                    print(f"⚠️ 브로드캐스트 전송 오류: {type(e).__name__}: {e}")
                    disconnected_connections.append(connection)

            for connection in disconnected_connections:
                self.disconnect(connection)

        except Exception as e:
            print(f"❌ 브로드캐스트 오류: {type(e).__name__}: {e}")
    
    async def broadcast_status(self, status_data: Dict[str, Any]):
        """시스템 상태 정보 브로드캐스트"""
        if not self.active_connections:
            return
        
        try:
            message = {
                "type": "status_update",
                "data": status_data,
                "timestamp": self._get_timestamp()
            }
            
            message_json = json.dumps(message, ensure_ascii=False, default=_json_default)
            
            disconnected_connections = []
            
            for connection in self.active_connections:
                try:
                    await connection.send_text(message_json)
                except Exception as e:
                    print(f"⚠️ 상태 브로드캐스트 전송 오류: {e}")
                    disconnected_connections.append(connection)
            
            for connection in disconnected_connections:
                self.disconnect(connection)
                
        except Exception as e:
            print(f"❌ 상태 브로드캐스트 오류: {e}")
    
    async def broadcast_save_status(self, save_status: Dict[str, Any]):
        """저장 상태 정보 브로드캐스트"""
        if not self.active_connections:
            return
        
        try:
            message = {
                "type": "save_status",
                "data": save_status,
                "timestamp": self._get_timestamp()
            }
            
            message_json = json.dumps(message, ensure_ascii=False, default=_json_default)
            
            disconnected_connections = []
            
            for connection in self.active_connections:
                try:
                    await connection.send_text(message_json)
                except Exception as e:
                    print(f"⚠️ 저장 상태 브로드캐스트 전송 오류: {e}")
                    disconnected_connections.append(connection)
            
            for connection in disconnected_connections:
                self.disconnect(connection)
                
        except Exception as e:
            print(f"❌ 저장 상태 브로드캐스트 오류: {e}")
    
    def _get_timestamp(self) -> str:
        """현재 시간을 ISO 형식으로 반환"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_connection_info(self) -> Dict[str, Any]:
        """연결 정보 조회"""
        return {
            "active_connections": self.connection_count,
            "connections": [
                {
                    "id": id(conn),
                    "client": str(conn.client) if hasattr(conn, 'client') else "unknown"
                }
                for conn in self.active_connections
            ]
        }
    
    async def ping_all_connections(self):
        """모든 연결에 핑 메시지 전송 (연결 상태 확인)"""
        if not self.active_connections:
            return
        
        try:
            ping_message = {
                "type": "ping",
                "timestamp": self._get_timestamp()
            }
            
            message_json = json.dumps(ping_message, ensure_ascii=False)
            
            disconnected_connections = []
            
            for connection in self.active_connections:
                try:
                    await connection.send_text(message_json)
                except Exception as e:
                    print(f"⚠️ 핑 전송 오류: {e}")
                    disconnected_connections.append(connection)
            
            for connection in disconnected_connections:
                self.disconnect(connection)
                
        except Exception as e:
            print(f"❌ 핑 브로드캐스트 오류: {e}")
    
    async def send_error_message(self, error_message: str):
        """에러 메시지를 모든 클라이언트에게 전송"""
        if not self.active_connections:
            return
        
        try:
            message = {
                "type": "error",
                "message": error_message,
                "timestamp": self._get_timestamp()
            }
            
            message_json = json.dumps(message, ensure_ascii=False)
            
            disconnected_connections = []
            
            for connection in self.active_connections:
                try:
                    await connection.send_text(message_json)
                except Exception as e:
                    print(f"⚠️ 에러 메시지 전송 오류: {e}")
                    disconnected_connections.append(connection)
            
            for connection in disconnected_connections:
                self.disconnect(connection)
                
        except Exception as e:
            print(f"❌ 에러 메시지 브로드캐스트 오류: {e}")
