# HBNU Monitoring System - 전체 구조 및 센서 연결 흐름

## 📋 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [폴더 구조](#폴더-구조)
3. [시스템 아키텍처](#시스템-아키텍처)
4. [센서 연결 방식](#센서-연결-방식)
5. [데이터 흐름](#데이터-흐름)
6. [실시간 모니터링 메커니즘](#실시간-모니터링-메커니즘)
7. [데이터 저장 시스템](#데이터-저장-시스템)
8. [WebSocket 통신 구조](#websocket-통신-구조)
9. [주요 컴포넌트 상세](#주요-컴포넌트-상세)

---

## 프로젝트 개요

**HBNU Monitoring System**은 DED(Direct Energy Deposition) 공정을 실시간으로 모니터링하는 시스템입니다. 다양한 센서에서 데이터를 수집하여 웹 기반 UI로 실시간 시각화하고, 데이터를 자동으로 저장합니다.

### 지원 센서
- **CNC Controller**: HXApi를 통한 위치, 속도, 피드레이트 데이터
- **IPG Laser**: TCP/IP 통신을 통한 레이저 출력 파워 데이터
- **Pyrometer**: 시리얼 통신을 통한 온도 데이터 (MPT, 1CT, 2CT)
- **Basler Camera**: USB3.0 카메라를 통한 용융풀 이미지 및 영역 계산
- **HikRobot Camera**: 2대의 산업용 카메라를 통한 듀얼 뷰 이미지

---

## 폴더 구조

```
HBNU_Monitoring/
├── backend/                      # FastAPI 백엔드 서버
│   ├── main.py                  # FastAPI 앱 및 엔드포인트
│   ├── sensor_manager.py        # 센서 통합 관리자
│   ├── data_storage.py          # 데이터 저장 및 관리
│   ├── websocket_manager.py     # WebSocket 연결 관리
│   ├── gcode_parser.py          # G-code 파싱 (선택적)
│   ├── requirements.txt         # Python 의존성
│   └── images/                  # 이미지 임시 저장 폴더
│
├── frontend/                     # React + TypeScript 프론트엔드
│   ├── src/
│   │   ├── components/          # UI 컴포넌트
│   │   │   ├── Header.tsx       # 시스템 제어 헤더
│   │   │   ├── CNCStatus.tsx    # CNC 상태 표시
│   │   │   ├── Charts.tsx       # 실시간 차트
│   │   │   ├── CameraView.tsx   # 카메라 뷰
│   │   │   ├── ConnectionStatus.tsx  # 연결 상태
│   │   │   └── EmergencyModal.tsx    # 비상 정지 모달
│   │   ├── hooks/
│   │   │   ├── useSensorData.ts # 센서 데이터 관리 훅
│   │   │   └── useAutoSave.ts  # 자동저장 로직 훅
│   │   ├── services/
│   │   │   └── api.ts           # 백엔드 API 통신 서비스
│   │   └── types/               # TypeScript 타입 정의
│   ├── electron/                # Electron 데스크톱 앱 설정
│   └── package.json             # Node.js 의존성
│
├── Sensors/                      # 센서 통신 모듈
│   ├── cnc_comm.py              # CNC (HXApi) 통신
│   ├── laser_comm.py            # IPG 레이저 통신
│   ├── pyrometer_comm.py        # Pyrometer 통신
│   ├── camera_comm.py           # Basler 카메라 통신
│   ├── vision2.py               # HikRobot 카메라 통신
│   ├── ded_log_reader.py        # DED 로그 파일 읽기
│   └── HXApi/                   # HXApi DLL 및 헤더 파일
│       ├── dll/                 # DLL 파일들
│       │   ├── HXApi.dll
│       │   ├── Qt5Core.dll
│       │   └── ...
│       └── include/             # C++ 헤더 파일
│
├── config/                       # 설정 파일 (INI 형식)
│   ├── Main.ini                 # 메인 설정
│   ├── HXApi.ini                # CNC 설정 (IP, Port)
│   ├── IPG.ini                  # 레이저 설정
│   ├── Pyrometer.ini            # Pyrometer 설정
│   └── Camera.ini               # 카메라 설정
│
├── DB/                           # 데이터 저장 폴더
│   └── [저장_폴더명]_[타임스탬프]/
│       ├── [타임스탬프].csv     # 센서 데이터 CSV
│       ├── meltpool_images/     # Basler 카메라 이미지
│       └── captures_hik/        # HikRobot 카메라 이미지
│
├── venv/                         # Python 가상환경
├── start_backend.bat            # 백엔드 실행 스크립트
├── start_frontend.bat           # 프론트엔드 실행 스크립트
└── requirements.txt             # 프로젝트 루트 의존성
```

---

## 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   React UI   │  │  WebSocket   │  │   REST API    │         │
│  │ Components   │◄─┤   Client     │◄─┤   Client     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              ▲ │
                              │ │ HTTP/WebSocket
                              │ │
┌─────────────────────────────┴─┴─────────────────────────────────┐
│                      Backend Layer (FastAPI)                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              FastAPI Server (main.py)                     │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   │
│  │  │   Sensor     │  │     Data     │  │   WebSocket   │  │   │
│  │  │   Manager    │  │   Storage    │  │   Manager    │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ▲ │
                              │ │ Python Threads/Async
                              │ │
┌─────────────────────────────┴─┴─────────────────────────────────┐
│                    Sensor Communication Layer                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │   CNC    │  │  Laser   │  │ Pyrometer│  │ Camera   │      │
│  │ Collector│  │Collector │  │Collector │  │Collector │      │
│  └────┬─────┘  └────┬──────┘  └────┬──────┘  └────┬─────┘      │
│       │            │               │               │            │
│  ┌────▼─────┐  ┌───▼────┐  ┌──────▼────┐  ┌──────▼─────┐     │
│  │   CNC    │  │ Laser  │  │ Pyrometer │  │  Camera    │     │
│  │    DB    │  │   DB   │  │    DB     │  │    DB      │     │
│  └──────────┘  └────────┘  └───────────┘  └────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              ▲ │
                              │ │ Hardware Protocols
                              │ │
┌─────────────────────────────┴─┴─────────────────────────────────┐
│                         Hardware Layer                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │   CNC    │  │  IPG     │  │ Pyrometer │  │ Basler   │      │
│  │Controller│  │  Laser   │  │  Sensor   │  │ Camera   │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 센서 연결 방식

### 1. CNC Controller (HXApi)

**통신 방식**: DLL (Dynamic Link Library) - ctypes를 통한 네이티브 라이브러리 호출

**연결 과정**:
```python
# Sensors/cnc_comm.py
1. HXApi.dll 로드 (ctypes.CDLL)
2. DLL 함수 시그니처 정의 (argtypes, restype)
3. HXApi.ini에서 IP/Port 읽기
4. HxInitialize2() 호출하여 CNC 컨트롤러 연결
5. 연결 성공 시 activate = True
```

**데이터 수집**:
- **샘플링 레이트**: 100Hz (10ms 간격)
- **수집 데이터**:
  - 현재 위치: `curpos_x, y, z, a, c` (HxGetSVF)
  - 머신 위치: `macpos_x, y, z, a, c` (HxGetSNF)
  - 나머지 위치: `rempos_x, y, z, a, c` (HxGetSNF)
  - 피드레이트, 오버라이드 등

**설정 파일**: `config/HXApi.ini`
```ini
[address]
ip = 127.0.0.1
port = 3000
```

**주의사항**: Python과 DLL의 비트(32/64)가 일치해야 함

---

### 2. IPG Laser

**통신 방식**: TCP/IP Socket (TCP 소켓 통신)

**연결 과정**:
```python
# Sensors/laser_comm.py
1. socket.socket() 생성
2. IPG.ini에서 IP/Port 읽기
3. socket.connect()로 레이저 장치 연결
4. 연결 성공 시 activate = True
```

**데이터 수집**:
- **샘플링 레이트**: 100Hz (10ms 간격)
- **통신 프로토콜**:
  - 출력 파워: `"ROP\r"` 명령 전송 → 응답 파싱
  - 설정 파워: `"RCS\r"` 명령 전송 → 응답 파싱
- **수집 데이터**: `outpower`, `setpower`

**설정 파일**: `config/IPG.ini`
```ini
[address]
ip = 192.168.1.100
port = 23
```

---

### 3. Pyrometer

**통신 방식**: Serial (RS-232 시리얼 통신)

**연결 과정**:
```python
# Sensors/pyrometer_comm.py
1. serial.Serial() 생성
2. Pyrometer.ini에서 포트/보드레이트 읽기
3. 시리얼 포트 열기
4. 초기화 명령 "00bum01\r" 전송
5. "ok" 응답 확인 → activate = True
```

**데이터 수집**:
- **샘플링 레이트**: 20Hz (50ms 간격) - 안정화를 위해 100Hz에서 감소
- **통신 프로토콜**:
  - 데이터 요청: `"00bup\r"` 전송
  - 응답: 12자리 16진수 문자열 (예: "0641A0F5B2C3")
  - 파싱: MPT(0-4), 1CT(4-8), 2CT(8-12)
- **수집 데이터**: `mpt` (Melt Pool Temperature), `1ct`, `2ct`
- **안정화 기능**:
  - 버퍼 클리어 (`reset_input_buffer()`)
  - 재시도 로직 (최대 3회)
  - 유효성 검사 (300~4000도 범위)

**설정 파일**: `config/Pyrometer.ini`
```ini
[address]
port = COM3
baudrate = 9600
parity = N
stopbits = 1
bytesize = 8
timeout = 1
```

---

### 4. Basler Camera

**통신 방식**: USB3.0 (Pylon SDK)

**연결 과정**:
```python
# Sensors/camera_comm.py
1. pylon.TlFactory.GetInstance().CreateFirstDevice()로 카메라 검색
2. camera.Open()로 카메라 열기
3. 카메라 설정 (노출시간, 해상도)
4. camera.StartGrabbing()으로 이미지 캡처 시작
```

**데이터 수집**:
- **샘플링 레이트**: 30Hz (33ms 간격)
- **이미지 처리**:
  - 이미지 캡처: `camera.RetrieveResult()`
  - 용융풀 영역 계산: `cv2.threshold()` + 픽셀 카운트
  - 픽셀 크기: 5.13mm × 4.10mm / (720 × 520)
- **수집 데이터**: `image` (numpy array), `melt_pool_area` (mm²)
- **이미지 저장**: 1초마다 `captures_basler/` 폴더에 저장

---

### 5. HikRobot Camera (2대)

**통신 방식**: USB3.0/GigE (MVS SDK)

**연결 과정**:
```python
# Sensors/vision2.py
1. MV_CC_EnumDevices()로 연결된 카메라 검색
2. 시리얼 번호로 특정 카메라 찾기
3. MV_CC_CreateHandle()로 핸들 생성
4. MV_CC_OpenDevice()로 장치 열기
5. MV_CC_StartGrabbing()으로 캡처 시작
```

**데이터 수집**:
- **카메라 1**: 시리얼 번호 `"02J81094725"`
- **카메라 2**: 시리얼 번호 `"02J75405689"`
- **이미지 처리**:
  - 각 카메라에서 프레임 캡처
  - `on_new_frame` 콜백으로 프레임 전달
  - SensorManager에서 2개 이미지를 수평 결합 (`cv2.hconcat()`)
- **수집 데이터**: `combined_image` (numpy array)

---

## 데이터 흐름

### 전체 데이터 흐름도

```
┌─────────────┐
│   Hardware  │
│   Sensors   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│  Sensor Communication Layer (Sensors/*.py)               │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │   CNC    │  │  Laser   │  │ Pyrometer│  │ Camera  ││
│  │    Comm  │  │   Comm   │  │   Comm   │  │  Comm   ││
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬────┘│
│       │            │               │              │      │
│       ▼            ▼               ▼              ▼      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │   CNC    │  │  Laser    │  │ Pyrometer│  │ Camera  ││
│  │Collector │  │Collector  │  │Collector │  │Collector││
│  │(Thread)  │  │(Thread)   │  │(Thread)  │  │(Thread) ││
│  └────┬─────┘  └────┬─────┘  └────┬──────┘  └────┬────┘│
│       │            │               │              │      │
│       ▼            ▼               ▼              ▼      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │   CNC    │  │  Laser   │  │ Pyrometer│  │ Camera  ││
│  │    DB    │  │   DB     │  │    DB    │  │   DB    ││
│  │ (deque)  │  │ (deque)  │  │ (deque)  │  │ (Queue) ││
│  └────┬─────┘  └────┬─────┘  └────┬──────┘  └────┬────┘│
└───────┼─────────────┼─────────────┼──────────────┼──────┘
        │             │             │              │
        └─────────────┴─────────────┴──────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │   SensorManager (backend/)          │
        │   - collect_all_data()              │
        │   - 각 DB에서 최신 데이터 조회       │
        │   - 통합 데이터 구조 생성            │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │   DataStorage (backend/)            │
        │   - store_data()                   │
        │   - 히스토리 저장 (deque)           │
        │   - CSV 저장 (저장 중일 때)         │
        │   - 이미지 저장                     │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │   WebSocketManager (backend/)       │
        │   - broadcast_data()                │
        │   - 모든 클라이언트에 전송          │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │   Frontend (React)                  │
        │   - WebSocketService                │
        │   - useSensorData hook              │
        │   - UI 컴포넌트 업데이트            │
        └─────────────────────────────────────┘
```

### 상세 데이터 흐름 단계

#### 1단계: 센서 데이터 수집 (Thread Level)

각 센서는 독립적인 **Thread**에서 동작하는 **Collector**를 가집니다:

```python
# 예: CNC Collector
class CNC_Collector(threading.Thread):
    def run(self):
        while self.running:
            # 1. 센서에서 데이터 읽기
            data = self.com.get_pos_data()
            
            # 2. DB에 저장 (deque 또는 Queue)
            if data:
                self.db.store_data(data)
            
            # 3. 샘플링 레이트에 맞춰 대기
            time.sleep(1/self.sample_rate)  # 100Hz = 0.01초
```

**특징**:
- 각 센서는 **독립적인 스레드**에서 실행
- **비동기적**으로 데이터 수집 (서로 블로킹하지 않음)
- **고정 샘플링 레이트**로 데이터 수집

#### 2단계: 데이터 버퍼링 (DB Level)

각 센서는 **자체 DB**를 가집니다:

```python
# 예: CNC_DB
class CNC_DB:
    def __init__(self, max_size=100):
        self.data_queue = deque(maxlen=max_size)  # 최대 100개 유지
    
    def store_data(self, data):
        self.data_queue.append(data)  # 최신 데이터 추가
    
    def retrieve_data(self):
        return self.data_queue[-1]  # 최신 데이터 반환
```

**특징**:
- **deque** 또는 **Queue**를 사용한 버퍼링
- 최신 데이터만 유지 (오래된 데이터는 자동 삭제)
- **스레드 안전** (각 스레드가 독립적으로 접근)

#### 3단계: 데이터 통합 (SensorManager Level)

**SensorManager**가 주기적으로 모든 센서 DB에서 데이터를 수집:

```python
# backend/sensor_manager.py
async def collect_all_data(self):
    sensor_data = {
        "timestamp": datetime.now(),
        "camera_data": None,
        "laser_data": None,
        "pyrometer_data": None,
        "cnc_data": None,
        "hik_camera_data": None
    }
    
    # 각 센서 DB에서 최신 데이터 조회
    if self.connection_status["cnc"]:
        cnc_data = await loop.run_in_executor(
            None, self.databases["cnc"].retrieve_data
        )
        sensor_data["cnc_data"] = cnc_data
    
    # ... 다른 센서들도 동일하게
    
    return sensor_data
```

**특징**:
- **비동기 실행** (`asyncio.run_in_executor`)
- 센서 연결 상태 확인 후 데이터 수집
- 통합된 JSON 구조로 반환

#### 4단계: 데이터 저장 (DataStorage Level)

**DataStorage**가 통합 데이터를 받아 저장:

```python
# backend/data_storage.py
def store_data(self, sensor_data):
    # 1. 데이터 정규화
    normalized_data = self._normalize_data(sensor_data)
    
    # 2. 히스토리에 추가 (메모리)
    self.data_history.append(normalized_data)
    
    # 3. 저장 중이면 CSV에 추가
    if self.is_saving:
        asyncio.create_task(self._save_to_csv_async(normalized_data))
    
    # 4. 이미지 저장 (비동기)
    asyncio.create_task(self._save_images_async(normalized_data))
```

**특징**:
- **정규화**: 센서별 데이터를 통일된 형식으로 변환
- **히스토리 관리**: 최근 5000개 데이터 메모리 보관
- **비동기 저장**: CSV/이미지 저장은 블로킹하지 않음

#### 5단계: 실시간 전송 (WebSocket Level)

**WebSocketManager**가 모든 연결된 클라이언트에 브로드캐스트:

```python
# backend/websocket_manager.py
async def broadcast_data(self, sensor_data):
    message = {
        "type": "sensor_data",
        "data": sensor_data,
        "timestamp": datetime.now().isoformat()
    }
    
    # 모든 연결된 클라이언트에 전송
    for connection in self.active_connections:
        await connection.send_text(json.dumps(message))
```

**특징**:
- **브로드캐스트**: 모든 클라이언트에 동시 전송
- **JSON 직렬화**: 데이터를 JSON 문자열로 변환
- **에러 처리**: 연결 끊김 감지 및 자동 제거

#### 6단계: 프론트엔드 수신 (Frontend Level)

**WebSocketService**가 메시지를 수신하고 React 상태 업데이트:

```typescript
// frontend/src/services/api.ts
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'sensor_data') {
        // React 상태 업데이트
        setLatestData(data.data);
        setHistoryData(prev => [...prev, data.data]);
    }
};
```

**특징**:
- **이벤트 기반**: 메시지 수신 시 자동 업데이트
- **상태 관리**: React useState로 최신 데이터 유지
- **히스토리 관리**: 최근 500개 데이터만 유지

---

## 실시간 모니터링 메커니즘

### 데이터 수집 주기

```
┌─────────────────────────────────────────────────────────┐
│              collect_sensor_data() 루프                  │
│              (main.py, 100ms = 10Hz)                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │  SensorManager.collect_all_data()    │
        │  - 각 센서 DB에서 최신 데이터 조회   │
        │  - 통합 데이터 구조 생성             │
        └──────────────┬──────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌───────────────┐            ┌───────────────┐
│ DataStorage   │            │ WebSocket     │
│ .store_data() │            │ .broadcast()  │
│ - 히스토리 저장│            │ - 클라이언트  │
│ - CSV 저장    │            │   전송        │
└───────────────┘            └───────────────┘
```

### 타이밍 다이어그램

```
센서 레벨 (Thread):
CNC Collector:     [100Hz] ████████████████████████████████
Laser Collector:   [100Hz] ████████████████████████████████
Pyrometer:         [20Hz]  ████░░░░░░░░░░░░░░░░░░░░░░░░░░░
Camera Collector:  [30Hz]  ██████░░░░░░░░░░░░░░░░░░░░░░░░░

백엔드 레벨 (Async):
collect_sensor_data: [10Hz] ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  └─> SensorManager.collect_all_data()
  └─> DataStorage.store_data()
  └─> WebSocketManager.broadcast_data()

프론트엔드 레벨:
WebSocket 수신:    [10Hz]  ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  └─> React 상태 업데이트
  └─> UI 리렌더링
```

### 샘플링 레이트 요약

| 센서 | 샘플링 레이트 | 주기 | 데이터 크기 |
|------|--------------|------|------------|
| CNC | 100Hz | 10ms | ~200 bytes |
| Laser | 100Hz | 10ms | ~50 bytes |
| Pyrometer | 20Hz | 50ms | ~50 bytes |
| Basler Camera | 30Hz | 33ms | ~375KB (이미지) |
| HikRobot Camera | ~30Hz | ~33ms | ~2MB (이미지) |
| **백엔드 통합** | **10Hz** | **100ms** | **~2.5MB** |
| **WebSocket 전송** | **10Hz** | **100ms** | **~2.5MB** |

**참고**: 이미지는 Base64 인코딩 또는 별도 엔드포인트로 전송 가능

---

## 데이터 저장 시스템

### 저장 구조

```
DB/
└── [폴더명]_[타임스탬프]/
    ├── [타임스탬프].csv          # 센서 데이터 CSV
    ├── meltpool_images/          # Basler 카메라 이미지
    │   ├── meltpool_00001_20250101_120000_123456.png
    │   └── ...
    └── captures_hik/             # HikRobot 카메라 이미지
        ├── hik_combined_20250101_120000.png
        └── ...
```

### CSV 파일 형식

```csv
timestamp,curpos_x,curpos_y,curpos_z,curpos_a,curpos_c,mpt,melt_pool_area,outpower,setpower
2025-01-01 12:00:00.123,10.5,20.3,5.2,0.0,0.0,1650.5,12.34,450.0,500.0
2025-01-01 12:00:00.223,10.6,20.4,5.3,0.0,0.0,1651.2,12.45,451.0,500.0
...
```

### 저장 모드

#### 1. 수동 저장
```python
# API 호출: POST /api/save/start
{
    "folder_name": "test_session"
}
```
- 사용자가 명시적으로 저장 시작
- 폴더명 지정 가능
- 저장 중지 시 `POST /api/save/stop`

#### 2. 자동 저장 (임시 저장)
```python
# API 호출: POST /api/save/start
{
    "folder_name": "auto_session",
    "auto_save": true
}
```
- 자동저장 모드 활성화
- 임시 스토리지에 데이터 보관 (최대 10,000개)
- 30분 후 자동 정리 (또는 수동 중지)
- 영구 저장 시 `POST /api/save/temp-to-permanent`

#### 3. CSV 로테이션
- 1시간마다 새 CSV 파일 생성
- 파일명: `[타임스탬프].csv`
- 긴 세션에서 파일 크기 관리

---

## WebSocket 통신 구조

### 연결 설정

```
Frontend                    Backend
   │                           │
   │  WebSocket Connect        │
   ├──────────────────────────>│
   │  ws://127.0.0.1:8000/ws   │
   │                           │
   │  Connection Accepted       │
   │<──────────────────────────┤
   │  {"type": "connection"}   │
   │                           │
```

### 메시지 타입

#### 1. sensor_data
```json
{
    "type": "sensor_data",
    "data": {
        "timestamp": "2025-01-01 12:00:00.123",
        "cnc_data": {
            "curpos_x": 10.5,
            "curpos_y": 20.3,
            ...
        },
        "laser_data": {
            "outpower": 450.0,
            "setpower": 500.0
        },
        ...
    },
    "timestamp": "2025-01-01T12:00:00.123456",
    "connection_count": 1
}
```

#### 2. status_update
```json
{
    "type": "status_update",
    "data": {
        "system_status": "running",
        "sensors": {
            "camera": true,
            "laser": true,
            "pyrometer": true,
            "cnc": true
        }
    }
}
```

#### 3. save_status
```json
{
    "type": "save_status",
    "data": {
        "is_saving": true,
        "save_path": "DB/test_session_20250101_120000"
    }
}
```

#### 4. connection
```json
{
    "type": "connection",
    "message": "WebSocket 연결이 성공했습니다",
    "timestamp": "2025-01-01T12:00:00"
}
```

#### 5. error
```json
{
    "type": "error",
    "message": "센서 연결 실패",
    "timestamp": "2025-01-01T12:00:00"
}
```

### 재연결 메커니즘

```typescript
// frontend/src/services/api.ts
class WebSocketService {
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;
    private reconnectInterval = 3000;  // 3초
    
    private handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            setTimeout(() => {
                this.connect();  // 재연결 시도
            }, this.reconnectInterval);
        }
    }
}
```

---

## 주요 컴포넌트 상세

### 1. SensorManager (`backend/sensor_manager.py`)

**역할**: 모든 센서의 통합 관리 및 데이터 수집

**주요 메서드**:
- `initialize()`: 모든 센서 비동기 초기화
- `collect_all_data()`: 모든 센서에서 데이터 수집 및 통합
- `get_connection_status()`: 센서 연결 상태 조회
- `cleanup()`: 리소스 정리

**초기화 순서**:
```python
1. Camera 초기화 (Basler)
2. Laser 초기화 (IPG)
3. Pyrometer 초기화
4. CNC 초기화 (HXApi)
5. HikRobot 카메라 초기화 (2대)
```

**테스트 모드**:
- 모든 센서 연결 실패 시 자동 활성화
- 더미 데이터 생성 (랜덤 값)

---

### 2. DataStorage (`backend/data_storage.py`)

**역할**: 센서 데이터 저장 및 관리

**주요 기능**:
- **히스토리 관리**: 최근 5000개 데이터 메모리 보관
- **CSV 저장**: 저장 모드일 때 CSV 파일에 기록
- **이미지 저장**: Basler/HikRobot 이미지 저장
- **임시 저장**: 자동저장 데이터 보관

**데이터 정규화**:
```python
normalized_data = {
    "timestamp": "2025-01-01 12:00:00.123",
    "curpos_x": 10.5,
    "curpos_y": 20.3,
    "mpt": 1650.5,
    "outpower": 450.0,
    "melt_pool_area": 12.34,
    ...
}
```

---

### 3. WebSocketManager (`backend/websocket_manager.py`)

**역할**: WebSocket 연결 관리 및 브로드캐스트

**주요 기능**:
- **연결 관리**: 클라이언트 연결/해제 추적
- **브로드캐스트**: 모든 클라이언트에 동시 전송
- **에러 처리**: 연결 끊김 자동 감지 및 제거

**연결 상태**:
```python
self.active_connections: List[WebSocket] = []
self.connection_count = 0
```

---

### 4. useSensorData Hook (`frontend/src/hooks/useSensorData.ts`)

**역할**: 센서 데이터 상태 관리 및 WebSocket 통신

**주요 기능**:
- **WebSocket 연결**: 자동 연결 및 재연결
- **상태 관리**: 최신 데이터, 히스토리, 연결 상태
- **이벤트 핸들링**: 센서 데이터, 상태 업데이트, 저장 상태

**상태 구조**:
```typescript
{
    isConnected: boolean;
    latestData: SensorData | null;
    historyData: SensorData[];  // 최대 500개
    systemStatus: SystemStatus | null;
    saveStatus: SaveStatus | null;
    error: string | null;
}
```

---

### 5. 센서 통신 모듈 패턴

모든 센서 통신 모듈은 **동일한 패턴**을 따릅니다:

```python
# 1. Communication 클래스: 하드웨어 통신
class SensorCommunication:
    def __init__(self, config_path):
        # 설정 파일 읽기
        # 하드웨어 연결
        self.activate = True/False
    
    def get_data(self):
        # 하드웨어에서 데이터 읽기
        return data
    
    def close(self):
        # 연결 종료

# 2. DB 클래스: 데이터 버퍼링
class SensorDB:
    def __init__(self, max_size=100):
        self.data_queue = deque(maxlen=max_size)
    
    def store_data(self, data):
        self.data_queue.append(data)
    
    def retrieve_data(self):
        return self.data_queue[-1]

# 3. Collector 클래스: 스레드에서 데이터 수집
class SensorCollector(threading.Thread):
    def __init__(self, com, db, sample_rate):
        self.com = com
        self.db = db
        self.sample_rate = sample_rate
    
    def run(self):
        while self.running:
            data = self.com.get_data()
            if data:
                self.db.store_data(data)
            time.sleep(1/self.sample_rate)
```

---

## 실행 흐름

### 백엔드 시작 (`start_backend.bat`)

```
1. Python 가상환경 활성화
2. backend/requirements.txt 설치
3. python backend/main.py 실행
   │
   ├─> FastAPI 앱 생성
   ├─> lifespan() 실행
   │   ├─> SensorManager 초기화
   │   │   ├─> Camera 초기화
   │   │   ├─> Laser 초기화
   │   │   ├─> Pyrometer 초기화
   │   │   ├─> CNC 초기화
   │   │   └─> HikRobot 초기화
   │   ├─> DataStorage 초기화
   │   ├─> WebSocketManager 초기화
   │   └─> collect_sensor_data() 태스크 시작
   │
   └─> FastAPI 서버 시작 (포트 8000)
       ├─> REST API 엔드포인트 등록
       └─> WebSocket 엔드포인트 등록 (/ws)
```

### 프론트엔드 시작 (`start_frontend.bat`)

```
1. cd frontend
2. npm install
3. npm run dev
   │
   ├─> React 개발 서버 시작 (포트 5173)
   ├─> Electron 앱 시작 (선택적)
   └─> 컴포넌트 마운트
       ├─> useSensorData hook 실행
       │   ├─> WebSocketService.connect()
       │   │   └─> ws://127.0.0.1:8000/ws 연결
       │   └─> 이벤트 리스너 등록
       └─> UI 컴포넌트 렌더링
```

### 데이터 수집 루프

```
collect_sensor_data() (100ms 주기)
    │
    ├─> SensorManager.collect_all_data()
    │   ├─> 각 센서 DB에서 최신 데이터 조회
    │   └─> 통합 데이터 구조 생성
    │
    ├─> DataStorage.store_data()
    │   ├─> 히스토리에 추가
    │   ├─> CSV 저장 (저장 중일 때)
    │   └─> 이미지 저장 (비동기)
    │
    └─> WebSocketManager.broadcast_data()
        └─> 모든 클라이언트에 전송
            └─> Frontend WebSocket 수신
                └─> React 상태 업데이트
                    └─> UI 리렌더링
```

---

## 설정 파일 구조

### HXApi.ini (CNC)
```ini
[address]
ip = 127.0.0.1
port = 3000
```

### IPG.ini (Laser)
```ini
[address]
ip = 192.168.1.100
port = 23

[data]
outpower = 0
setpower = 0
```

### Pyrometer.ini
```ini
[address]
port = COM3
baudrate = 9600
parity = N
stopbits = 1
bytesize = 8
timeout = 1

[data]
mpt = 0
1ct = 0
2ct = 0
```

---

## 주요 기술 스택

### Backend
- **FastAPI**: 비동기 웹 프레임워크
- **uvicorn**: ASGI 서버
- **asyncio**: 비동기 프로그래밍
- **threading**: 센서 데이터 수집 스레드
- **ctypes**: DLL 호출 (HXApi)
- **pyserial**: 시리얼 통신 (Pyrometer)
- **socket**: TCP/IP 통신 (Laser)
- **pypylon**: Basler 카메라 SDK
- **opencv-python**: 이미지 처리

### Frontend
- **React**: UI 프레임워크
- **TypeScript**: 타입 안전성
- **Tailwind CSS**: 스타일링
- **Chart.js**: 차트 시각화
- **Electron**: 데스크톱 앱
- **WebSocket API**: 실시간 통신

---

## 성능 최적화

### 1. 비동기 처리
- 센서 데이터 수집: `asyncio.run_in_executor()`로 블로킹 방지
- CSV/이미지 저장: `asyncio.create_task()`로 비동기 실행

### 2. 메모리 관리
- **deque**: 고정 크기 버퍼 (오래된 데이터 자동 삭제)
- **Queue**: 스레드 안전 버퍼
- 히스토리 제한: 최대 5000개 (백엔드), 500개 (프론트엔드)

### 3. 네트워크 최적화
- **WebSocket**: HTTP 폴링 대신 실시간 양방향 통신
- **JSON 압축**: 필요 시 gzip 압축 가능
- **이미지 최적화**: Base64 대신 별도 엔드포인트 사용 가능

---

## 트러블슈팅

### 센서 연결 실패
1. 설정 파일 확인 (IP, Port, COM 포트)
2. 하드웨어 연결 확인
3. 권한 확인 (시리얼 포트, DLL 로드)
4. 로그 확인: `⚠️ [센서명] 연결 실패`

### WebSocket 연결 실패
1. 백엔드 서버 실행 확인 (포트 8000)
2. 프론트엔드 포트 확인 (기본 8001 → 8000으로 변경 필요)
3. CORS 설정 확인
4. 브라우저 콘솔 에러 확인

### 데이터가 업데이트되지 않음
1. WebSocket 연결 상태 확인
2. 센서 연결 상태 확인 (`/api/status`)
3. 브라우저 콘솔에서 WebSocket 메시지 확인
4. 백엔드 로그에서 데이터 수집 확인

---

## 결론

HBNU Monitoring System은 **계층적 아키텍처**로 설계되어 있습니다:

1. **하드웨어 레이어**: 실제 센서 장치
2. **통신 레이어**: 센서별 통신 모듈 (Thread 기반)
3. **관리 레이어**: SensorManager (센서 통합 관리)
4. **저장 레이어**: DataStorage (데이터 저장)
5. **전송 레이어**: WebSocketManager (실시간 전송)
6. **표시 레이어**: React Frontend (UI)

각 레이어는 **독립적으로 동작**하며, **비동기 처리**를 통해 **실시간 모니터링**을 구현합니다.

