'''
IPG laser 통신 및 좌표 데이터 수집 코드 (수정 버전)
Copyleft ⓒ Seonghun_ji, Modified by Hyub Lee
last update: 2025.04.29
Requirement package ()
'''
import socket
import configparser as conf
import time
from collections import deque
import threading
import os
import sys

class LaserCommunication:
    def __init__(self, config_path=None):
        '''Initializes the sensor and communication'''

        self.config = conf.ConfigParser()

        if config_path is None:
            base_path = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_path, "../config/IPG.ini")
            config_path = os.path.normpath(config_path)

        if not os.path.exists(config_path):
            print(f"Error: {config_path} does not exist.")
            sys.exit(1)

        self.config.read(config_path)
        self.address = {key: value for key, value in self.config.items('address')}
        self.data = {key: value for key, value in self.config.items('data')}
        print(f"address:{self.address}\ndata:{self.data}")

        self.ip = str(self.address['ip'])
        self.port = int(self.address['port'])

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        try:
            self.socket.connect((self.ip, self.port))
            self.activate = True
            print(f"Connected to IPG LASER at {self.ip}:{self.port}")
        except Exception as e:
            self.activate = False
            print(f"Failed to connect: {e}")

    def get_data(self):
        if self.activate:
            try:
                self.socket.sendall("ROP\r".encode('ascii'))    
                response = self.socket.recv(1024).decode('ascii').strip()
                outpower_str = response.split(':')[-1].strip()
                if outpower_str.lower() in ('off', 'low'):
                    outpower = 0.0
                else:
                    outpower = float(outpower_str)
            except:
                outpower = None

            try:
                self.socket.sendall("RCS\r".encode('ascii'))    
                response = self.socket.recv(1024).decode('ascii').strip()
                setpower_str = response.split(':')[-1].strip()
                setpower = float(setpower_str)
            except:
                setpower = None

            self.data['outpower'] = outpower
            self.data['setpower'] = setpower

        return self.data
    
    def close(self):
        if self.activate:
            self.activate = False
            self.socket.close()
        print("Connection closed.")

class LaserDB:
    def __init__(self, max_size=100) -> None:
        self.data_queue = deque(maxlen=max_size)
    
    def store_data(self, data):
        self.data_queue.append(data)

    def retrieve_data(self):
        if self.data_queue:
            return self.data_queue[-1]
        return print("Test Data queue is empty")

class IPG_Collector(threading.Thread):
    def __init__(self, com, db):
        threading.Thread.__init__(self)
        self.com = com
        self.db = db
        self.running = True
        self.sample_rate = 100

    def run(self):
        while self.running:
            loop_start = time.perf_counter()
            if self.com.activate:
                data = self.com.get_data()
                if data:
                    self.db.store_data(data)
            else:
                time.sleep(0.5)
            sleep_time = max(0, (1/self.sample_rate)-(time.perf_counter()-loop_start))
            time.sleep(sleep_time)
        time.sleep(0.1)
    
    def stop(self):
        self.running = False

if __name__ == '__main__':
    com = LaserCommunication()
    db = LaserDB()
    collector = IPG_Collector(com, db)
    collector.start()

    try:
        while True:
            if db.data_queue:
                data = db.retrieve_data()
                print(data)
            time.sleep(1)
    except:
        print('Error')