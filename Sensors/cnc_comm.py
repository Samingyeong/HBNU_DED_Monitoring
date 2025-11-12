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

    def open(self):
        ip = self.address['ip'].split('.')
        port = int(self.address['port'])
        res = self.hx.HxInitialize2(0, int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3]), port)
        if res:
            self.activate = True
            print(f"API 초기화 및 연결 성공: {res}")
        else:
            self.activate = False
            print("HXApi 연결 실패")

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
            'feed_rate': self.hx.HxGetSVF(0, 722)
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
        print("Test Data queue is empty")
        return None

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
