@echo off
echo 🎨 HBNU Monitoring Frontend 시작 중...
echo.

REM 프론트엔드 디렉토리로 이동
cd frontend

REM 의존성 설치
echo 📚 프론트엔드 의존성 설치 중...
npm install

REM 개발 서버 시작
echo 🖥️ React + Electron 개발 서버 시작 중...
echo.
npm run dev

pause
