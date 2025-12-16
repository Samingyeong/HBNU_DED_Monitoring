'''
HXAPI 통신 및 좌표 데이터 수집 코드 (JSON 출력 리팩토링 버전)
Copyleft ⒲ Seonghun_ji, Modified by Hyub Lee
last update: 2025.04.29
Requirement package (HXApi)
'''
import configparser as conf
import time
from collections import deque
import threading
import ctypes
import os
import sys
import json

# DLL 경로 설정
base_path = os.path.abspath(os.path.dirname(__file__))
dll_path = os.path.join(base_path, "HXApi", "dll")
os.environ['PATH'] = dll_path + os.pathsep + os.environ['PATH']

class CNCCommunication:
    def __init__(self, config_path=None) -> None:
        self.config = conf.ConfigParser()
        files_read = self.config.read(config_path)
        print(f"[디버그] 읽은 파일 리스트: {files_read}")

        try:
            self.address = {key: value for key, value in self.config.items('address')}
        except conf.NoSectionError:
            print(f"INI 파일에 [address] 섹션이 없습니다: {config_path}")
            raise Exception("INI 파일에 [address] 섹션이 없습니다")

        try:
            self.hx = ctypes.CDLL(os.path.join(dll_path, "HXApi.dll"))
        except OSError as e:
            print(f"DLL 로드 실패: {e}")
            raise Exception(f"DLL 로드 실패: {e}")

        self.api_types()
        self.open()

    def api_types(self):
        self.HX_ETHERNET = 0
        self.HXRTX       = 1

        self.hx.HxInitialize2.argtypes = [ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
        self.hx.HxInitialize2.restype = ctypes.c_bool

        self.hx.HxConnect.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.hx.HxConnect.restype = ctypes.c_bool

        self.hx.HxGetConnectState.argtypes = [ctypes.c_int32]
        self.hx.HxGetConnectState.restype = ctypes.c_bool

        self.hx.HxGetSVF.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self.hx.HxGetSVF.restype = ctypes.c_double

        self.hx.HxGetSNF.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self.hx.HxGetSNF.restype = ctypes.c_double

        # R 레지스터 읽기 함수 (피더 RPM, 가스 유량용)
        self.hx.HxGetRW.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self.hx.HxGetRW.restype = ctypes.c_int32

        self.hx.HxGetRB.argtypes = [ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
        self.hx.HxGetRB.restype = ctypes.c_bool

    def open(self):
        ip = self.address['ip'].split('.')
        port = int(self.address['port'])
        print(f"[CNC] HxInitialize2 호출 중... IP: {'.'.join(ip)}, Port: {port}")
        res = self.hx.HxInitialize2(0, int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3]), port)
        print(f"[CNC] HxInitialize2 결과: {res}")
        if res:
            self.activate = True
            print(f"[OK] CNC API 초기화 및 연결 성공 - activate=True")
        else:
            self.activate = False
            print("[ERROR] CNC HXApi 연결 실패 - activate=False")

    def get_pos_data(self):
        if not self.activate:
            return None

        pos_data = {
            'curpos_x': self.hx.HxGetSVF(0, 83),
            'curpos_y': self.hx.HxGetSVF(0, 84),
            'curpos_z': self.hx.HxGetSVF(0, 85),
            'curpos_a': self.hx.HxGetSVF(0, 86),
            'curpos_c': self.hx.HxGetSVF(0, 87),
            'macpos_x': self.hx.HxGetSNF(0, 237),
            'macpos_y': self.hx.HxGetSNF(0, 238),
            'macpos_z': self.hx.HxGetSNF(0, 239),
            'macpos_a': self.hx.HxGetSNF(0, 240),
            'macpos_c': self.hx.HxGetSNF(0, 241),
            'rempos_x': self.hx.HxGetSNF(0, 247),
            'rempos_y': self.hx.HxGetSNF(0, 248),
            'rempos_z': self.hx.HxGetSNF(0, 249),
            'rempos_a': self.hx.HxGetSNF(0, 250),
            'rempos_c': self.hx.HxGetSNF(0, 251),
            'oper_time': self.hx.HxGetSNF(0, 0),
            'total_oper_time': self.hx.HxGetSNF(0, 1),
            'feed_override': self.hx.HxGetSVF(0, 675),
            'rapid_override': self.hx.HxGetSVF(0, 676),
            'feed_rate': self.hx.HxGetSVF(0, 722),
            # 피더 RPM 데이터 (R 레지스터 - 일반적인 DED 시스템 맵핑)
            # 참고: C:\DED\Recipe\Default.rcp에서 피더 1~6 설정 확인됨
            # 레지스터 번호는 일반적인 범위로 설정 (R100~R200)
            'feeder1_rpm': self.hx.HxGetRW(0, 100),  # R100: Feeder1 RPM
            'feeder1_remaining': self.hx.HxGetRW(0, 110),  # R110: Feeder1 잔량
            'feeder1_status': bool(self.hx.HxGetRB(0, 120, 0)),  # R120.0: Feeder1 상태
            'feeder2_rpm': self.hx.HxGetRW(0, 101),  # R101: Feeder2 RPM
            'feeder2_remaining': self.hx.HxGetRW(0, 111),  # R111: Feeder2 잔량
            'feeder2_status': bool(self.hx.HxGetRB(0, 120, 1)),  # R120.1: Feeder2 상태
            'feeder3_rpm': self.hx.HxGetRW(0, 102),  # R102: Feeder3 RPM
            'feeder3_remaining': self.hx.HxGetRW(0, 112),  # R112: Feeder3 잔량
            'feeder3_status': bool(self.hx.HxGetRB(0, 120, 2)),  # R120.2: Feeder3 상태
            # 가스 유량 데이터 (R 레지스터)
            'coaxial_gas': self.hx.HxGetRW(0, 130),  # R130: Coaxial Gas
            'feeding_gas': self.hx.HxGetRW(0, 131),  # R131: Feeding Gas
            'shield_gas': self.hx.HxGetRW(0, 132),  # R132: Shield Gas
        }
        return pos_data

    def close(self):
        self.activate = False

