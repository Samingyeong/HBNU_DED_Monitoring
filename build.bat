@echo off
echo ========================================
echo HBU Monitoring 실행파일 빌더
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
echo PyInstaller로 실행파일 빌드 중...
echo.

REM PyInstaller 실행
pyinstaller --onefile ^
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
    echo ✅ 빌드 성공!
    echo ========================================
    echo.
    echo 실행파일 위치: dist\HBU_Monitoring.exe
    echo.
    if exist "dist\HBU_Monitoring.exe" (
        for %%A in ("dist\HBU_Monitoring.exe") do echo 파일 크기: %%~zA bytes
    )
    echo.
    echo 배포 방법:
    echo 1. dist\HBU_Monitoring.exe 파일을 복사
    echo 2. 필요한 설정 파일들도 함께 배포
    echo 3. 대상 PC에서 실행
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
