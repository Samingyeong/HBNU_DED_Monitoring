# HBNU Monitoring System - 아키텍처 문서

## 📋 개요

기존 PyQt 기반 모니터링 시스템을 **React + Electron + FastAPI** 아키텍처로 리팩토링한 실시간 DED(Direct Energy Deposition) 공정 모니터링 시스템입니다.

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Electron)              │
├─────────────────────────────────────────────────────────────┤
│  • React Components (UI)                                   │
│  • WebSocket Client (실시간 데이터)                        │
│  • REST API Client (제어 명령)                             │
│  • Recharts (데이터 시각화)                                │
└─────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/WebSocket
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                        │
├─────────────────────────────────────────────────────────────┤
│  • FastAPI Server (REST API + WebSocket)                   │
│  • Sensor Manager (센서 통신 관리)                         │
│  • Data Storage (데이터 저장)                              │
│  • WebSocket Manager (실시간 브로드캐스트)                 │
└─────────────────────────────────────────────────────────────┘
                                │
                                │ 기존 센서 통신 모듈 재사용
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    Sensor Layer                             │
├─────────────────────────────────────────────────────────────┤
│  • Basler Camera (Melt pool 영역 계산)                     │
│  • HikRobot Camera x2 (비전 시스템)                        │
│  • IPG Laser (출력/설정 파워)                              │
│  • Pyrometer (온도 측정)                                   │
│  • HXApi CNC (좌표 정보)                                   │
└─────────────────────────────────────────────────────────────┘
```

## 📁 디렉토리 구조

```
HBNU_Monitoring/
├── backend/                    # FastAPI 백엔드
│   ├── main.py                # 메인 서버 파일
│   ├── sensor_manager.py      # 센서 통신 관리
│   ├── data_storage.py        # 데이터 저장 로직
│   ├── websocket_manager.py   # WebSocket 관리
│   ├── requirements.txt       # 백엔드 의존성
│   └── __init__.py
├── frontend/                   # React + Electron 프론트엔드
│   ├── src/
│   │   ├── components/        # React 컴포넌트
│   │   │   ├── Header.tsx     # 헤더 (제어 버튼, 상태 표시)
│   │   │   ├── CNCStatus.tsx  # CNC 상태 표시
│   │   │   ├── ConnectionStatus.tsx # 센서 연결 상태
│   │   │   ├── CameraView.tsx # 카메라 이미지 표시
│   │   │   ├── Charts.tsx     # 실시간 차트
│   │   │   └── EmergencyModal.tsx # 비상 정지 모달
│   │   ├── services/
│   │   │   └── api.ts         # API 서비스 및 WebSocket
│   │   ├── hooks/
│   │   │   └── useSensorData.ts # 센서 데이터 관리 훅
│   │   └── App.tsx           # 메인 앱 컴포넌트
│   ├── electron/              # Electron 설정
│   └── package.json          # 프론트엔드 의존성
├── Sensors/                   # 기존 센서 통신 모듈 (재사용)
│   ├── camera_comm.py        # Basler 카메라
│   ├── laser_comm.py         # IPG 레이저
│   ├── pyrometer_comm.py     # Pyrometer
│   ├── cnc_comm.py           # HXApi CNC
│   └── vision2.py            # HikRobot 카메라
├── config/                    # 설정 파일들
├── start_backend.bat         # 백엔드 시작 스크립트
├── start_frontend.bat        # 프론트엔드 시작 스크립트
└── README_ARCHITECTURE.md    # 이 문서
```

## 🔄 데이터 플로우

### 1. 센서 데이터 수집
```
센서 → 센서 통신 모듈 → SensorManager → DataStorage
```

### 2. 실시간 데이터 전송
```
DataStorage → WebSocketManager → Frontend (WebSocket)
```

### 3. REST API 통신
```
Frontend → FastAPI → SensorManager/DataStorage
```

### 4. 데이터 저장
```
센서 데이터 → DataStorage → CSV 파일 + 이미지 파일
```

## 🚀 시작 방법

### 1. 백엔드 서버 시작
```bash
# Windows
start_backend.bat

# 또는 수동으로
cd backend
pip install -r requirements.txt
python main.py
```

### 2. 프론트엔드 시작
```bash
# Windows
start_frontend.bat

# 또는 수동으로
cd frontend
npm install
npm run dev
```

## 📊 주요 기능

### 백엔드 (FastAPI)
- **센서 통신 관리**: 모든 센서의 연결 및 데이터 수집 관리
- **실시간 데이터 전송**: WebSocket을 통한 실시간 데이터 브로드캐스트
- **REST API**: 시스템 제어 및 상태 조회 API
- **데이터 저장**: CSV 및 이미지 파일 저장
- **비동기 처리**: 모든 센서 데이터를 비동기적으로 처리

### 프론트엔드 (React + Electron)
- **실시간 모니터링**: WebSocket을 통한 실시간 데이터 표시
- **데이터 시각화**: Recharts를 사용한 차트 및 그래프
- **카메라 뷰**: Basler 및 HikRobot 카메라 이미지 표시
- **시스템 제어**: 데이터 저장 시작/중지, 비상 정지
- **연결 상태 모니터링**: 센서 및 백엔드 연결 상태 표시

## 🔧 API 엔드포인트

### REST API
- `GET /api/status` - 시스템 상태 조회
- `GET /api/data/latest` - 최신 센서 데이터
- `GET /api/data/history` - 히스토리 데이터
- `POST /api/save/start` - 데이터 저장 시작
- `POST /api/save/stop` - 데이터 저장 중지
- `GET /api/save/status` - 저장 상태 조회

### WebSocket
- `ws://127.0.0.1:8000/ws` - 실시간 데이터 스트림

