'''
Pyrometer 통신 및 데이터 수집 코드 (안정화 버전)
- 깨짐 방지: 버퍼 클리어 + 유효성 검사 + 재시도
'''

import configparser as conf
import time
from collections import deque
import serial
import threading
import os
import sys

class PyrometerCommunication:
    def __init__(self, config_path=None):
        '''Initializes the sensor and communication'''
        self.config = conf.ConfigParser()

        # config_path가 None이면 pyrometer_comm.py 파일 위치 기준으로 경로 설정
        if config_path is None:
            base_path = os.path.dirname(os.path.abspath(__file__))  # 이 pyrometer_comm.py 파일 위치
            config_path = os.path.join(base_path, "../config/Pyrometer.ini")
            config_path = os.path.normpath(config_path)

        # 파일 경로 확인
        if not os.path.exists(config_path):
            print(f"Error: {config_path} does not exist.")
            sys.exit(1)

        self.config.read(config_path)
        
        self.address = {key: value for key, value in self.config.items('address')}
        self.data = {key: value for key, value in self.config.items('data')}
        print(f"address:{self.address}\ndata:{self.data}")
        self.open()

    def open(self):
        self.serial = serial.Serial(
            port=self.address['port'],
            baudrate=int(self.address['baudrate']),
            parity=self.address['parity'],
            stopbits=int(self.address['stopbits']),
            bytesize=int(self.address['bytesize']),
            timeout=int(self.address['timeout'])
        )

        if self.serial.is_open:
            print(f"Serial port {self.address['port']} opened successfully.")

            self.serial.write("00bum01\r".encode('ascii'))
            initial_response = self.serial.read_until(b'\r').decode('utf-8').strip()
            
            if initial_response == 'ok':
                self.activate = True
                print("Connected to pyrometer.")
            else:
                self.activate = False
                print(f"Unexpected response: {initial_response}")

    def get_data(self):
        if self.activate:
            # 🔑 항상 버퍼 정리 (깨짐 방지)
            self.serial.reset_input_buffer()
            self.serial.write("00bup\r".encode())

            response = None
            # 🔑 최대 3번 재시도
            for _ in range(3):
                try:
                    candidate = self.serial.read_until(b'\r').decode("utf-8").strip()
                    if len(candidate) == 12 and all(c in "0123456789ABCDEFabcdef" for c in candidate):
                        response = candidate
                        break
                except Exception as e:
                    continue

            if response:
                try:
                    mpt = int(response[0:4], 16) / 10
                    c1  = int(response[4:8], 16) / 10
                    c2  = int(response[8:12], 16) / 10

                    # 정상 범위만 반영 (비정상 값은 마지막값 유지)
                    if 300 < mpt < 4000:
                        self.data['mpt'] = mpt
                    if 300 < c1 < 4000:
                        self.data['1ct'] = c1
                    if 300 < c2 < 4000:
                        self.data['2ct'] = c2
                except Exception as e:
                    print(f"[WARN] Parse error: {e}")
        return self.data
    
    def close(self):
        self.activate = False
    

class PyrometerDB:
    def __init__(self, max_size=100) -> None:
        self.data_queue = deque(maxlen=max_size)
    
    def store_data(self, data):
        self.data_queue.append(data)

    def retrieve_data(self):
        if self.data_queue:
            return self.data_queue[-1]
        return {"mpt": 0.0, "1ct": 0.0, "2ct": 0.0}


class PyrometerCollector(threading.Thread):
    def __init__(self, com, db):
        threading.Thread.__init__(self)
        self.com = com
        self.db = db
        self.running = True
        self.sample_rate = 20   # 🔑 100 → 20 Hz (안정화)

    def run(self):
        while self.running:
            loop_start = time.perf_counter()
            if self.com.activate:
                data = self.com.get_data()
                if data:
                    self.db.store_data(data)
            else:
                time.sleep(0.5)
            sleep_time = max(0, (1/self.sample_rate) - (time.perf_counter() - loop_start))
            time.sleep(sleep_time)
        time.sleep(0.1)
    
    def stop(self):
        self.running = False


if __name__ == "__main__":
    com = PyrometerCommunication()
    db = PyrometerDB()
    collector = PyrometerCollector(com, db)
    collector.start()

    try:
        while True:
            if db.data_queue:
                data = db.retrieve_data()
                print(data)
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n[EXIT] KeyboardInterrupt received. Exiting program...')
    except Exception as e:
        print(f'[ERROR] {e}')
    finally:
        collector.stop()
        collector.join()
        com.close()