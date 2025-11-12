"""
CNC Subprocess Manager - 32비트 Python 호환성을 위한 별도 프로세스 실행
HBU_monitoring 방식과 동일하게 subprocess로 CNC 통신을 분리
"""
import subprocess
import json
import threading
import os
import sys
from typing import Dict, Optional, Any


class CNCSubprocessManager:
    """CNC 통신을 별도 프로세스로 실행하고 JSON 데이터를 수신"""
    
    def __init__(self, python_executable: str = None, config_path: str = None):
        """
        Args:
            python_executable: 32비트 Python 실행 파일 경로 (예: "C:/Python36-32/python.exe")
            config_path: HXApi.ini 설정 파일 경로
        """
        self.python_executable = python_executable
        self.config_path = config_path
        self.cnc_process: Optional[subprocess.Popen] = None
        self.cnc_thread: Optional[threading.Thread] = None
        self.cnc_data: Dict[str, Any] = {}
        self.cnc_thread_running = False
        
        # 기본 경로 설정
        if not self.config_path:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.config_path = os.path.join(base_path, "config", "HXApi.ini")
        
        if not self.python_executable:
            # 32비트 Python 자동 검색
            self.python_executable = self._find_32bit_python()
    
    def _find_32bit_python(self) -> Optional[str]:
        """32비트 Python 실행 파일 자동 검색"""
        # 일반적인 32비트 Python 설치 경로들
        common_paths = [
            r"C:\Python36-32\python.exe",
            r"C:\Python37-32\python.exe",
            r"C:\Python38-32\python.exe",
            r"C:\Python39-32\python.exe",
            r"C:\Python310-32\python.exe",
            r"C:\Users\{}\AppData\Local\Programs\Python\Python36-32\python.exe".format(os.getenv('USERNAME', 'user')),
            r"C:\Users\{}\AppData\Local\Programs\Python\Python37-32\python.exe".format(os.getenv('USERNAME', 'user')),
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        # 현재 Python이 32비트인지 확인
        import platform
        if platform.architecture()[0] == '32bit':
            return sys.executable
        
        return None
    
    def start(self):
        """CNC subprocess 시작"""
        if self.cnc_process:
            print("⚠️ CNC 프로세스가 이미 실행 중입니다")
            return
        
        if not self.python_executable:
            raise Exception("32비트 Python 실행 파일을 찾을 수 없습니다. python_executable을 명시적으로 지정하세요.")
        
        if not os.path.exists(self.python_executable):
            raise Exception(f"Python 실행 파일이 존재하지 않습니다: {self.python_executable}")
        
        # cnc_comm.py 경로
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "Sensors", "cnc_comm.py"
        )
        
        if not os.path.exists(script_path):
            raise Exception(f"CNC 스크립트가 존재하지 않습니다: {script_path}")
        
        try:
            print(f"🚀 CNC subprocess 시작: {self.python_executable} {script_path}")
            
            # subprocess 시작
            self.cnc_process = subprocess.Popen(
                [self.python_executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='cp949',
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            
            # JSON 데이터 수신 스레드 시작
            self.cnc_thread_running = True
            self.cnc_thread = threading.Thread(
                target=self._cnc_data_collector,
                args=(self.cnc_process,),
                daemon=True
            )
            self.cnc_thread.start()
            
            print("✅ CNC subprocess 시작 완료")
            
        except Exception as e:
            print(f"❌ CNC subprocess 시작 실패: {e}")
            raise
    
    def _cnc_data_collector(self, pipe: subprocess.Popen):
        """subprocess의 stdout에서 JSON 데이터 읽기"""
        while self.cnc_thread_running:
            try:
                output = pipe.stdout.readline()
                if output:
                    try:
                        # JSON 파싱
                        data = json.loads(output.strip())
                        self.cnc_data = data
                    except json.JSONDecodeError as e:
                        print(f"⚠️ CNC JSON 파싱 오류: {e}, 출력: {output[:100]}")
                    except Exception as e:
                        print(f"⚠️ CNC 데이터 처리 오류: {e}")
                elif pipe.poll() is not None:
                    # 프로세스 종료됨
                    print("⚠️ CNC 프로세스가 종료되었습니다")
                    break
            except Exception as e:
                print(f"⚠️ CNC 데이터 수집 오류: {e}")
                break
    
    def get_latest_data(self) -> Optional[Dict[str, Any]]:
        """최신 CNC 데이터 반환"""
        return self.cnc_data.copy() if self.cnc_data else None
    
    def stop(self):
        """CNC subprocess 정지"""
        self.cnc_thread_running = False
        
        if self.cnc_thread:
            self.cnc_thread.join(timeout=2)
        
        if self.cnc_process:
            try:
                self.cnc_process.terminate()
                self.cnc_process.wait(timeout=5)
                print("✅ CNC subprocess 정지 완료")
            except subprocess.TimeoutExpired:
                self.cnc_process.kill()
                print("⚠️ CNC 프로세스 강제 종료")
            except Exception as e:
                print(f"⚠️ CNC 프로세스 정지 오류: {e}")
            finally:
                self.cnc_process = None
    
    def is_running(self) -> bool:
        """CNC 프로세스 실행 상태 확인"""
        if self.cnc_process:
            return self.cnc_process.poll() is None
        return False

