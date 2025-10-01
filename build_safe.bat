@echo off
echo ========================================
echo HBU Monitoring 안전 빌드 (폴더 방식)
echo ========================================

REM 기존 빌드 폴더 정리
if exist "dist" (
    echo 기존 dist 폴더 삭제 중...
    rmdir /s /q "dist"
)

if exist "build" (
    echo 기존 build 폴더 삭제 중...
    rmdir /s /q "build"
)

if exist "main.spec" (
    echo 기존 spec 파일 삭제 중...
    del "main.spec"
)

echo.
echo PyInstaller로 안전 빌드 중... (폴더 방식)
echo.

REM PyInstaller 실행 (--onedir 방식)
pyinstaller --onedir ^
    --windowed ^
    --name=HBU_Monitoring ^
    --add-data="UI;UI" ^
    --add-data="settings.py;." ^
    --add-data="config;config" ^
    --hidden-import=PySide2.QtCore ^
    --hidden-import=PySide2.QtWidgets ^
    --hidden-import=PySide2.QtGui ^
    --hidden-import=pyqtgraph ^
    --hidden-import=cv2 ^
    --hidden-import=numpy ^
    --hidden-import=pandas ^
    --hidden-import=qt_material ^
    --hidden-import=configparser ^
    --hidden-import=json ^
    --hidden-import=threading ^
    --hidden-import=datetime ^
    --hidden-import=time ^
    --hidden-import=os ^
    --hidden-import=sys ^
    --hidden-import=subprocess ^
    --hidden-import=random ^
    --hidden-import=queue ^
    --hidden-import=shutil ^
    --hidden-import=argparse ^
    --hidden-import=pathlib ^
    --collect-all=PySide2 ^
    --collect-all=pyqtgraph ^
    --collect-all=qt_material ^
    main.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ 안전 빌드 성공!
    echo ========================================
    echo.
    echo 실행파일 위치: dist\HBU_Monitoring\HBU_Monitoring.exe
    echo.
    echo 배포 방법:
    echo 1. dist\HBU_Monitoring 폴더 전체를 복사
    echo 2. 실제 장비에 붙여넣기
    echo 3. HBU_Monitoring.exe 실행
    echo.
    pause
) else (
    echo.
    echo ========================================
    echo ❌ 빌드 실패!
    echo ========================================
    echo.
    echo 오류가 발생했습니다. 로그를 확인하세요.
    echo.
    pause
)
