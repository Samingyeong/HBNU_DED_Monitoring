# 32비트 Python 환경 설정 가이드

HXApi DLL이 32비트로 컴파일되어 있어 32비트 Python 환경이 필요합니다.

## 1. 32비트 Python 설치

### Windows에서 32비트 Python 다운로드

1. **Python 공식 사이트 방문**
   - https://www.python.org/downloads/
   - 또는 직접 링크: https://www.python.org/downloads/release/python-31011/
   - **Windows installer (32-bit)** 선택

2. **설치 시 주의사항**
   - ✅ "Add Python to PATH" 체크
   - ✅ "Install for all users" 선택 (선택적)
   - 설치 경로 확인 (예: `C:\Python310-32\`)

3. **설치 확인**
   ```powershell
   # 명령 프롬프트에서
   python --version
   # Python 3.10.11 출력 확인
   
   # 비트 확인
   python -c "import platform; print(platform.architecture()[0])"
   # 32bit 출력 확인
   ```

## 2. 가상환경 재구축

### 기존 64비트 가상환경 삭제

```powershell
# 프로젝트 루트에서
Remove-Item -Recurse -Force venv
```

### 32비트 Python으로 새 가상환경 생성

```powershell
# 32비트 Python으로 가상환경 생성
C:\Python310-32\python.exe -m venv venv

# 또는 PATH에 32비트 Python이 먼저 등록되어 있다면
python -m venv venv
```

### 가상환경 활성화

```powershell
.\venv\Scripts\activate

# 비트 확인
python -c "import platform; print(platform.architecture()[0])"
# 32bit 출력 확인
```

## 3. 의존성 설치

### 백엔드 의존성 설치

```powershell
# pip 업그레이드
python -m pip install --upgrade pip

# 백엔드 의존성 설치
cd backend
pip install -r requirements.txt
cd ..
```

### 프로젝트 루트 의존성 설치

```powershell
pip install -r requirements.txt
```

### 32비트 호환 버전 확인

일부 패키지는 32비트 버전이 없을 수 있습니다. 문제가 발생하면:

1. **numpy**: 32비트 지원 확인
   ```powershell
   pip install "numpy<1.24"  # 1.24 이상은 32비트 미지원 가능
   ```

2. **opencv-python**: 32비트 지원 확인
   ```powershell
   pip install opencv-python==4.8.1.78  # 특정 버전 사용
   ```

## 4. CNC Subprocess 모드 설정

### 방법 1: 환경 변수 설정

```powershell
# PowerShell에서
$env:USE_CNC_SUBPROCESS = "true"
$env:CNC_PYTHON_EXECUTABLE = "C:\Python310-32\python.exe"

# 백엔드 실행
python backend\main.py
```

### 방법 2: .env 파일 생성

프로젝트 루트에 `.env` 파일 생성:

```env
USE_CNC_SUBPROCESS=true
CNC_PYTHON_EXECUTABLE=C:\Python310-32\python.exe
```

### 방법 3: 코드에서 직접 설정

`backend/main.py` 수정:

```python
sensor_manager = SensorManager(
    use_cnc_subprocess=True,
    cnc_python_path=r"C:\Python310-32\python.exe"
)
```

## 5. CNC 통신 스크립트 수정

`Sensors/cnc_comm.py`의 `__main__` 부분을 프로젝트 경로에 맞게 수정:

```python
if __name__ == "__main__":
    # 프로젝트 루트 기준으로 경로 설정
    import os
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(base_path, "config", "HXApi.ini")
    
    com = CNCCommunication(config_path=config_path)
    db = CNC_DB()
    collector = CNC_Collector(com, db)
    collector.start()

    try:
        while True:
            if db.data_queue:
                data = db.retrieve_data()
                print(json.dumps(data, ensure_ascii=False), flush=True)
            time.sleep(0.03)
    except KeyboardInterrupt:
        print('종료 요청 감지')
        collector.stop()
    except Exception as e:
        print(f'Error: {e}')
        collector.stop()
```

## 6. 테스트

### CNC 통신 단독 테스트

```powershell
# 32비트 Python으로 직접 실행
C:\Python310-32\python.exe Sensors\cnc_comm.py

# JSON 출력이 나오면 성공
```

### 백엔드 서버 실행

```powershell
# 가상환경 활성화
.\venv\Scripts\activate

# 환경 변수 설정
$env:USE_CNC_SUBPROCESS = "true"
$env:CNC_PYTHON_EXECUTABLE = "C:\Python310-32\python.exe"

# 백엔드 실행
python backend\main.py
```

## 7. 문제 해결

### DLL 로드 실패

**에러**: `[WinError 193] %1은(는) 올바른 Win32 응용 프로그램이 아닙니다`

**해결**:
1. Python 비트 확인: `python -c "import platform; print(platform.architecture()[0])"`
2. DLL 비트 확인: `dumpbin /headers Sensors\HXApi\dll\HXApi.dll | findstr machine`
3. 일치하지 않으면 subprocess 모드 사용

### Subprocess 시작 실패

**에러**: `CNC subprocess 시작 실패`

**해결**:
1. Python 경로 확인: `CNC_PYTHON_EXECUTABLE` 환경 변수 확인
2. cnc_comm.py 경로 확인
3. config/HXApi.ini 파일 존재 확인

### 패키지 설치 실패

**에러**: `ERROR: Could not find a version that satisfies the requirement`

**해결**:
1. 32비트 지원 버전 확인
2. requirements.txt에서 버전 명시
3. pip 캐시 클리어: `pip cache purge`

## 8. 성능 최적화

### 샘플링 레이트

- **CNC Collector**: 100Hz (10ms)
- **Laser Collector**: 100Hz (10ms)
- **Pyrometer Collector**: 20Hz (50ms) - 안정화
- **Camera Collector**: 30Hz (33ms)
- **데이터 통합**: 50Hz (20ms) - HBU_monitoring 방식

### 메모리 관리

32비트 Python은 메모리 제한(약 2GB)이 있으므로:
- 데이터 히스토리 크기 제한 (5000개)
- 이미지 버퍼 크기 제한 (10개)
- 주기적인 가비지 컬렉션

## 9. 배치 파일 생성

`start_backend_32bit.bat` 생성:

```batch
@echo off
echo 🚀 HBNU Monitoring Backend 서버 시작 중 (32비트 모드)...
echo.

REM 가상환경 활성화
if exist "venv\Scripts\activate.bat" (
    echo 📦 가상환경 활성화 중...
    call venv\Scripts\activate.bat
)

REM 환경 변수 설정
set USE_CNC_SUBPROCESS=true
set CNC_PYTHON_EXECUTABLE=C:\Python310-32\python.exe

REM 백엔드 의존성 설치
echo 📚 백엔드 의존성 설치 중...
cd backend
pip install -r requirements.txt
cd ..

REM 백엔드 서버 시작
echo 🌐 FastAPI 서버 시작 중...
echo 서버 주소: http://127.0.0.1:8000
echo API 문서: http://127.0.0.1:8000/docs
echo CNC Subprocess 모드: 활성화
echo.
python backend\main.py

pause
```

## 10. 확인 체크리스트

- [ ] 32비트 Python 설치 완료
- [ ] 가상환경 재생성 (32비트)
- [ ] 모든 의존성 설치 완료
- [ ] CNC 통신 단독 테스트 성공
- [ ] 환경 변수 설정 완료
- [ ] 백엔드 서버 실행 성공
- [ ] WebSocket 연결 확인
- [ ] 센서 데이터 수신 확인

## 참고

- **HBNU_Monitoring**: 50Hz 데이터 통합 (HBU_monitoring 방식)
- **CNC Subprocess**: 32비트 Python 호환성 보장
- **실시간 모니터링**: Thread 기반 독립 수집 + 50Hz 통합

