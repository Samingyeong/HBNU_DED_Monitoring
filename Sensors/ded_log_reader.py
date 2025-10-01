import os
import re
import time
import threading
from datetime import datetime
from collections import deque

class DEDLogReader:
    def __init__(self, ded_log_path="C:/DED/Log/Trace", max_history=1000):
        self.log_path = ded_log_path
        self.max_history = max_history
        self.process_events = deque(maxlen=max_history)
        self.last_position = 0
        self.current_log_file = None
        self.running = False
        self.monitor_thread = None
        
    def get_current_log_file(self):
        """현재 날짜의 로그 파일 경로 반환"""
        today = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.log_path, f"Trace_{today}.txt")
    
    def parse_log_line(self, line):
        """로그 라인을 파싱하여 공정 이벤트 추출"""
        try:
            # 타임스탬프와 메시지 분리
            parts = line.strip().split(', ', 2)
            if len(parts) < 3:
                return None
                
            timestamp_str = parts[0] + ', ' + parts[1]
            message = parts[2]
            
            # 공정 시작 패턴
            if "NC_CS5AXIS,IsRunning,True" in message:
                return {
                    'timestamp': timestamp_str,
                    'datetime': datetime.strptime(timestamp_str, "%Y-%m-%d, %H:%M:%S.%f"),
                    'event': 'process_start',
                    'message': message,
                    'raw_line': line.strip()
                }
            # 공정 종료 패턴
            elif "NC_CS5AXIS,IsRunning,False" in message:
                return {
                    'timestamp': timestamp_str,
                    'datetime': datetime.strptime(timestamp_str, "%Y-%m-%d, %H:%M:%S.%f"),
                    'event': 'process_end',
                    'message': message,
                    'raw_line': line.strip()
                }
            # NC 시작 패턴
            elif "IsNCStarted = true" in message:
                return {
                    'timestamp': timestamp_str,
                    'datetime': datetime.strptime(timestamp_str, "%Y-%m-%d, %H:%M:%S.%f"),
                    'event': 'nc_start',
                    'message': message,
                    'raw_line': line.strip()
                }
            # NC 종료 패턴
            elif "IsNCStarted = false" in message:
                return {
                    'timestamp': timestamp_str,
                    'datetime': datetime.strptime(timestamp_str, "%Y-%m-%d, %H:%M:%S.%f"),
                    'event': 'nc_end',
                    'message': message,
                    'raw_line': line.strip()
                }
                
        except Exception as e:
            print(f"로그 라인 파싱 오류: {e}")
            return None
            
        return None
    
    def read_new_log_lines(self):
        """새로운 로그 라인들을 읽어서 이벤트 추출"""
        current_file = self.get_current_log_file()
        
        # 파일이 변경되었으면 위치 초기화
        if current_file != self.current_log_file:
            self.current_log_file = current_file
            self.last_position = 0
            
        if not os.path.exists(current_file):
            return []
            
        try:
            with open(current_file, 'r', encoding='utf-8') as f:
                # 이전 위치로 이동
                f.seek(self.last_position)
                
                new_lines = f.readlines()
                self.last_position = f.tell()
                
                events = []
                for line in new_lines:
                    event = self.parse_log_line(line)
                    if event:
                        events.append(event)
                        self.process_events.append(event)
                        
                return events
                
        except Exception as e:
            print(f"로그 파일 읽기 오류: {e}")
            return []
    
    def start_monitoring(self):
        """실시간 모니터링 시작"""
        if self.running:
            return
            
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("DED 로그 모니터링 시작")
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        print("DED 로그 모니터링 중지")
    
    def _monitor_loop(self):
        """모니터링 루프"""
        while self.running:
            try:
                events = self.read_new_log_lines()
                if events:
                    for event in events:
                        print(f"[DED Log] {event['event']}: {event['timestamp']}")
                        
                time.sleep(0.1)  # 100ms 간격으로 체크
                
            except Exception as e:
                print(f"모니터링 루프 오류: {e}")
                time.sleep(1)
    
    def get_latest_event(self):
        """최신 이벤트 반환"""
        if self.process_events:
            return self.process_events[-1]
        return None
    
    def get_process_events(self, event_type=None):
        """특정 타입의 이벤트들 반환"""
        if event_type:
            return [event for event in self.process_events if event['event'] == event_type]
        return list(self.process_events)
    
    def get_current_process_status(self):
        """현재 공정 상태 반환"""
        latest = self.get_latest_event()
        if not latest:
            return 'unknown'
            
        if latest['event'] == 'process_start' or latest['event'] == 'nc_start':
            return 'running'
        elif latest['event'] == 'process_end' or latest['event'] == 'nc_end':
            return 'stopped'
        else:
            return 'unknown'

class DEDProcessLogger:
    """공정 이벤트를 CSV로 저장하는 클래스"""
    
    def __init__(self, save_dir="DB/process_logs"):
        self.save_dir = save_dir
        self.current_file = None
        self.csv_headers = ['timestamp', 'datetime', 'event', 'message', 'raw_line']
        
        # 저장 디렉토리 생성
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def get_current_csv_file(self):
        """현재 날짜의 CSV 파일 경로 반환"""
        today = datetime.now().strftime("%Y%m%d")
        return os.path.join(self.save_dir, f"process_log_{today}.csv")
    
    def save_event(self, event):
        """이벤트를 CSV 파일에 저장"""
        csv_file = self.get_current_csv_file()
        
        try:
            # 파일이 없으면 헤더와 함께 생성
            if not os.path.exists(csv_file):
                with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                    f.write(','.join(self.csv_headers) + '\n')
            
            # 이벤트 데이터를 CSV 라인으로 변환
            csv_line = [
                event['timestamp'],
                event['datetime'].strftime("%Y-%m-%d %H:%M:%S.%f"),
                event['event'],
                event['message'].replace(',', ';'),  # CSV 구분자 충돌 방지
                event['raw_line'].replace(',', ';')
            ]
            
            # 파일에 추가
            with open(csv_file, 'a', encoding='utf-8', newline='') as f:
                f.write(','.join(csv_line) + '\n')
                
        except Exception as e:
            print(f"CSV 저장 오류: {e}")
    
    def save_events_batch(self, events):
        """여러 이벤트를 일괄 저장"""
        for event in events:
            self.save_event(event)

if __name__ == "__main__":
    # 테스트 코드
    reader = DEDLogReader()
    logger = DEDProcessLogger()
    
    print("DED 로그 모니터링 테스트 시작...")
    reader.start_monitoring()
    
    try:
        while True:
            time.sleep(1)
            latest = reader.get_latest_event()
            if latest:
                print(f"최신 이벤트: {latest['event']} at {latest['timestamp']}")
                logger.save_event(latest)
    except KeyboardInterrupt:
        print("테스트 종료")
        reader.stop_monitoring()