## 📈 센서 데이터 구조

```json
{
  "timestamp": "2024-01-01 12:00:00.000",
  "camera_data": {
    "image": "base64_encoded_image",
    "melt_pool_area": 15.25
  },
  "laser_data": {
    "outpower": 500.0,
    "setpower": 500.0
  },
  "pyrometer_data": {
    "mpt": 1650.5,
    "1ct": 1620.0,
    "2ct": 1680.0
  },
  "cnc_data": {
    "curpos_x": 10.5,
    "curpos_y": 20.3,
    "curpos_z": 5.2,
    "curpos_a": 0.0,
    "curpos_c": 0.0
  },
  "hik_camera_data": {
    "combined_image": "base64_encoded_image"
  }
}
```

## 🎨 UI 컴포넌트 구조

### 주요 컴포넌트
- **Header**: 시스템 제어, 저장 상태, 비상 정지 버튼
- **CNCStatus**: CNC 좌표, 피드레이트, 가스 정보 표시
- **ConnectionStatus**: 모든 센서 연결 상태 표시
- **CameraView**: Basler/HikRobot 카메라 이미지 탭 전환
- **Charts**: 실시간 데이터 차트 (온도, 영역, 레이저 파워)
- **EmergencyModal**: 비상 정지 확인 모달

### 데이터 관리
- **useSensorData 훅**: 모든 센서 데이터 상태 관리
- **API 서비스**: REST API 및 WebSocket 통신
- **실시간 업데이트**: WebSocket을 통한 자동 데이터 갱신

## 🔒 보안 고려사항

- **CORS 설정**: 개발 환경에서 모든 도메인 허용 (프로덕션에서는 제한 필요)
- **API 인증**: 필요시 JWT 토큰 기반 인증 추가
- **네트워크 보안**: 내부 네트워크에서만 사용 권장

## 🐛 문제 해결

### 백엔드 연결 실패
1. 백엔드 서버가 실행 중인지 확인
2. 포트 8000이 사용 가능한지 확인
3. 센서 하드웨어 연결 상태 확인

### 프론트엔드 빌드 오류
1. Node.js 버전 확인 (권장: 16+)
2. `npm install` 재실행
3. `node_modules` 폴더 삭제 후 재설치

### 센서 연결 오류
1. 센서 하드웨어 연결 상태 확인
2. 설정 파일(`config/` 폴더) 확인
3. 백엔드 로그에서 오류 메시지 확인

## 📝 개발 노트

### 기존 시스템과의 차이점
- **UI 프레임워크**: PyQt → React + Electron
- **백엔드**: 단일 애플리케이션 → FastAPI 서버
- **통신 방식**: 직접 호출 → REST API + WebSocket
- **데이터 저장**: UI 스레드 → 백그라운드 비동기 처리

### 장점
- **확장성**: 모듈화된 구조로 기능 추가 용이
- **유지보수성**: 프론트엔드/백엔드 분리로 독립적 개발 가능
- **성능**: 비동기 처리로 응답성 향상
- **사용자 경험**: 현대적인 웹 UI/UX

### 기존 코드 재사용
- **센서 통신 모듈**: `Sensors/` 폴더의 모든 코드 재사용
- **설정 파일**: `config/` 폴더의 INI 파일들 재사용
- **데이터 저장 형식**: CSV 형식 유지
- **센서 설정**: 기존 설정 구조 유지

## 🔄 마이그레이션 가이드

### 1단계: 백엔드 서버 시작
```bash
# 백엔드 의존성 설치 및 서버 시작
start_backend.bat
```

### 2단계: 프론트엔드 시작
```bash
# 프론트엔드 의존성 설치 및 개발 서버 시작
start_frontend.bat
```

### 3단계: 센서 연결 확인
- 백엔드 로그에서 센서 연결 상태 확인
- 프론트엔드 UI에서 연결 상태 표시 확인

### 4단계: 기능 테스트
- 실시간 데이터 표시 확인
- 차트 업데이트 확인
- 카메라 이미지 표시 확인
- 데이터 저장 기능 테스트

## 🎯 향후 개선 방향

### 단기 계획
- 이미지 압축 및 최적화
- 에러 처리 및 복구 로직 강화
- 로그 시스템 개선

### 장기 계획
- 클라우드 연동 (데이터 백업)
- 모바일 앱 지원
- AI 기반 이상 탐지 기능
- 다중 클라이언트 지원

이 아키텍처를 통해 기존 시스템의 안정성을 유지하면서도 현대적인 웹 기술을 활용한 확장 가능한 모니터링 시스템을 구축할 수 있습니다.
