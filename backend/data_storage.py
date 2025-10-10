"""
데이터 스토리지 - 센서 데이터 저장 및 관리
기존 CSV 저장 로직을 백엔드로 이동
"""
import os
import csv
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import deque
import pandas as pd
import cv2
import numpy as np


class DataStorage:
    """센서 데이터 저장 및 관리 클래스"""
    
    def __init__(self, max_history_size: int = 5000):
        self.max_history_size = max_history_size
        self.data_history = deque(maxlen=max_history_size)
        
        # 저장 관련 상태
        self.is_saving = False
        self.current_save_path = None
        self.save_folder = None
        self.save_task = None
        
        # 임시 저장 관련 (자동저장 데이터 보관)
        self.temp_storage = deque(maxlen=10000)  # 최대 10,000개 데이터 보관
        self.temp_storage_start_time = None
        self.temp_storage_session_id = None
        self.temp_storage_cleanup_task = None
        
        # 이미지 저장 관련
        self.image_save_dir = None
        self.hik_save_dir = None
        self.frame_id = 0
        self.last_hik_save = 0
        
        # 데이터베이스 경로 설정
        self.base_db_path = os.path.join(os.path.dirname(__file__), "..", "DB")
        os.makedirs(self.base_db_path, exist_ok=True)
        
        # 이미지 저장 경로 설정
        self.images_path = os.path.join(os.path.dirname(__file__), "images")
        os.makedirs(self.images_path, exist_ok=True)
    
    def store_data(self, sensor_data: Dict[str, Any]):
        """센서 데이터를 히스토리에 저장"""
        try:
            # 데이터 정규화
            normalized_data = self._normalize_data(sensor_data)
            
            # 히스토리에 추가
            self.data_history.append(normalized_data)
            
            # 이미지 저장 처리
            asyncio.create_task(self._save_images_async(normalized_data))
            
            # 저장 중이면 CSV에 추가
            if self.is_saving and self.save_folder:
                asyncio.create_task(self._save_to_csv_async(normalized_data))
            
            # 임시 저장 중이면 임시 스토리지에 추가
            if self.temp_storage_session_id:
                self.temp_storage.append(normalized_data)
                
        except Exception as e:
            print(f"❌ 데이터 저장 오류: {e}")
    
    def _normalize_data(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """센서 데이터를 정규화"""
        normalized = {
            "timestamp": sensor_data.get("timestamp", ""),
            "time_elapsed": 0.0,
            "curpos_x": None,
            "curpos_y": None,
            "curpos_z": None,
            "curpos_a": None,
            "curpos_c": None,
            "mpt": None,  # melt pool temperature
            "1ct": None,  # 1-color temperature
            "2ct": None,  # 2-color temperature
            "outpower": None,
            "setpower": None,
            "melt_pool_area": None,
            "image_available": False,
            "hik_image_available": False
        }
        
        # CNC 데이터 처리
        if sensor_data.get("cnc_data"):
            cnc_data = sensor_data["cnc_data"]
            normalized.update({
                "curpos_x": cnc_data.get("curpos_x"),
                "curpos_y": cnc_data.get("curpos_y"),
                "curpos_z": cnc_data.get("curpos_z"),
                "curpos_a": cnc_data.get("curpos_a"),
                "curpos_c": cnc_data.get("curpos_c")
            })
        
        # 레이저 데이터 처리
        if sensor_data.get("laser_data"):
            laser_data = sensor_data["laser_data"]
            normalized.update({
                "outpower": laser_data.get("outpower"),
                "setpower": laser_data.get("setpower")
            })
        
        # Pyrometer 데이터 처리
        if sensor_data.get("pyrometer_data"):
            pyro_data = sensor_data["pyrometer_data"]
            normalized.update({
                "mpt": pyro_data.get("mpt"),
                "1ct": pyro_data.get("1ct"),
                "2ct": pyro_data.get("2ct")
            })
        
        # 카메라 데이터 처리
        if sensor_data.get("camera_data"):
            camera_data = sensor_data["camera_data"]
            normalized.update({
                "melt_pool_area": camera_data.get("melt_pool_area"),
                "image_available": camera_data.get("image") is not None
            })
        
        # HikRobot 카메라 데이터 처리
        if sensor_data.get("hik_camera_data"):
            hik_data = sensor_data["hik_camera_data"]
            normalized.update({
                "hik_image_available": hik_data.get("combined_image") is not None
            })
        
        return normalized
    
    async def _save_images_async(self, data: Dict[str, Any]):
        """이미지 저장 (비동기)"""
        try:
            # Basler 카메라 이미지 저장
            if (data.get("image_available") and 
                data.get("outpower", 0) > 10 and
                self.image_save_dir):
                
                # 이미지 데이터 가져오기 (실제 구현에서는 sensor_manager에서 가져와야 함)
                # 여기서는 플레이스홀더
                pass
            
            # HikRobot 이미지 저장 (1초마다)
            if (data.get("hik_image_available") and 
                (time.time() - self.last_hik_save) >= 1.0):
                
                # 이미지 저장 로직 (실제 구현에서는 sensor_manager에서 가져와야 함)
                self.last_hik_save = time.time()
                
        except Exception as e:
            print(f"⚠️ 이미지 저장 오류: {e}")
    
    async def _save_to_csv_async(self, data: Dict[str, Any]):
        """CSV 파일에 데이터 저장 (비동기)"""
        try:
            if not self.current_save_path:
                return
            
            # CSV에 저장할 데이터 준비
            csv_data = {
                "timestamp": data["timestamp"],
                "curpos_x": data["curpos_x"],
                "curpos_y": data["curpos_y"],
                "curpos_z": data["curpos_z"],
                "curpos_a": data["curpos_a"],
                "curpos_c": data["curpos_c"],
                "mpt": data["mpt"],
                "melt_pool_area": data["melt_pool_area"],
                "outpower": data["outpower"],
                "setpower": data["setpower"]
            }
            
            # CSV 파일에 추가
            file_exists = os.path.exists(self.current_save_path)
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None, self._write_csv_row, self.current_save_path, csv_data, file_exists
            )
            
        except Exception as e:
            print(f"⚠️ CSV 저장 오류: {e}")
    
    def _write_csv_row(self, filepath: str, data: Dict, file_exists: bool):
        """CSV 파일에 행 추가 (동기 함수)"""
        try:
            with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = list(data.keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(data)
        except Exception as e:
            print(f"❌ CSV 쓰기 오류: {e}")
    
    async def start_saving(self, folder_name: str) -> str:
        """데이터 저장 시작"""
        if self.is_saving:
            raise Exception("이미 저장 중입니다")
        
        try:
            # 저장 폴더 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.save_folder = os.path.join(
                self.base_db_path, 
                f"{folder_name}_{timestamp}"
            )
            os.makedirs(self.save_folder, exist_ok=True)
            
            # 이미지 저장 폴더 생성
            self.image_save_dir = os.path.join(self.save_folder, "meltpool_images")
            self.hik_save_dir = os.path.join(self.save_folder, "captures_hik")
            os.makedirs(self.image_save_dir, exist_ok=True)
            os.makedirs(self.hik_save_dir, exist_ok=True)
            
            # CSV 파일 경로 설정
            self.current_save_path = os.path.join(
                self.save_folder, 
                f"{timestamp}.csv"
            )
            
            self.is_saving = True
            self.frame_id = 0
            self.last_hik_save = 0
            
            # 1시간마다 새 CSV 파일 생성하는 태스크 시작
            self.save_task = asyncio.create_task(self._csv_rotation_task())
            
            print(f"✅ 데이터 저장 시작: {self.save_folder}")
            return self.save_folder
            
        except Exception as e:
            self.is_saving = False
            raise Exception(f"저장 시작 실패: {str(e)}")
    
    async def stop_saving(self):
        """데이터 저장 중지"""
        if not self.is_saving:
            return
        
        try:
            self.is_saving = False
            
            # CSV 로테이션 태스크 정지
            if self.save_task:
                self.save_task.cancel()
                try:
                    await self.save_task
                except asyncio.CancelledError:
                    pass
            
            self.current_save_path = None
            self.save_folder = None
            self.image_save_dir = None
            self.hik_save_dir = None
            
            print("✅ 데이터 저장 중지 완료")
            
        except Exception as e:
            raise Exception(f"저장 중지 실패: {str(e)}")
    
    async def _csv_rotation_task(self):
        """1시간마다 새 CSV 파일 생성"""
        while self.is_saving:
            try:
                # 1시간 대기
                await asyncio.sleep(3600)
                
                if self.is_saving and self.save_folder:
                    # 새 CSV 파일 생성
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    self.current_save_path = os.path.join(
                        self.save_folder, 
                        f"{timestamp}.csv"
                    )
                    print(f"📄 새 CSV 파일 생성: {self.current_save_path}")
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"⚠️ CSV 로테이션 오류: {e}")
    
    def get_latest_data(self) -> Optional[Dict[str, Any]]:
        """최신 데이터 조회"""
        if self.data_history:
            return dict(self.data_history[-1])
        return None
    
    def get_history_data(self, limit: int = 100) -> List[Dict[str, Any]]:
        """히스토리 데이터 조회"""
        if not self.data_history:
            return []
        
        # 최근 limit개 데이터 반환
        recent_data = list(self.data_history)[-limit:]
        return [dict(item) for item in recent_data]
    
    def save_camera_image(self, image: np.ndarray, power: float, area: float) -> Optional[str]:
        """Basler 카메라 이미지 저장"""
        if not self.image_save_dir or image is None:
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = os.path.join(
                self.image_save_dir,
                f"meltpool_{self.frame_id:05d}_{timestamp}.png"
            )
            cv2.imwrite(filename, image)
            self.frame_id += 1
            
            print(f"📸 Basler 이미지 저장: {filename} (Power={power:.1f}W, Area={area:.2f}mm²)")
            return filename
            
        except Exception as e:
            print(f"⚠️ Basler 이미지 저장 오류: {e}")
            return None
    
    def save_hik_image(self, combined_image: np.ndarray) -> Optional[str]:
        """HikRobot 합쳐진 이미지 저장"""
        if not self.hik_save_dir or combined_image is None:
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(
                self.hik_save_dir,
                f"hik_combined_{timestamp}.png"
            )
            cv2.imwrite(filename, combined_image)
            
            print(f"📹 HikRobot 이미지 저장: {filename}")
            return filename
            
        except Exception as e:
            print(f"⚠️ HikRobot 이미지 저장 오류: {e}")
            return None
    
    async def start_temp_storage(self, session_id: str):
        """임시 저장 시작 (자동저장 데이터 보관)"""
        try:
            self.temp_storage_session_id = session_id
            self.temp_storage_start_time = datetime.now()
            self.temp_storage.clear()  # 기존 임시 데이터 초기화
            
            # 30분 후 자동 정리 태스크 시작
            self.temp_storage_cleanup_task = asyncio.create_task(self._temp_storage_cleanup())
            
            print(f"📦 임시 저장 시작: {session_id}")
            
        except Exception as e:
            print(f"❌ 임시 저장 시작 실패: {e}")
            raise Exception(f"임시 저장 시작 실패: {str(e)}")
    
    async def stop_temp_storage(self):
        """임시 저장 중지"""
        try:
            if self.temp_storage_cleanup_task:
                self.temp_storage_cleanup_task.cancel()
                try:
                    await self.temp_storage_cleanup_task
                except asyncio.CancelledError:
                    pass
            
            self.temp_storage_session_id = None
            self.temp_storage_start_time = None
            
            print("📦 임시 저장 중지 완료")
            
        except Exception as e:
            print(f"❌ 임시 저장 중지 실패: {e}")
    
    async def save_temp_storage_to_permanent(self, folder_name: str) -> str:
        """임시 저장된 데이터를 영구 저장으로 이동"""
        if not self.temp_storage_session_id or not self.temp_storage:
            raise Exception("저장할 임시 데이터가 없습니다")
        
        try:
            # 영구 저장 폴더 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            permanent_folder = os.path.join(
                self.base_db_path, 
                f"{folder_name}_{timestamp}"
            )
            os.makedirs(permanent_folder, exist_ok=True)
            
            # CSV 파일 경로 설정
            csv_path = os.path.join(permanent_folder, f"{timestamp}.csv")
            
            # 임시 데이터를 CSV로 저장
            temp_data_list = list(self.temp_storage)
            if temp_data_list:
                # CSV 헤더 작성
                fieldnames = list(temp_data_list[0].keys())
                
                with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    # 데이터 행들 작성
                    for data in temp_data_list:
                        writer.writerow(data)
                
                print(f"✅ 임시 데이터 영구 저장 완료: {csv_path} ({len(temp_data_list)}개 데이터)")
                
                # 임시 저장 중지
                await self.stop_temp_storage()
                
                return permanent_folder
            else:
                raise Exception("저장할 데이터가 없습니다")
                
        except Exception as e:
            print(f"❌ 임시 데이터 영구 저장 실패: {e}")
            raise Exception(f"임시 데이터 영구 저장 실패: {str(e)}")
    
    async def _temp_storage_cleanup(self):
        """30분 후 임시 저장 데이터 자동 정리"""
        try:
            # 30분 대기
            await asyncio.sleep(1800)  # 30분 = 1800초
            
            if self.temp_storage_session_id:
                print(f"🧹 임시 저장 데이터 자동 정리: {self.temp_storage_session_id}")
                await self.stop_temp_storage()
                
        except asyncio.CancelledError:
            print("🧹 임시 저장 정리 태스크 취소됨")
        except Exception as e:
            print(f"❌ 임시 저장 정리 오류: {e}")
    
    def get_temp_storage_info(self) -> Dict[str, Any]:
        """임시 저장 정보 조회"""
        if not self.temp_storage_session_id:
            return {
                "has_temp_data": False,
                "session_id": None,
                "data_count": 0,
                "start_time": None,
                "remaining_time": 0
            }
        
        remaining_seconds = 0
        if self.temp_storage_start_time:
            elapsed = (datetime.now() - self.temp_storage_start_time).total_seconds()
            remaining_seconds = max(0, 1800 - elapsed)  # 30분 - 경과시간
        
        return {
            "has_temp_data": True,
            "session_id": self.temp_storage_session_id,
            "data_count": len(self.temp_storage),
            "start_time": self.temp_storage_start_time.isoformat() if self.temp_storage_start_time else None,
            "remaining_time": int(remaining_seconds)
        }
