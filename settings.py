import os

# 프로젝트 루트 경로 (main.py가 있는 위치 기준)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# config 폴더 경로
CONFIG_DIR = os.path.join(BASE_DIR, "config")

# 설정 파일 경로들
CAMERA_CONFIG_PATH = os.path.join(CONFIG_DIR, "Camera.ini")
HXAPI_CONFIG_PATH = os.path.join(CONFIG_DIR, "HXApi.ini")
IPG_CONFIG_PATH = os.path.join(CONFIG_DIR, "IPG.ini")
PYROMETER_CONFIG_PATH = os.path.join(CONFIG_DIR, "Pyrometer.ini")
MAIN_CONFIG_PATH = os.path.join(CONFIG_DIR, "Main.ini")

# 예시로 추가할 수도 있음
SAVE_PATH_DEFAULT = os.path.join(BASE_DIR, "DB")

CNC_PYTHON_EXECUTABLE = r"C:/Users/user/AppData/Local/Programs/Python/Python36-32/python.exe"
CNC_SCRIPT_PATH = r"./Sensors/cnc_comm.py"