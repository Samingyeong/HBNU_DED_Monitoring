@echo off
echo 🚀 HBNU Monitoring Backend 서버 시작 중...
echo.

REM 가상환경 활성화 (있는 경우)
if exist "venv\Scripts\activate.bat" (
    echo 📦 가상환경 활성화 중...
    call venv\Scripts\activate.bat
)

REM 백엔드 의존성 설치
echo 📚 백엔드 의존성 설치 중...
cd backend
pip install -r requirements.txt

REM 백엔드 서버 시작
echo 🌐 FastAPI 서버 시작 중...
echo 서버 주소: http://127.0.0.1:8000
echo API 문서: http://127.0.0.1:8000/docs
echo.
python main.py

pause
