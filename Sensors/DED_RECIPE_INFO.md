# DED 레시피 파일 정보

## 📁 파일 위치
- **원본**: `C:\DED\Recipe\`
- **백업**: `Sensors\DED_Recipe_*.rcp`

## 📋 레시피 파일 구조

### 1. 피더 설정 (Feeder Configuration)

#### COATING 모드
```ini
CoatingFeederRPM1=100
CoatingFeederGas1=7.000
IsSelectedCoatingFeeder1=True
```

#### NORMAL 모드
```ini
NormalFeederRPM1=9
NormalFeederGas1=5.500
IsSelectedNormalFeeder1=False
```

#### SCAN 모드
```ini
ScanFeederRPM1=100
ScanFeederGas1=7.000
IsSelectedScanFeeder1=True
```

### 2. 피더 번호별 설정
- **Feeder 1~6**: 각각 독립적인 RPM 및 Gas 설정
- **RPM 범위**: 일반적으로 9~100 RPM
- **Gas 범위**: 4.5~12.0 L/min

### 3. 가스 설정
```ini
CoaxialGas=7.000
ShieldGas=12.000
```

### 4. 레이저 설정
```ini
LaserPower=445
```

## 🔧 CNC 레지스터 맵핑

피더 RPM 데이터는 CNC의 R 레지스터에서 읽어옵니다:

### 피더 RPM
- **Feeder1 RPM**: R100
- **Feeder2 RPM**: R101
- **Feeder3 RPM**: R102

### 피더 잔량
- **Feeder1 잔량**: R110
- **Feeder2 잔량**: R111
- **Feeder3 잔량**: R112

### 피더 상태
- **Feeder1 상태**: R120.0 (비트)
- **Feeder2 상태**: R120.1 (비트)
- **Feeder3 상태**: R120.2 (비트)

### 가스 유량
- **Coaxial Gas**: R130
- **Feeding Gas**: R131
- **Shield Gas**: R132

## 📝 참고사항

1. **레지스터 번호 확인**:
   - CNC 화면 → 파라미터 → I/O 설정 → PLC 모니터
   - R 레지스터 값 실시간 확인 가능

2. **레시피 파일 수정**:
   - DED 프로그램에서 직접 수정
   - 또는 텍스트 에디터로 `.rcp` 파일 편집

3. **백업**:
   - 레시피 변경 전 백업 권장
   - 원본 파일: `C:\DED\Recipe\`

## 🔗 관련 파일

- **CNC 통신**: `Sensors/cnc_comm.py`
- **백엔드 센서 관리**: `backend/sensor_manager.py`
- **프론트엔드 표시**: `frontend/src/components/CNCStatus.tsx`

