# GitHub 클론 후 설정 가이드 (센서 연결 포함)

코드를 GitHub에서 클론한 뒤 **센서 연결이 안 될 때** 아래 순서대로 확인하세요.

---

## 1. Python 가상환경 및 패키지

클론한 폴더에는 **venv와 node_modules가 없습니다** (.gitignore). 반드시 설치해야 합니다.

```powershell
# 프로젝트 루트에서
cd HBNU_DED_Monitoring

# Python 가상환경 생성 및 활성화
python -m venv venv
.\venv\Scripts\Activate.ps1

# 백엔드 의존성 설치 (pandas, pypylon, fastapi 등)
pip install -r backend\requirements.txt
# 또는 루트 requirements.txt 사용 시
pip install -r requirements.txt
```

- **에러:** `ModuleNotFoundError: No module named 'pandas'` → 위 `pip install`을 실행하세요.

---

## 2. config 폴더 및 설정 파일

센서는 **config/*.ini**에서 IP·COM 포트를 읽습니다. 클론 시 config는 저장소에 포함되어 있지만, **PC마다 값이 다를 수 있습니다.**

| 파일 | 용도 | 확인할 값 |
|------|------|------------|
| **config/HXApi.ini** | CNC | `ip`, `port` (기본 127.0.0.1:3000) |
| **config/IPG.ini** | 레이저 | `ip`, `port` (예: 192.168.3.230, 10001) |
| **config/Pyrometer.ini** | 파이로미터 | `port` (예: COM12) |

- **경로:** 프로젝트 루트의 `config` 폴더. 백엔드는 `backend/` 기준 상대 경로로 찾으므로, **반드시 프로젝트 루트에서 `backend`를 포함한 구조**를 유지하세요.
- **config가 없다면:** 다른 PC에서 복사하거나, 레포의 config 예시를 참고해 IP/COM을 수정하세요.

---

## 3. HXApi DLL (CNC 연결용)

CNC 연결은 **Sensors/HXApi/dll/HXApi.dll**을 사용합니다. 이 폴더는 저장소에 포함되어 있어야 합니다.

- **위치:** `HBNU_DED_Monitoring/Sensors/HXApi/dll/HXApi.dll`
- **없다면:** 다른 PC에서 해당 폴더 전체를 복사하거나, 배포 패키지에서 복원하세요.
- **에러:** `DLL 파일 없음` / `DLL 로드 실패` → 위 경로에 DLL이 있는지 확인하세요.

---

## 4. DED 전용 경로 (선택)

피더 RPM·가스 유량 등은 **DED가 설치된 PC의 GuiState.ini**에서 읽습니다. 해당 PC가 아니면 이 경로는 없을 수 있습니다.

- **경로 예:** `C:\DED\CS5AXIS\Data\GuiState.ini` (또는 `D:\DED\...`)
- **없어도:** 센서(camera, laser, pyrometer, cnc) 연결 자체는 가능합니다. GuiState 데이터만 비어 있을 뿐입니다.

---

## 5. 실행 방법

- **백엔드:** 프로젝트 루트 또는 **backend** 폴더에서 실행합니다.  
  - 루트에서: `python backend/main.py`  
  - backend에서: `python main.py` (이때도 config 경로는 `backend/__file__` 기준으로 잡혀서 프로젝트 루트의 config를 봅니다.)
- **실제로:** 대부분 `cd backend` 후 `python main.py`로 실행하므로, **backend/main.py**의 `__file__`은 `.../backend/main.py`이고, `../config`는 프로젝트 루트의 config로 해석됩니다. **프로젝트 루트를 현재 작업 디렉터리로 두지 않아도** 경로는 맞습니다.

정리하면, **반드시 프로젝트 루트를 기준으로 backend/config/Sensors 폴더 구조가 유지**되어 있으면 됩니다.

---

## 6. 센서별 “연결 안 됨” 체크리스트

| 증상 | 확인 사항 |
|------|------------|
| **Basler 카메라** | 다른 프로그램(Pylon Viewer, DED GUI 등)에서 카메라 사용 중이면 종료. |
| **레이저 (IPG)** | config/IPG.ini의 IP·포트, 레이저 전원·LAN 연결. |
| **파이로미터** | config/Pyrometer.ini의 COM 포트, 다른 프로그램에서 해당 COM 사용 중이면 종료. |
| **CNC** | HXApi 서비스(127.0.0.1:3000) 실행 여부, config/HXApi.ini, Sensors/HXApi/dll 존재. |

자세한 에러별 대처는 **trouble_shooting_md/SENSOR_CONNECTION_ERRORS_KR.md**를 참고하세요.

---

## 요약

1. **클론 후:** `venv` 생성 + `pip install -r backend/requirements.txt`  
2. **config/** IP·COM이 현재 PC/장비에 맞는지 확인  
3. **Sensors/HXApi/dll/** 에 HXApi.dll 존재 여부 확인  
4. DED PC가 아니면 GuiState.ini 없어도 됨 (선택)  
5. 백엔드는 **backend** 또는 프로젝트 루트에서 실행, 폴더 구조만 유지

이후에도 센서 연결이 안 되면, 터미널에 나오는 **에러 메시지**와 **SENSOR_CONNECTION_ERRORS_KR.md**를 함께 확인하면 원인 파악에 도움이 됩니다.
