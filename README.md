# HBNU Monitoring System

DED(Direct Energy Deposition) 모니터링 시스템 - 실시간 센서 데이터 수집 및 시각화

## 🚀 주요 기능

### 1. 실시간 센서 모니터링
- **CNC 데이터**: 위치, 피드레이트, 피더 상태, 가스 유량
- **레이저 데이터**: 출력 파워, 설정 파워
- **파이로미터 데이터**: 용융풀 온도, 주변 온도
- **카메라 데이터**: 용융풀 영역, 이미지 캡처
- **HikRobot 카메라**: 듀얼 카메라 시스템

### 2. 자동저장 시스템
- **로그 파일 모니터링**: `Trace_YYYY-MM-DD.txt`, `Exception_YYYY-MM-DD.txt`
- **자동 시작/중지**: Trace 로그의 시작/종료 이벤트 감지
- **예외 처리**: Exception 로그 발생 시 자동 중지
- **경로 지원**: C드라이브 기본, D드라이브 폴백

### 3. 비상 정지 시스템
- **즉시 중지**: 모든 센서 데이터 수집 중단
- **확인 모달**: 사용자 확인 후 실행
- **안전 장치**: 레이저 출력 즉시 중단

### 4. 현대적 UI/UX
- **React + TypeScript**: 타입 안전성과 개발 효율성
- **Tailwind CSS**: 반응형 디자인
- **Electron**: 데스크톱 애플리케이션
- **실시간 차트**: Chart.js 기반 데이터 시각화

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Sensors       │
│   (React/TS)    │◄──►│   (FastAPI)     │◄──►│   (Hardware)    │
│                 │    │                 │    │                 │
│ • Real-time UI  │    │ • Data Collection│    │ • CNC Controller│
│ • Auto-save     │    │ • WebSocket     │    │ • Laser System  │
│ • Emergency     │    │ • File Monitor  │    │ • Pyrometer     │
│ • Charts        │    │ • API Endpoints │    │ • Cameras       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 프로젝트 구조

```
HBNU_Monitoring/
├── frontend/                 # React 프론트엔드
│   ├── src/
│   │   ├── components/       # UI 컴포넌트
│   │   │   ├── Header.tsx   # 시스템 제어 헤더
│   │   │   ├── CNCStatus.tsx # CNC 상태 표시
│   │   │   ├── Charts.tsx   # 실시간 차트
│   │   │   ├── CameraView.tsx# 카메라 뷰
│   │   │   └── EmergencyModal.tsx # 비상 정지 모달
│   │   ├── hooks/           # 커스텀 훅
│   │   │   ├── useSensorData.ts # 센서 데이터 관리
│   │   │   └── useAutoSave.ts  # 자동저장 로직
│   │   ├── services/        # API 서비스
│   │   │   └── api.ts       # 백엔드 통신
│   │   └── types/          # TypeScript 타입 정의
│   ├── electron/           # Electron 설정
│   └── dist/               # 빌드 결과물
├── backend/                 # FastAPI 백엔드
│   ├── main.py             # 메인 서버
│   ├── sensor_manager.py   # 센서 관리자
│   └── models/             # 데이터 모델
├── Sensors/                # 센서 통신 모듈
│   ├── cnc_comm.py         # CNC 통신
│   ├── laser_comm.py        # 레이저 통신
│   ├── pyrometer_comm.py   # 파이로미터 통신
│   ├── camera_comm.py      # 카메라 통신
│   └── HXApi/              # HXApi DLL
├── config/                 # 설정 파일
│   ├── Main.ini
│   ├── Camera.ini
│   ├── Laser.ini
│   ├── Pyrometer.ini
│   └── HXApi.ini
├── DB/                     # 데이터베이스
├── test_backend.py         # 테스트용 백엔드 (시뮬레이션)
└── main.py                 # 메인 애플리케이션 (PySide2)
```

## 🛠️ 설치 및 실행

### 1. 환경 설정
```bash
# Python 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 프론트엔드 실행
```bash
cd frontend
npm install
npm run dev
```

### 3. 백엔드 실행

#### 실제 센서 연결 (main.py)
```bash
python main.py
```

#### 테스트용 시뮬레이션 (test_backend.py)
```bash
python test_backend.py
```

## 🔧 설정

### 센서 설정 파일
- `config/Main.ini`: 메인 설정
- `config/Camera.ini`: 카메라 설정
- `config/Laser.ini`: 레이저 설정
- `config/Pyrometer.ini`: 파이로미터 설정
- `config/HXApi.ini`: CNC 설정

### 자동저장 설정
- **기본 경로**: `C:\DED\Log\`
- **폴백 경로**: `D:\DED\Log\`
- **모니터링 파일**: 
  - `Trace\Trace_YYYY-MM-DD.txt`
  - `Exception\Exception_YYYY-MM-DD.txt`

## 📊 API 엔드포인트

### 시스템 상태
- `GET /api/status` - 시스템 상태 조회
- `GET /api/data/latest` - 최신 센서 데이터
- `GET /api/data/history` - 히스토리 데이터

### 데이터 저장
- `POST /api/save/start` - 저장 시작
- `POST /api/save/stop` - 저장 중지
- `GET /api/save/status` - 저장 상태

### 비상 정지
- `POST /api/emergency/toggle` - 비상 정지 토글

### WebSocket
- `WS /ws` - 실시간 데이터 스트림

## 🧪 테스트 모드

센서가 없는 환경에서 테스트하려면:

```bash
# 테스트 백엔드 실행 (포트 8001)
python test_backend.py

# 프론트엔드 실행 (포트 5173)
cd frontend
npm run dev
```

테스트 백엔드는 실제 센서 데이터를 시뮬레이션하여 모든 기능을 테스트할 수 있습니다.

## 🔄 최근 업데이트

### v2.0.0 (2025-10-07)
- ✅ **자동저장 시스템 구현**: 로그 파일 모니터링 기반 자동 시작/중지
- ✅ **비상 정지 개선**: 직관적인 확인 모달 UI
- ✅ **테스트 백엔드 추가**: 센서 없이도 전체 기능 테스트 가능
- ✅ **현대적 UI**: React + TypeScript + Tailwind CSS
- ✅ **실시간 모니터링**: WebSocket 기반 실시간 데이터 전송
- ✅ **Electron 통합**: 데스크톱 애플리케이션 지원

## 📝 개발 노트

### 자동저장 로직
- Trace 파일에서 `NC_CS5Axis,StartNormal,step,10` 감지 시 자동저장 시작
- Trace 파일에서 `NC_CS5AXIS,IsRunning,False` 감지 시 자동저장 중지
- Exception 파일에서 오류 감지 시 자동저장 중지

### 센서 연결
- 실제 센서: `main.py` 실행 (포트 8000)
- 테스트 모드: `test_backend.py` 실행 (포트 8001)

## 🤝 기여

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

Copyright by KITECH V2.0

---

**개발 환경**: React + Electron + FastAPI + Python  
**센서 지원**: CNC, Laser, Pyrometer, Camera, HikRobot  
**데이터베이스**: CSV 파일 기반  
**실시간 통신**: WebSocket
