# DED 로그 모니터링 기능

## 개요

HBU_monitoring 시스템에 DED 시스템의 공정 시작/종료 로그를 실시간으로 읽어서 CSV 파일에 자동 저장하는 기능이 추가되었습니다.

## 주요 기능

### 1. 실시간 DED 로그 모니터링
- DED 시스템의 Trace 로그 파일을 실시간으로 모니터링
- 공정 시작/종료 이벤트를 자동으로 감지
- NC 시작/종료 이벤트도 함께 추적

### 2. 자동 CSV 저장
- 공정 이벤트를 별도 CSV 파일에 자동 저장
- 기존 센서 데이터 CSV에 공정 상태 컬럼 추가
- 날짜별로 파일 분리 저장

### 3. UI 상태 표시
- 실시간 공정 상태를 UI에 표시
- 공정 실행 중/중지/불명 상태 구분

## 파일 구조

```
HBU_monitoring/
├── Sensors/
│   ├── ded_log_reader.py          # DED 로그 읽기 클래스
│   └── ...
├── Monitoring/
│   └── DB/
│       ├── [프로젝트폴더]/
│       │   ├── YYYYMMDDHHMMSS.csv # 센서 데이터 (공정 상태 포함)
│       │   └── ...
├── DB/
│   └── process_logs/              # 공정 이벤트 전용 폴더
│       └── process_log_YYYYMMDD.csv
└── test_ded_log_monitoring.py     # 테스트 스크립트
```

## 사용 방법

### 1. 기본 사용
```python
from Sensors.ded_log_reader import DEDLogReader, DEDProcessLogger

# DED 로그 리더 초기화
reader = DEDLogReader()
logger = DEDProcessLogger()

# 모니터링 시작
reader.start_monitoring()

# 현재 공정 상태 확인
status = reader.get_current_process_status()
print(f"공정 상태: {status}")  # 'running', 'stopped', 'unknown'

# 모니터링 중지
reader.stop_monitoring()
```

### 2. 이벤트 처리
```python
# 새로운 이벤트 읽기
new_events = reader.read_new_log_lines()
for event in new_events:
    print(f"이벤트: {event['event']} at {event['timestamp']}")
    logger.save_event(event)  # CSV에 저장
```

### 3. 이벤트 타입
- `process_start`: 공정 시작 (NC_CS5AXIS,IsRunning,True)
- `process_end`: 공정 종료 (NC_CS5AXIS,IsRunning,False)
- `nc_start`: NC 시작 (IsNCStarted = true)
- `nc_end`: NC 종료 (IsNCStarted = false)

## CSV 파일 형식

### 1. 센서 데이터 CSV (기존 + 공정 상태)
```csv
time,curpos_x,curpos_y,curpos_z,curpos_a,curpos_c,mpt,melt_pool_area,outpower,process_status
2025-08-18 15:59:58.477,-137.52,-160.48,-64.37,0.0,0.0,699.9,,0.0,running
```

### 2. 공정 이벤트 CSV (새로 추가)
```csv
timestamp,datetime,event,message,raw_line
2025-08-25, 13:27:52.30,2025-08-25 13:27:52.300000,process_start,NC_CS5AXIS;IsRunning;True,2025-08-25; 13:27:52.30; NC_CS5AXIS;IsRunning;True
```

## 테스트

### 1. 로그 파싱 테스트
```bash
cd HBU_monitoring
python test_ded_log_monitoring.py
# 선택: 1 (로그 파싱 테스트)
```

### 2. 실시간 모니터링 테스트
```bash
cd HBU_monitoring
python test_ded_log_monitoring.py
# 선택: 2 (실시간 모니터링 테스트)
```

## 설정

### 1. DED 로그 경로 설정
기본 경로: `C:/DED/Log/Trace`
```python
reader = DEDLogReader(ded_log_path="C:/DED/Log/Trace")
```

### 2. CSV 저장 경로 설정
기본 경로: `DB/process_logs`
```python
logger = DEDProcessLogger(save_dir="DB/process_logs")
```

## 통합된 기능

### 1. main.py에 자동 통합
- 프로그램 시작 시 자동으로 DED 로그 모니터링 시작
- 저장 버튼 클릭 시 공정 이벤트도 함께 저장
- UI에 실시간 공정 상태 표시

### 2. 데이터 수집기와 연동
- 센서 데이터와 공정 상태를 동시에 수집
- 공정 상태가 센서 데이터 CSV에 추가 컬럼으로 포함

## 주의사항

1. **DED 시스템 경로**: DED 시스템이 `C:/DED/` 경로에 설치되어 있어야 합니다.
2. **로그 파일 권한**: Trace 로그 파일에 읽기 권한이 있어야 합니다.
3. **실시간 모니터링**: 프로그램이 실행 중일 때만 로그를 모니터링합니다.
4. **파일 크기**: 로그 파일이 매우 클 수 있으므로 메모리 사용량을 주의하세요.

## 문제 해결

### 1. 로그 파일을 찾을 수 없는 경우
```python
# 로그 파일 경로 확인
reader = DEDLogReader()
print(f"로그 파일 경로: {reader.get_current_log_file()}")
```

### 2. 이벤트가 감지되지 않는 경우
- DED 시스템이 실제로 공정을 실행하고 있는지 확인
- 로그 파일이 실시간으로 업데이트되고 있는지 확인
- 로그 파일 형식이 예상과 다른지 확인

### 3. CSV 저장 오류
- 저장 디렉토리에 쓰기 권한이 있는지 확인
- 디스크 공간이 충분한지 확인

## 업데이트 내역

- **v1.0**: 기본 DED 로그 모니터링 기능 추가
- **v1.1**: CSV 자동 저장 기능 추가
- **v1.2**: UI 상태 표시 기능 추가
- **v1.3**: 테스트 스크립트 추가
