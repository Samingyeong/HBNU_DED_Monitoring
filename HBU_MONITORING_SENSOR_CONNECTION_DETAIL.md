# HBU Monitoring System - 센서 연결 상세 분석

## 📋 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [폴더 구조](#폴더-구조)
3. [센서 연결 상세 분석](#센서-연결-상세-분석)
4. [데이터 수집 흐름](#데이터-수집-흐름)
5. [HBNU_Monitoring과의 차이점](#hbnU_monitoring과의-차이점)

---

## 프로젝트 개요

**HBU Monitoring System**은 PySide2 기반의 데스크톱 GUI 애플리케이션으로, DED 공정을 실시간 모니터링합니다. HBNU_Monitoring과 달리 **단일 프로세스**에서 모든 기능을 처리합니다.

### 주요 특징
- **PySide2 GUI**: Qt 기반 데스크톱 애플리케이션
- **단일 프로세스**: 모든 센서 통신이 메인 프로세스 내에서 실행
- **CNC 별도 프로세스**: CNC만 subprocess로 분리 실행 (32비트 Python 호환성)
- **Trace 로그 모니터링**: 자동저장 시작/중지 이벤트 감지
- **수동 버퍼**: 공정 데이터를 메모리에 임시 저장 후 수동 저장

---

## 폴더 구조

```
HBU_monitoring/
├── main.py                          # 메인 프로그램 (PySide2 GUI)
├── settings.py                      # 설정 파일 경로 정의
├── requirements.txt                 # Python 의존성
│
├── config/                          # 설정 파일 (INI 형식)
│   ├── Main.ini                     # 메인 설정 (저장 경로 등)
│   ├── HXApi.ini                   # CNC 설정
│   ├── IPG.ini                     # 레이저 설정
│   ├── Pyrometer.ini               # Pyrometer 설정
│   └── Camera.ini                   # 카메라 설정
│
├── Sensors/                         # 센서 통신 모듈
│   ├── cnc_comm.py                 # CNC 통신 (HXApi DLL)
│   ├── laser_comm.py               # IPG 레이저 통신 (TCP/IP)
│   ├── pyrometer_comm.py           # Pyrometer 통신 (Serial)
│   ├── camera_comm.py              # Basler 카메라 통신 (USB3.0)
│   ├── optris_client_with_fallback.py  # Optris 카메라 (선택적)
│   │
│   ├── HXApi/                      # HXApi DLL 및 헤더
│   │   ├── dll/
│   │   │   ├── HXApi.dll
│   │   │   ├── Qt5Core.dll
│   │   │   └── ...
│   │   └── include/                 # C++ 헤더 파일
│   │
│   └── previous/                    # 이전 버전 파일들
│
├── UI/                              # PySide2 UI 파일
│   ├── Template.ui                  # 메인 UI 디자인
│   ├── Template_ui.py               # UI 코드 생성
│   ├── save_path.ui                 # 저장 경로 설정 UI
│   └── ui_camera_setting.py         # 카메라 설정 UI
│
├── DB/                              # 데이터 저장 폴더
│   └── [폴더명]_[타임스탬프]/
│       └── [타임스탬프].csv
│
└── Monitoring/                      # 모니터링 데이터 (선택적)
    └── DB/
```

---

## 센서 연결 상세 분석

### 1. CNC Controller (HXApi) - 별도 프로세스 실행

#### 🔴 특이사항: Subprocess로 분리 실행

HBU_monitoring에서는 CNC 통신을 **별도 Python 프로세스**로 실행합니다. 이는 32비트/64비트 호환성 문제를 해결하기 위한 방법입니다.

#### 연결 과정

```python
# main.py - DataCollector.setup_sensors()
# 1. 별도 Python 프로세스로 cnc_comm.py 실행
self.cnc_process = subprocess.Popen(
    [CNC_PYTHON_EXECUTABLE, CNC_SCRIPT_PATH],  # Python36-32/python.exe
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding='cp949'
)

# 2. JSON 출력을 읽는 스레드 시작
self.cnc_thread = Thread(
    target=self.cnc_data_collector, 
    args=(self.cnc_process,), 
    daemon=True
)
self.cnc_thread.start()
```

#### cnc_comm.py 실행 흐름

```python
# Sensors/cnc_comm.py
if __name__ == "__main__":
    # 1. 설정 파일 읽기
    com = CNCCommunication(config_path="config/HXApi.ini")
    
    # 2. 데이터베이스 및 컬렉터 생성
    db = CNC_DB()
    collector = CNC_Collector(com, db, sample_rate=100)
    collector.start()
    
    # 3. JSON 형식으로 stdout에 출력
    while True:
        if db.data_queue:
            data = db.retrieve_data()
            print(json.dumps(data, ensure_ascii=False), flush=True)
        time.sleep(0.03)
```

#### 데이터 수집 상세

**1단계: DLL 로드 및 초기화**
```python
# Sensors/cnc_comm.py:33-40
try:
    # DLL 경로 설정
    base_path = os.path.abspath(os.path.dirname(__file__))
    dll_path = os.path.join(base_path, "HXApi", "dll")
    os.environ['PATH'] = dll_path + os.pathsep + os.environ['PATH']
    
    # HXApi.dll 로드
    self.hx = ctypes.CDLL(os.path.join(dll_path, "HXApi.dll"))
except OSError as e:
    print(f"DLL 로드 실패: {e}")
    sys.exit(1)
```

**2단계: API 함수 시그니처 정의**
```python
# Sensors/cnc_comm.py:42-59
def api_types(self):
    # 통신 타입 정의
    self.HX_ETHERNET = 0
    self.HXRTX = 1
    
    # HxInitialize2 함수 정의
    self.hx.HxInitialize2.argtypes = [
        ctypes.c_int32,  # comtype
        ctypes.c_int32,  # ip1
        ctypes.c_int32,  # ip2
        ctypes.c_int32,  # ip3
        ctypes.c_int32,  # ip4
        ctypes.c_int32   # port
    ]
    self.hx.HxInitialize2.restype = ctypes.c_bool
    
    # HxGetSVF 함수 정의 (현재 위치 읽기)
    self.hx.HxGetSVF.argtypes = [ctypes.c_int32, ctypes.c_int32]
    self.hx.HxGetSVF.restype = ctypes.c_double
    
    # HxGetSNF 함수 정의 (머신 위치 읽기)
    self.hx.HxGetSNF.argtypes = [ctypes.c_int32, ctypes.c_int32]
    self.hx.HxGetSNF.restype = ctypes.c_double
```

**3단계: CNC 컨트롤러 연결**
```python
# Sensors/cnc_comm.py:61-70
def open(self):
    # 설정 파일에서 IP/Port 읽기
    ip = self.address['ip'].split('.')  # "127.0.0.1" → ["127", "0", "0", "1"]
    port = int(self.address['port'])     # 3000
    
    # HXApi 초기화 및 연결
    res = self.hx.HxInitialize2(
        0,              # HX_ETHERNET
        int(ip[0]),     # 127
        int(ip[1]),     # 0
        int(ip[2]),     # 0
        int(ip[3]),     # 1
        port            # 3000
    )
    
    if res:
        self.activate = True
        print(f"API 초기화 및 연결 성공: {res}")
    else:
        self.activate = False
        print("HXApi 연결 실패")
```

**4단계: 위치 데이터 읽기**
```python
# Sensors/cnc_comm.py:72-98
def get_pos_data(self):
    if not self.activate:
        return None
    
    pos_data = {
        # 현재 위치 (HxGetSVF - Servo Variable Float)
        'curpos_x': self.hx.HxGetSVF(0, 83),   # 포트 0, 주소 83
        'curpos_y': self.hx.HxGetSVF(0, 84),
        'curpos_z': self.hx.HxGetSVF(0, 85),
        'curpos_a': self.hx.HxGetSVF(0, 86),
        'curpos_c': self.hx.HxGetSVF(0, 87),
        
        # 머신 위치 (HxGetSNF - Servo Number Float)
        'macpos_x': self.hx.HxGetSNF(0, 237),
        'macpos_y': self.hx.HxGetSNF(0, 238),
        'macpos_z': self.hx.HxGetSNF(0, 239),
        'macpos_a': self.hx.HxGetSNF(0, 240),
        'macpos_c': self.hx.HxGetSNF(0, 241),
        
        # 나머지 위치
        'rempos_x': self.hx.HxGetSNF(0, 247),
        'rempos_y': self.hx.HxGetSNF(0, 248),
        'rempos_z': self.hx.HxGetSNF(0, 249),
        'rempos_a': self.hx.HxGetSNF(0, 250),
        'rempos_c': self.hx.HxGetSNF(0, 251),
        
        # 운전 시간
        'oper_time': self.hx.HxGetSNF(0, 0),
        'total_oper_time': self.hx.HxGetSNF(0, 1),
        
        # 피드레이트 및 오버라이드
        'feed_override': self.hx.HxGetSVF(0, 675),
        'rapid_override': self.hx.HxGetSVF(0, 676),
        'feed_rate': self.hx.HxGetSVF(0, 722)
    }
    return pos_data
```

**5단계: Collector 스레드에서 주기적 수집**
```python
# Sensors/cnc_comm.py:116-137
class CNC_Collector(threading.Thread):
    def __init__(self, com, db, sample_rate=100):
        threading.Thread.__init__(self)
        self.com = com
        self.db = db
        self.running = True
        self.sample_rate = sample_rate  # 100Hz
    
    def run(self):
        while self.running:
            loop_start = time.perf_counter()
            
            if self.com.activate:
                # 데이터 읽기
                data = self.com.get_pos_data()
                if data:
                    # DB에 저장
                    self.db.store_data(data)
            else:
                time.sleep(0.5)  # 연결 실패 시 0.5초 대기
            
            # 정확한 샘플링 레이트 유지
            sleep_time = max(0, (1/self.sample_rate) - (time.perf_counter() - loop_start))
            time.sleep(sleep_time)
```

**6단계: JSON 출력 및 메인 프로세스 수신**
```python
# main.py:773-781
def cnc_data_collector(self, pipe):
    """subprocess의 stdout에서 JSON 데이터 읽기"""
    while self.cnc_thread_running:
        output = pipe.stdout.readline()
        if output:
            try:
                # JSON 파싱
                data = json.loads(output.strip())
                self.cnc_data = data
            except Exception as e:
                print(f"Error parsing CNC JSON data: {e}")
```

#### 설정 파일

**config/HXApi.ini**
```ini
[address]
ip = 127.0.0.1
port = 3000

[data]
curpos_X = 0
curpos_Y = 0
...
```

#### HXApi 주소 매핑

| 데이터 | 함수 | 포트 | 주소 | 설명 |
|--------|------|------|------|------|
| curpos_x | HxGetSVF | 0 | 83 | 현재 X 위치 |
| curpos_y | HxGetSVF | 0 | 84 | 현재 Y 위치 |
| curpos_z | HxGetSVF | 0 | 85 | 현재 Z 위치 |
| curpos_a | HxGetSVF | 0 | 86 | 현재 A 위치 |
| curpos_c | HxGetSVF | 0 | 87 | 현재 C 위치 |
| macpos_x | HxGetSNF | 0 | 237 | 머신 X 위치 |
| macpos_y | HxGetSNF | 0 | 238 | 머신 Y 위치 |
| macpos_z | HxGetSNF | 0 | 239 | 머신 Z 위치 |
| macpos_a | HxGetSNF | 0 | 240 | 머신 A 위치 |
| macpos_c | HxGetSNF | 0 | 241 | 머신 C 위치 |
| rempos_x | HxGetSNF | 0 | 247 | 나머지 X 위치 |
| rempos_y | HxGetSNF | 0 | 248 | 나머지 Y 위치 |
| rempos_z | HxGetSNF | 0 | 249 | 나머지 Z 위치 |
| rempos_a | HxGetSNF | 0 | 250 | 나머지 A 위치 |
| rempos_c | HxGetSNF | 0 | 251 | 나머지 C 위치 |
| oper_time | HxGetSNF | 0 | 0 | 운전 시간 |
| total_oper_time | HxGetSNF | 0 | 1 | 총 운전 시간 |
| feed_override | HxGetSVF | 0 | 675 | 피드 오버라이드 |
| rapid_override | HxGetSVF | 0 | 676 | 래피드 오버라이드 |
| feed_rate | HxGetSVF | 0 | 722 | 피드레이트 |

---

### 2. IPG Laser - TCP/IP Socket 통신

#### 연결 과정

**1단계: 설정 파일 읽기**
```python
# Sensors/laser_comm.py:16-36
def __init__(self, config_path=None):
    self.config = conf.ConfigParser()
    
    # 기본 경로 설정
    if config_path is None:
        base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_path, "../config/IPG.ini")
    
    self.config.read(config_path)
    self.address = {key: value for key, value in self.config.items('address')}
    self.data = {key: value for key, value in self.config.items('data')}
    
    # IP/Port 추출
    self.ip = str(self.address['ip'])      # "192.168.3.230"
    self.port = int(self.address['port'])  # 10001
    
    # TCP 소켓 생성
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connect()
```

**2단계: 레이저 장치 연결**
```python
# Sensors/laser_comm.py:41-48
def connect(self):
    try:
        # TCP 연결
        self.socket.connect((self.ip, self.port))
        self.activate = True
        print(f"Connected to IPG LASER at {self.ip}:{self.port}")
    except Exception as e:
        self.activate = False
        print(f"Failed to connect: {e}")
```

**3단계: 데이터 읽기 (명령-응답 방식)**
```python
# Sensors/laser_comm.py:50-74
def get_data(self):
    if self.activate:
        # 출력 파워 읽기
        try:
            # "ROP\r" 명령 전송 (Read Output Power)
            self.socket.sendall("ROP\r".encode('ascii'))
            
            # 응답 수신 (예: "ROP:450.0\r")
            response = self.socket.recv(1024).decode('ascii').strip()
            outpower_str = response.split(':')[-1].strip()
            
            # "off" 또는 "low" 처리
            if outpower_str.lower() in ('off', 'low'):
                outpower = 0.0
            else:
                outpower = float(outpower_str)
        except:
            outpower = None
        
        # 설정 파워 읽기
        try:
            # "RCS\r" 명령 전송 (Read Current Setpoint)
            self.socket.sendall("RCS\r".encode('ascii'))
            
            # 응답 수신 (예: "RCS:500.0\r")
            response = self.socket.recv(1024).decode('ascii').strip()
            setpower_str = response.split(':')[-1].strip()
            setpower = float(setpower_str)
        except:
            setpower = None
        
        self.data['outpower'] = outpower
        self.data['setpower'] = setpower
    
    return self.data
```

**4단계: Collector 스레드에서 주기적 수집**
```python
# Sensors/laser_comm.py:94-116
class IPG_Collector(threading.Thread):
    def __init__(self, com, db):
        threading.Thread.__init__(self)
        self.com = com
        self.db = db
        self.running = True
        self.sample_rate = 100  # 100Hz
    
    def run(self):
        while self.running:
            loop_start = time.perf_counter()
            
            if self.com.activate:
                data = self.com.get_data()
                if data:
                    self.db.store_data(data)
            else:
                time.sleep(0.5)  # 연결 실패 시 대기
            
            sleep_time = max(0, (1/self.sample_rate) - (time.perf_counter() - loop_start))
            time.sleep(sleep_time)
```

#### 설정 파일

**config/IPG.ini**
```ini
[address]
ip = 192.168.3.230
port = 10001

[data]
setpower = 0
outpower = 0
```

#### IPG 레이저 통신 프로토콜

| 명령 | 설명 | 응답 형식 | 예시 |
|------|------|----------|------|
| `ROP\r` | 출력 파워 읽기 | `ROP:값\r` | `ROP:450.0\r` |
| `RCS\r` | 설정 파워 읽기 | `RCS:값\r` | `RCS:500.0\r` |

**특징**:
- **ASCII 인코딩**: 모든 명령은 ASCII 문자열
- **캐리지 리턴**: 명령 끝에 `\r` 필요
- **타임아웃**: 소켓 기본 타임아웃 사용
- **에러 처리**: 예외 발생 시 `None` 반환

---

### 3. Pyrometer - Serial (RS-232) 통신

#### 연결 과정

**1단계: 시리얼 포트 설정**
```python
# Sensors/pyrometer_comm.py:39-46
def open(self):
    self.serial = serial.Serial(
        port=self.address['port'],           # "COM12"
        baudrate=int(self.address['baudrate']),  # 115200
        parity=self.address['parity'],       # "E" (Even)
        stopbits=int(self.address['stopbits']),  # 1
        bytesize=int(self.address['bytesize']),  # 8
        timeout=int(self.address['timeout'])     # 3초
    )
```

**2단계: 초기화 명령 전송**
```python
# Sensors/pyrometer_comm.py:48-60
if self.serial.is_open:
    print(f"Serial port {self.address['port']} opened successfully.")
    
    # 초기화 명령 전송
    self.serial.write("00bum01\r".encode('ascii'))
    
    # 응답 읽기 (최대 '\r'까지)
    initial_response = self.serial.read_until(b'\r').decode('utf-8').strip()
    
    # "ok" 응답 확인
    if initial_response == 'ok':
        self.activate = True
        print("Connected to pyrometer.")
    else:
        self.activate = False
        print(f"Unexpected response: {initial_response}")
```

**3단계: 온도 데이터 읽기**
```python
# Sensors/pyrometer_comm.py:62-74
def get_data(self):
    if self.activate:
        # 데이터 요청 명령 전송
        self.serial.write("00bup\r".encode())
        
        # 응답 읽기 (12자리 16진수 문자열)
        response = self.serial.read_until(b'\r').decode("utf-8").strip()
        
        # 응답 파싱 (12자리 확인)
        if len(response) == 12:
            # 2컬러 온도 (0-4): AAAA
            self.data['mpt'] = int(response[0:4], 16) / 10
            
            # 채널 1 온도 (4-8): BBBB
            self.data['1ct'] = int(response[4:8], 16) / 10
            
            # 채널 2 온도 (8-12): CCCC
            self.data['2ct'] = int(response[8:12], 16) / 10
        else:
            pass  # 잘못된 응답 무시
    
    return self.data
```

**4단계: Collector 스레드에서 주기적 수집**
```python
# Sensors/pyrometer_comm.py:91-115
class PyrometerCollector(threading.Thread):
    def __init__(self, com, db):
        threading.Thread.__init__(self)
        self.com = com
        self.db = db
        self.running = True
        self.sample_rate = 100  # 100Hz
    
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
```

#### 설정 파일

**config/Pyrometer.ini**
```ini
[address]
port = COM12
baudrate = 115200
parity = E
stopbits = 1
bytesize = 8
timeout = 3

[data]
MPT = 0
1cT = 0
2cT = 0
```

#### Pyrometer 통신 프로토콜

| 명령 | 설명 | 응답 형식 | 예시 |
|------|------|----------|------|
| `00bum01\r` | 초기화 | `ok\r` | `ok\r` |
| `00bup\r` | 온도 데이터 요청 | 12자리 16진수 | `0641A0F5B2C3\r` |

**응답 파싱**:
```
응답: "0641A0F5B2C3"
├─ 0-4:   "0641" → MPT (2컬러 온도) = 0x0641 / 10 = 160.1°C
├─ 4-8:   "A0F5" → 1CT (채널 1) = 0xA0F5 / 10 = 4117.3°C
└─ 8-12:  "B2C3" → 2CT (채널 2) = 0xB2C3 / 10 = 4576.3°C
```

**참고**: 실제 온도 범위는 300~4000°C이지만, 16진수로 인코딩되어 전송됩니다.

---

### 4. Basler Camera - USB3.0 (Pylon SDK)

#### 연결 과정

**1단계: 카메라 검색 및 연결**
```python
# Sensors/camera_comm.py:13-28
def __init__(self):
    connected = False
    
    # 최대 3회 재시도
    for i in range(3):
        try:
            # 첫 번째 연결된 Basler 카메라 검색
            self.camera = pylon.InstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice()
            )
            
            # 카메라 열기
            self.camera.Open()
            
            # 카메라 설정
            self.cam_setting()
            
            print("Camera Connected!")
            connected = True
            break
        except Exception as e:
            print(f"Connection attempt {i+1} failed. Error: {e}")
            time.sleep(1)
    
    if not connected:
        raise Exception("No device is available. Please check the camera connection.")
    
    # 연속 이미지 캡처 시작
    self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
```

**2단계: 카메라 설정**
```python
# Sensors/camera_comm.py:32-36
def cam_setting(self, expos=5000, width=720, height=520):
    # 노출 시간 설정 (마이크로초)
    self.camera.ExposureTime.SetValue(expos)  # 5000μs = 5ms
    
    # 해상도 설정
    self.camera.Width.SetValue(width)   # 720
    self.camera.Height.SetValue(height) # 520
```

**3단계: 이미지 캡처**
```python
# Sensors/camera_comm.py:38-49
def get_data(self):
    img = None
    try:
        # 이미지 가져오기 (타임아웃 1000ms)
        grab_result = self.camera.RetrieveResult(
            1000, 
            pylon.TimeoutHandling_ThrowException
        )
        
        if grab_result.GrabSucceeded():
            # numpy 배열로 변환
            img = grab_result.Array.copy()
        else:
            print("Failed to get image.")
        
        # 리소스 해제
        grab_result.Release()
    except Exception as e:
        print(f"Error during image acquisition: {e}")
    
    return img
```

**4단계: Collector 스레드에서 주기적 수집**
```python
# Sensors/camera_comm.py:74-92
class CameraCollector(threading.Thread):
    def __init__(self, camera, db, sample_rate=30):
        threading.Thread.__init__(self)
        self.camera = camera
        self.db = db
        self.running = True
        self.sample_rate = sample_rate  # 30Hz
    
    def run(self):
        while self.running:
            loop_start = time.perf_counter()
            
            # 이미지 캡처
            data = self.camera.get_data()
            if data is not None:
                # DB에 저장
                self.db.store_data(data)
            
            # 정확한 샘플링 레이트 유지
            sleep_time = max(0, (1/self.sample_rate) - (time.perf_counter() - loop_start))
            time.sleep(sleep_time)
```

#### 설정 파일

**config/Camera.ini**
```ini
[parameters]
width = 1920
height = 1080
pixel_size = 0.00835
threshold = 250
fps = 30
exposure = 50000
gain = 0.0
gamma = 1.2
black_level = 0.0
digital_shift = 0

[data]
image = 0
melt_pool_area = 0
temp = 0
```

**참고**: 실제 코드에서는 하드코딩된 값(720x520, 5000μs)을 사용하고 있습니다.

---

## 데이터 수집 흐름

### 전체 데이터 흐름도

```
┌─────────────────────────────────────────────────────────┐
│  Hardware Sensors                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │   CNC    │  │  IPG     │  │ Pyrometer│  │ Basler  ││
│  │Controller│  │  Laser   │  │  Sensor  │  │ Camera  ││
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬────┘│
└───────┼─────────────┼─────────────┼─────────────┼──────┘
        │             │             │             │
        │ TCP/IP      │ TCP/IP      │ Serial      │ USB3.0
        │             │             │             │
┌───────▼─────────────▼─────────────▼─────────────▼──────┐
│  Sensor Communication Modules (Sensors/*.py)            │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │   CNC    │  │  Laser   │  │ Pyrometer│  │ Camera  ││
│  │    Comm  │  │   Comm   │  │   Comm   │  │  Comm   ││
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬────┘│
│       │             │             │             │      │
│       ▼             ▼             ▼             ▼      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │   CNC    │  │  Laser   │  │ Pyrometer│  │ Camera  ││
│  │Collector │  │Collector │  │Collector │  │Collector││
│  │(Thread)  │  │(Thread)  │  │(Thread)  │  │(Thread) ││
│  └────┬─────┘  └────┬─────┘  └────┬──────┘  └────┬────┘│
│       │             │             │             │      │
│       ▼             ▼             ▼             ▼      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │   CNC    │  │  Laser   │  │ Pyrometer│  │ Camera  ││
│  │    DB    │  │   DB     │  │    DB    │  │   DB    ││
│  │ (deque)  │  │ (deque)  │  │ (deque)  │  │ (deque) ││
│  └────┬─────┘  └────┬─────┘  └────┬──────┘  └────┬────┘│
└───────┼─────────────┼─────────────┼─────────────┼──────┘
        │             │             │             │
        │ JSON stdout │             │             │
        │ (subprocess)│             │             │
        │             │             │             │
┌───────▼─────────────┼─────────────┼─────────────┼──────┐
│  Main Process (main.py)                                │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │  DataCollector                                  │  │
│  │  - collect_and_merge_data_list() (50Hz)        │  │
│  │  - 각 DB에서 최신 데이터 조회                   │  │
│  │  - 통합 데이터 구조 생성                        │  │
│  └──────────────┬──────────────────────────────────┘  │
│                 │                                      │
│                 ▼                                      │
│  ┌─────────────────────────────────────────────────┐  │
│  │  data_storage (dict)                            │  │
│  │  - 리스트 형태로 데이터 저장                     │  │
│  │  - 최대 5000개 유지                              │  │
│  └──────────────┬──────────────────────────────────┘  │
└─────────────────┼──────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  GUI Update (PySide2)                                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Mainwindow                                     │   │
│  │  - update_gui() (10Hz)                         │   │
│  │  - draw_graph()                                │   │
│  │  - draw_image() (100Hz)                        │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 상세 데이터 수집 단계

#### 1단계: 센서별 독립 수집 (Thread Level)

각 센서는 독립적인 Thread에서 동작:

```python
# CNC: Subprocess + Thread
cnc_process → stdout (JSON) → cnc_thread (JSON 파싱) → cnc_data

# Laser: Thread
ipg_collector (Thread) → ipg_db (deque)

# Pyrometer: Thread
pyro_collector (Thread) → pyro_db (deque)

# Camera: Thread
cam_collector (Thread) → cam_db (deque)
```

#### 2단계: 데이터 통합 (DataCollector Level)

```python
# main.py:859-923
def collect_and_merge_data_list(self):
    """50Hz로 실행되는 데이터 통합 루프"""
    self.is_running = True
    
    while self.is_running:
        loop_start_time = time.perf_counter()
        elapsed_time = round(time.perf_counter() - start_time, 3)
        current_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
        
        # 각 센서 DB에서 최신 데이터 조회
        ipg_data = {}
        pyro_data = {}
        camera_data = {}
        
        if self.testmode:
            # 테스트 모드: 랜덤 데이터 생성
            ...
        else:
            # 실측 데이터 수집
            if self.ipg_db and self.ipg_db.data_queue:
                ipg_data = self.ipg_db.retrieve_data()
            
            if self.pyro_db and self.pyro_db.data_queue:
                pyro_data = self.pyro_db.retrieve_data()
            
            if self.cam_db and self.cam_db.data_queue:
                camera_data = self.cam_db.retrieve_data()
        
        # 데이터 통합
        merged_data = {
            'time': current_time,
            '_t': elapsed_time
        }
        
        if self.cnc_data:
            merged_data.update(self.cnc_data)  # CNC는 이미 dict
        if ipg_data:
            merged_data.update(ipg_data)
        if pyro_data:
            merged_data.update(pyro_data)
        if camera_data:
            merged_data.update(camera_data)
        
        # 데이터 저장소 업데이트
        if len(merged_data) > 2:
            self.update_data_storage_list(merged_data)
        
        # 50Hz 유지
        sleep_time = max(0, (1/50) - (time.perf_counter() - loop_start_time))
        time.sleep(sleep_time)
```

#### 3단계: 데이터 저장소 업데이트

```python
# main.py:831-856
def update_data_storage_list(self, new_data):
    """새로운 데이터를 데이터 저장소에 업데이트"""
    for key, value in new_data.items():
        if key == 'time':
            self.data_storage[key].append(value)
        
        elif key == '_t':
            self.data_storage[key].append(value)
            # 최대 5000개 유지
            if len(self.data_storage['_t']) > 5000:
                self.data_storage['_t'].pop(0)
        
        elif key in self.config_data['cnc']:
            # CNC 데이터는 단일값으로 저장 (리스트 아님)
            self.data_storage[key] = value
        
        elif key == 'image':
            # 이미지는 최대 10개만 유지
            if len(self.data_storage['image']) >= 10:
                self.data_storage['image'].pop(0)
            self.data_storage['image'].append(value)
        
        else:
            # 나머지 데이터는 리스트로 저장 (최대 5000개)
            if len(self.data_storage[key]) >= 5000:
                self.data_storage[key].pop(0)
            self.data_storage[key].append(value)
```

#### 4단계: GUI 업데이트

```python
# main.py:197-247
def update_gui(self):
    """10Hz로 실행되는 GUI 업데이트"""
    # CNC 위치 데이터 표시
    self.ui.cur_x_val.setText(safe_format(self.DC.data_storage.get('curpos_x')))
    self.ui.cur_y_val.setText(safe_format(self.DC.data_storage.get('curpos_y')))
    ...
    
    # 그래프 업데이트
    self.draw_graph()

def draw_graph(self):
    """시계열 그래프 업데이트"""
    self.line_data1.setData(
        self.DC.data_storage['_t'], 
        self.DC.data_storage['mpt']
    )
    ...
```

---

## HBNU_Monitoring과의 차이점

### 아키텍처 차이

| 항목 | HBU_monitoring | HBNU_Monitoring |
|------|----------------|-----------------|
| **UI 프레임워크** | PySide2 (Qt) | React + TypeScript |
| **백엔드** | 단일 프로세스 | FastAPI (별도 서버) |
| **통신 방식** | 직접 함수 호출 | WebSocket + REST API |
| **CNC 처리** | Subprocess (32비트 Python) | 직접 DLL 로드 |
| **데이터 저장** | Thread 기반 직접 저장 | FastAPI 백엔드 저장 |
| **자동저장** | Trace 로그 모니터링 | Trace 로그 모니터링 (동일) |

### 센서 연결 차이

#### CNC Controller

**HBU_monitoring**:
- Subprocess로 별도 Python 프로세스 실행
- JSON stdout으로 데이터 전송
- 32비트 Python 호환성 해결

**HBNU_Monitoring**:
- 직접 DLL 로드 (ctypes.CDLL)
- 비동기 실행 (asyncio.run_in_executor)
- 64비트 Python 필요

#### 데이터 수집 주기

**HBU_monitoring**:
- CNC: 100Hz (subprocess)
- Laser: 100Hz
- Pyrometer: 100Hz
- Camera: 30Hz
- **통합**: 50Hz (DataCollector)

**HBNU_Monitoring**:
- CNC: 100Hz
- Laser: 100Hz
- Pyrometer: 20Hz (안정화)
- Camera: 30Hz
- **통합**: 10Hz (collect_sensor_data)

### 데이터 저장 차이

**HBU_monitoring**:
- Thread 기반 직접 CSV 저장
- 수동 버퍼 (메모리 임시 저장)
- 1시간마다 CSV 로테이션

**HBNU_Monitoring**:
- FastAPI 백엔드에서 저장
- 임시 저장 (temp_storage)
- 비동기 저장 (asyncio.create_task)

---

## 결론

HBU_monitoring은 **단일 프로세스 GUI 애플리케이션**으로 설계되어 있으며, 센서 연결은 다음과 같은 특징을 가집니다:

1. **CNC는 Subprocess로 분리**: 32비트/64비트 호환성 문제 해결
2. **Thread 기반 수집**: 각 센서가 독립적인 Thread에서 동작
3. **50Hz 통합 수집**: DataCollector가 모든 센서 데이터를 통합
4. **직접 GUI 업데이트**: PySide2를 통한 실시간 시각화

HBNU_Monitoring과 비교하면, **더 단순한 구조**이지만 **32비트 Python 호환성**을 위해 CNC를 별도 프로세스로 분리한 것이 특징입니다.