class CNC_DB:
    def __init__(self, max_size=100) -> None:
        self.data_queue = deque(maxlen=max_size)

    def store_data(self, data):
        self.data_queue.append(data)

    def retrieve_data(self):
        if self.data_queue:
            return self.data_queue[-1]
        return None  # 큐가 비어있으면 None 반환 (정상 동작)

class CNC_Collector(threading.Thread):
    def __init__(self, com, db, sample_rate=100):
        threading.Thread.__init__(self)
        self.com = com
        self.db = db
        self.running = True
        self.sample_rate = sample_rate

    def run(self):
        while self.running:
            loop_start = time.perf_counter()
            if self.com.activate:
                data = self.com.get_pos_data()
                if data:
                    self.db.store_data(data)
            else:
                time.sleep(0.5)
            sleep_time = max(0, (1/self.sample_rate)-(time.perf_counter()-loop_start))
            time.sleep(sleep_time)

    def stop(self):
        self.running = False

if __name__ == "__main__":
    # 프로젝트 루트 기준으로 경로 설정
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, "config", "HXApi.ini")
    
    # 설정 파일이 없으면 기본 경로 시도
    if not os.path.exists(config_path):
        # 상대 경로로 시도
        config_path = os.path.join("config", "HXApi.ini")
        if not os.path.exists(config_path):
            print(f"❌ 설정 파일을 찾을 수 없습니다: {config_path}")
            sys.exit(1)
    
    print(f"📁 설정 파일 경로: {config_path}")
    
    try:
        com = CNCCommunication(config_path=config_path)
        db = CNC_DB()
        collector = CNC_Collector(com, db)
        collector.start()
        
        print("✅ CNC 데이터 수집 시작 (JSON 출력)")

        while True:
            if db.data_queue:
                data = db.retrieve_data()
                if data:
                    print(json.dumps(data, ensure_ascii=False), flush=True)
            time.sleep(0.03)
    except KeyboardInterrupt:
        print('\n종료 요청 감지')
        collector.stop()
    except Exception as e:
        print(f'Error: {e}')
        if 'collector' in locals():
            collector.stop()
