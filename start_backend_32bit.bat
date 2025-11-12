@echo off
echo 🚀 HBNU Monitoring Backend 서버 시작 중 (32비트 모드)...
echo.

REM 가상환경 활성화 (있는 경우)
if exist "venv\Scripts\activate.bat" (
    echo 📦 가상환경 활성화 중...
    call venv\Scripts\activate.bat
)

REM 환경 변수 설정 (CNC Subprocess 모드)
set USE_CNC_SUBPROCESS=true
REM 32비트 Python 경로를 여기에 설정하세요
set CNC_PYTHON_EXECUTABLE=C:\Python310-32\python.exe
REM 또는 사용자별 경로:
REM set CNC_PYTHON_EXECUTABLE=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310-32\python.exe

echo 📌 CNC Subprocess 모드: 활성화
echo    Python 경로: %CNC_PYTHON_EXECUTABLE%
echo.

REM 백엔드 의존성 설치
echo 📚 백엔드 의존성 설치 중...
cd backend
pip install -r requirements.txt
cd ..

REM 백엔드 서버 시작
echo 🌐 FastAPI 서버 시작 중...
echo 서버 주소: http://127.0.0.1:8000
echo API 문서: http://127.0.0.1:8000/docs
echo 데이터 수집 주기: 50Hz (HBU_monitoring 방식)
echo.
python backend\main.py

pause

