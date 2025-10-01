# main.py

from UI.Template_ui import Ui_DED_Monitoring
from UI.save_path_ui import Ui_Dialog as save_UI_Dialog
from UI.ui_camera_setting import Ui_Cam_set

from PySide2 import QtCore
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from qt_material import apply_stylesheet

import argparse
import configparser
import subprocess
import pyqtgraph as pg
import sys, os, time, cv2, numpy as np, pandas as pd, random, queue
from threading import Thread
from datetime import datetime, timedelta
import json

from settings import (
    CAMERA_CONFIG_PATH, HXAPI_CONFIG_PATH, IPG_CONFIG_PATH, PYROMETER_CONFIG_PATH,
    MAIN_CONFIG_PATH, CNC_PYTHON_EXECUTABLE, CNC_SCRIPT_PATH
)
from Sensors.camera_comm import CameraCommunication, CameraDB, CameraCollector
from Sensors.laser_comm import LaserCommunication, LaserDB, IPG_Collector
from Sensors.pyrometer_comm import PyrometerCommunication, PyrometerDB, PyrometerCollector

# ✅ HikRobot 추가
from Sensors.vision2 import HikCameraThread

my_font = QFont("Times New Roman", 15)
my_font2 = QFont("Times New Roman", 12)

parser = argparse.ArgumentParser(description="DED Monitoring Program")
parser.add_argument('--testmode', action='store_true', help="Run in test mode with random data")
args = parser.parse_args()


# -------------------------------------------------- Mainwindow -------------------------------------------------- #
class Mainwindow(QMainWindow):
    def __init__(self, testmode: bool = False):
        super().__init__()
        self.testmode = testmode

        # UI
        self.ui = Ui_DED_Monitoring()
        self.ui.setupUi(self)

        # 데이터 수집기
        self.DC = DataCollector(main=self, testmode=self.testmode)

        # UI 초기화
        self.setup_button_actions()
        self.graphs_init()
        self.is_running = False
        self.camera_active = False
        self.is_saving = False

        # 타이머
        self.current_time = QTimer(self)
        self.current_time.timeout.connect(self.update_current_time)
        self.current_time.start(1000)

        self.graph_update_timer = QTimer(self)
        self.graph_update_timer.timeout.connect(self.update_gui)

        self.image_update_timer = QTimer(self)
        self.image_update_timer.timeout.connect(self.draw_image)

        # 시작
        time.sleep(0.2)
        self.DC.start_threads()
        self.graph_update_timer.start(100)   # 10 Hz
        self.image_update_timer.start(33)    # ~30 fps

    def exit(self):
        print("[EXIT] Exiting program...")
        self.is_running = False
        self.is_saving = False
        try:
            self.graph_update_timer.stop()
            self.image_update_timer.stop()
            self.current_time.stop()
        except Exception as e:
            print(f"[EXIT] Timer stop error: {e}")
        try:
            if getattr(self.DC, 'cnc_process', None):
                self.DC.cnc_process.terminate()
            if getattr(self.DC, 'ipg_collector', None):
                self.DC.ipg_collector.stop(); self.DC.ipg_collector.join()
            if getattr(self.DC, 'pyro_collector', None):
                self.DC.pyro_collector.stop(); self.DC.pyro_collector.join()
            if getattr(self.DC, 'cam_collector', None):
                self.DC.cam_collector.stop(); self.DC.cam_collector.join()
            if getattr(self.DC, 'hik_cam_thread', None):
                self.DC.hik_cam_thread.stop(); self.DC.hik_cam_thread.join()
        except Exception as e:
            print(f"[EXIT] collectors stop error: {e}")
        QCoreApplication.instance().quit()

    def setup_button_actions(self):
        self.ui.Save_btn.clicked.connect(self.save_clicked)
        self.ui.setting_btn.clicked.connect(self.open_cam_ui)
        self.ui.Exit_btn.clicked.connect(self.exit)

    def graphs_init(self):
        self.set_serial_style(self.ui.meltpool_area, 'Melt Pool Area', 'Area(㎟)', 'Time', -1, 5)
        self.set_serial_style(self.ui.meltpool_temp, 'Melt Pool Temperature', 'Temperature(°C)', 'Time', 670, 2350, True)
        self.set_serial_style(self.ui.laserpower, 'Laser Power', 'Power(W)', 'Time', -20, 1100, True)
        self.line_data1 = self.ui.meltpool_temp.plot([], [], pen=pg.mkPen(width=3, color='r'), name='Melt Pool temperature')
        self.line_data2 = self.ui.meltpool_area.plot([], [], pen=pg.mkPen(width=3, color='b'), name='Melt Pool Area')
        self.line_data3 = self.ui.laserpower.plot([], [], pen=pg.mkPen(width=3, color='orange'), name='Out Power')
        self.line_data4 = self.ui.meltpool_temp.plot([], [], pen=pg.mkPen(width=3, color='green', style=QtCore.Qt.DotLine), name='1-color temperature')
        self.line_data5 = self.ui.laserpower.plot([], [], pen=pg.mkPen(width=3, color='orange', style=QtCore.Qt.DotLine), name='Set Power')

    def save_clicked(self, checked: bool):
        if checked:
            self.open_save_ui()
            self.is_saving = True
            self.save_thread = Thread(target=self.save, daemon=True)
            self.save_thread.start()
        else:
            self.is_saving = False
            if hasattr(self, 'save_thread'):
                self.save_thread.join(timeout=1)

    def update_current_time(self):
        self.ui.current_time.setDateTime(QDateTime.currentDateTime())

    def update_gui(self):
        try:
            def safe_format(value, fmt="{:.2f}", default="N/A"):
                if isinstance(value, list):
                    value = value[-1] if value else None
                if value is None:
                    return default
                try:
                    return fmt.format(value)
                except Exception:
                    return default
            # CNC 값 업데이트
            self.ui.cur_x_val.setText(safe_format(self.DC.data_storage.get('curpos_x')))
            self.ui.cur_y_val.setText(safe_format(self.DC.data_storage.get('curpos_y')))
            self.ui.cur_z_val.setText(safe_format(self.DC.data_storage.get('curpos_z')))
            self.ui.cur_a_val.setText(safe_format(self.DC.data_storage.get('curpos_a')))
            self.ui.cur_c_val.setText(safe_format(self.DC.data_storage.get('curpos_c')))
        except Exception as e:
            print(f"!!!!!!!!Error in update_gui: {e}")
        self.draw_graph()
        self.update_connection_status()
    def update_connection_status(self):
        """각 센서 연결 상태를 UI 동그라미로 표시"""
        def set_dot(widget_name: str, ok: bool, radius: int = 10):
            w = getattr(self.ui, widget_name, None)
            if w is None:
                print(f"[WARN] status dot not found: {widget_name}")
                return
            color = "green" if ok else "red"
            w.setStyleSheet(f"border-radius: {radius}px; background-color: {color};")

        # Basler
        set_dot("camera_status_circle", bool(getattr(self.DC, "camera_connected", False)))
        # Pyrometer
        set_dot("pyrometer_status_circle", bool(getattr(self.DC, "pyro_connected", False)))
        # Laser (IPG)
        set_dot("laser_status_circle", bool(getattr(self.DC, "ipg_connected", False)))
        # HikRobot 1, 2
        set_dot("hik_status_circle_1", bool(getattr(self.DC, "hik_connected_1", False)))
        set_dot("hik_status_circle_2", bool(getattr(self.DC, "hik_connected_2", False)))

    def draw_graph(self):
        try:
            self.line_data1.setData(self.DC.data_storage.get('_t', []), self.DC.data_storage.get('mpt', []))
            self.line_data2.setData(self.DC.data_storage.get('_t', []), self.DC.data_storage.get('melt_pool_area', []))
            self.line_data3.setData(self.DC.data_storage.get('_t', []), self.DC.data_storage.get('outpower', []))
            self.line_data4.setData(self.DC.data_storage.get('_t', []), self.DC.data_storage.get('1ct', []))
            self.line_data5.setData(self.DC.data_storage.get('_t', []), self.DC.data_storage.get('setpower', []))
        except Exception as e:
            print(f"!!!!!!!!draw_graph() graph Error: {e}")

    def draw_image(self):
        try:
            # Basler
            basler_imgs = self.DC.data_storage.get('image')
            if basler_imgs:
                self.update_label_with_img(self.ui.img_label, basler_imgs[-1])

            # HikRobot (좌우 합쳐진 이미지)
            hik_img = self.DC.get_combined_hik_image()
            if hik_img is not None:
                print(f"[DEBUG] HikRobot 이미지 표시 중: {hik_img.shape}")
                self.update_label_with_img(self.ui.hik_img_label, hik_img)
            else:
                print("[DEBUG] HikRobot 이미지가 None입니다.")
                # 개별 프레임 상태 확인
                print(f"[DEBUG] Frame1: {self.DC.latest_frame1 is not None}, Frame2: {self.DC.latest_frame2 is not None}")
        except Exception as e:
            print(f"!!!!!!!!draw_image() image Error: {e}")

    def update_label_with_img(self, label, img):
        if img.ndim == 2:
            h, w = img.shape
            qimg = QImage(img.data, w, h, w, QImage.Format_Grayscale8)
        else:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, _ = img_rgb.shape
            qimg = QImage(img_rgb.data, w, h, w * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qimg).scaled(540, 340, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pix)

    def set_serial_style(self, obj, title, labelx, labely, vmin, vmax, legend=False):
        obj.setBackground('#e6e6e6')
        obj.setLabel('top', title, color='black')
        obj.setLabel('left', labelx, color='black')
        obj.setLabel('bottom', labely, color='black', units='s')
        obj.setLabel('right', ' ', color='black')
        obj.setYRange(vmin, vmax, padding=0)
        obj.showGrid(y=True)
        if legend:
            obj.addLegend(brush=(255, 255, 255, 255), pen=pg.mkPen(color=(0, 0, 0)), size=(50, 15), offset=(5, 5), labelTextColor=(0, 0, 0))

    def save(self):
        folder_generator = True
        start_time = datetime.now()
        file_name = str(start_time.strftime("%Y%m%d%H%M%S"))
        expected_columns = ['time', 'curpos_x', 'curpos_y', 'curpos_z', 'curpos_a', 'curpos_c', 'mpt', 'melt_pool_area', 'outpower']

        if folder_generator and hasattr(self, 'folder_path') and self.folder_path:
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
            file_name = os.path.join(self.folder_path, f"{file_name}.csv")
            self.csv_path = file_name   # ✅ CSV 경로 저장
            folder_generator = False

        while self.is_saving:
            loop_start_time = time.perf_counter()
            current_time = datetime.now()

            # 1시간마다 새로운 CSV 생성
            if (current_time - start_time) >= timedelta(hours=1):
                file_name = os.path.join(self.folder_path, f"{current_time.strftime('%Y%m%d%H%M%S')}.csv")
                self.csv_path = file_name   # ✅ 최신 CSV 경로 갱신
                start_time = current_time

            data_to_save = {}
            for key, value in self.DC.data_storage.items():
                if isinstance(value, list):
                    data_to_save[key] = value[-1] if len(value) > 0 else None
                else:
                    data_to_save[key] = value

            save_row = {col: data_to_save.get(col, None) for col in expected_columns}
            _df = pd.DataFrame([save_row])

            if os.path.exists(file_name):
                _df.to_csv(file_name, header=None, index=False, mode='a')
            else:
                _df.to_csv(file_name, header=True, index=False, mode='w')

            time.sleep(max(0, (1/30) - (time.perf_counter() - loop_start_time)))

    def open_cam_ui(self,
                    cam_config_path=CAMERA_CONFIG_PATH,
                    CNC_config_path=HXAPI_CONFIG_PATH,
                    IPG_config_path=IPG_CONFIG_PATH,
                    Pyro_config_path=PYROMETER_CONFIG_PATH):
        cam_config = configparser.ConfigParser()
        cnc_config = configparser.ConfigParser()
        ipg_config = configparser.ConfigParser()
        pyro_config = configparser.ConfigParser()
        cam_config.read(cam_config_path)
        cnc_config.read(CNC_config_path)
        ipg_config.read(IPG_config_path)
        pyro_config.read(Pyro_config_path)
        dialog = QDialog(self)
        ui = Ui_Cam_set()
        ui.setupUi(dialog)

    def open_save_ui(self, config_path=MAIN_CONFIG_PATH):
        config = configparser.ConfigParser()
        config.read(config_path)
        dialog = QDialog(self)
        ui = save_UI_Dialog()
        ui.setupUi(dialog)
        ui.lineEdit.setText(str(config['save_path']['path']))
        if dialog.exec_() == QDialog.Accepted:
            self.folder_path = "Monitoring/DB/" + ui.lineEdit.text()
            config['save_path']['path'] = ui.lineEdit.text()
            with open(MAIN_CONFIG_PATH, 'w') as configfile:
                config.write(configfile)
            print(f"Save Path: {self.folder_path}")
        else:
            print("Dialog canceled")


# -------------------------------------------- DataCollector -------------------------------------------- #
import os
import cv2
import time
import json
import configparser
import numpy as np
from threading import Thread
from datetime import datetime

class DataCollector:
    def __init__(self, main, testmode: bool = False):
        super().__init__()
        self.MW = main
        self.testmode = testmode
        self.camera_connected = False
        self.hik_connected_1 = False
        self.hik_connected_2 = False
        self.ipg_connected = False
        self.pyro_connected = False
        self.config_data = self.load_config_keys()
        self.sample_rate = 50
        self.cnc_data = {}
        self.cnc_thread_running = True
        self.cnc_process = None
        self.cnc_thread = None

        # ---- 이미지 저장 관련 ----
        self.save_dir = None   # Basler 저장 디렉토리
        self.hik_save_dir = None  # HikRobot 저장 디렉토리
        self.frame_id = 0
        self.last_hik_save = 0

        # ---- HikRobot 프레임 ----
        self.latest_frame1 = None
        self.latest_frame2 = None

        if not self.testmode:
            self.setup_sensors()

    def setup_sensors(self):
        # Basler
        try:
            self.cam = CameraCommunication()
            self.cam_db = CameraDB()
            self.cam_collector = CameraCollector(self.cam, self.cam_db)
            self.cam_collector.start()
            self.camera_connected = True
            print("Basler camera connected.")
        except Exception as e:
            print(f"[Warning] Basler connection failed: {e}")
            self.camera_connected = False

        # HikRobot 2대
        try:
            def push_hik_frame_1(frame):
                self.latest_frame1 = frame
                print(f"[DEBUG] HikRobot-1 프레임 저장됨: {frame.shape}")

            def push_hik_frame_2(frame):
                self.latest_frame2 = frame
                print(f"[DEBUG] HikRobot-2 프레임 저장됨: {frame.shape}")

            self.hik_cam_thread_1 = HikCameraThread("02J81094725", on_new_frame=push_hik_frame_1, parent=self)
            self.hik_cam_thread_1.start()
            self.hik_connected_1 = True

            self.hik_cam_thread_2 = HikCameraThread("02J75405689", on_new_frame=push_hik_frame_2, parent=self)
            self.hik_cam_thread_2.start()
            self.hik_connected_2 = True

            print("HikRobot cameras connected.")
        except Exception as e:
            print(f"[Warning] HikRobot connection failed: {e}")
            self.hik_connected_1 = False
            self.hik_connected_2 = False

        # CNC
        try:
            self.cnc_process = subprocess.Popen(
                [CNC_PYTHON_EXECUTABLE, CNC_SCRIPT_PATH],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding='cp949'
            )
            self.cnc_thread_running = True
            self.cnc_thread = Thread(target=self.cnc_data_collector, args=(self.cnc_process,), daemon=True)
            self.cnc_thread.start()
        except Exception as e:
            print(f"[Warning] CNC process start failed: {e}")
            self.cnc_process = None; self.cnc_thread = None

        # IPG
        try:
            self.ipg = LaserCommunication()
            self.ipg_db = LaserDB()
            self.ipg_collector = IPG_Collector(self.ipg, self.ipg_db)
            self.ipg_collector.start()
            self.ipg_connected = True
        except Exception as e:
            print(f"[Warning] IPG Laser connection failed: {e}")
            self.ipg = None; self.ipg_db = None; self.ipg_collector = None
            self.ipg_connected = False

        # Pyrometer
        try:
            self.pyro = PyrometerCommunication()
            self.pyro_db = PyrometerDB()
            self.pyro_collector = PyrometerCollector(self.pyro, self.pyro_db)
            self.pyro_collector.start()
            self.pyro_connected = True
        except Exception as e:
            print(f"[Warning] Pyrometer connection failed: {e}")
            self.pyro = None; self.pyro_db = None; self.pyro_collector = None
            self.pyro_connected = False

    # ✅ HikRobot 이미지 합치기 함수
    def get_combined_hik_image(self):
        """HikRobot 2대 이미지를 좌우로 붙여 반환"""
        print(f"[DEBUG] get_combined_hik_image 호출 - Frame1: {self.latest_frame1 is not None}, Frame2: {self.latest_frame2 is not None}")
        
        if self.latest_frame1 is not None and self.latest_frame2 is not None:
            try:
                h1, w1 = self.latest_frame1.shape[:2]
                h2, w2 = self.latest_frame2.shape[:2]
                print(f"[DEBUG] Frame1 크기: {h1}x{w1}, Frame2 크기: {h2}x{w2}")
                h = max(h1, h2)
                f1 = cv2.resize(self.latest_frame1, (w1, h))
                f2 = cv2.resize(self.latest_frame2, (w2, h))
                combined = cv2.hconcat([f1, f2])
                print(f"[DEBUG] 합쳐진 이미지 크기: {combined.shape}")
                return combined
            except Exception as e:
                print(f"[Warning] Failed to combine HikRobot frames: {e}")
        else:
            print("[DEBUG] HikRobot 프레임 중 하나 이상이 None입니다.")
        return None

    def cnc_data_collector(self, proc):
        while self.cnc_thread_running and proc and proc.stdout:
            output = proc.stdout.readline()
            if not output:
                break
            try:
                data = json.loads(output.strip())
                self.cnc_data = data
            except Exception as e:
                print(f"Error parsing CNC JSON data: {e}")

    def stop_threads(self):
        self.is_running = False
        self.cnc_thread_running = False
        if getattr(self, 'cnc_process', None):
            try:
                self.cnc_process.terminate()
                self.cnc_process.wait(timeout=5)
            except Exception as e:
                print(f"[EXIT] CNC subprocess termination error: {e}")
            self.cnc_process = None
        if getattr(self, 'cam_collector', None):
            try:
                self.cam_collector.stop(); self.cam_collector.join()
            except Exception:
                pass
            self.cam_collector = None; self.camera_connected = False
        if getattr(self, 'ipg_collector', None):
            try:
                self.ipg_collector.stop(); self.ipg_collector.join()
            except Exception:
                pass
            self.ipg_collector = None; self.ipg_connected = False
        if getattr(self, 'pyro_collector', None):
            try:
                self.pyro_collector.stop(); self.pyro_collector.join()
            except Exception:
                pass
            self.pyro_collector = None; self.pyro_connected = False

    def start_threads(self):
        self.initialize_data_storage_list()
        Thread(target=self.collect_and_merge_data_list, daemon=True).start()

    def load_config_keys(self, config_path=MAIN_CONFIG_PATH):
        config = configparser.ConfigParser(); config.read(config_path)
        self.cnc_keys = [k for k in config['cnc']] if 'cnc' in config else []
        self.ipg_keys = [k for k in config['ipg']] if 'ipg' in config else []
        self.pyro_keys = [k for k in config['pyro']] if 'pyro' in config else []
        self.camera_keys = [k for k in config['camera']] if 'camera' in config else []
        return {'cnc': self.cnc_keys, 'ipg': self.ipg_keys, 'pyro': self.pyro_keys, 'camera': self.camera_keys}

    def initialize_data_storage_list(self):
        self.data_storage = {'time': [], '_t': []}
        for key in self.config_data['ipg'] + self.config_data['pyro'] + self.config_data['camera']:
            self.data_storage[key] = []
        for k in ['image', 'melt_pool_area', 'mpt', 'outpower', '1ct', 'setpower']:
            if k not in self.data_storage:
                self.data_storage[k] = []
        for key in self.config_data['cnc']:
            self.data_storage[key] = None

    def update_data_storage_list(self, new_data: dict):
        for key, value in new_data.items():
            if key == 'time':
                self.data_storage[key].append(value)
            elif key == '_t':
                self.data_storage[key].append(value)
                if len(self.data_storage['_t']) > 5000:
                    self.data_storage['_t'].pop(0)
            elif key in self.config_data['cnc']:
                self.data_storage[key] = value
            elif key == 'image':
                if 'image' not in self.data_storage:
                    self.data_storage['image'] = []
                if len(self.data_storage['image']) >= 10:
                    self.data_storage['image'].pop(0)
                self.data_storage['image'].append(value)
            else:
                if key not in self.data_storage:
                    self.data_storage[key] = []
                if len(self.data_storage[key]) >= 5000:
                    self.data_storage[key].pop(0)
                self.data_storage[key].append(value)

    def collect_and_merge_data_list(self):
        """각 센서 통신 데이터의 DB에서 가장 최근값을 불러와서 data_storage를 업데이트"""
        start_time = time.perf_counter()
        self.is_running = True

        while self.is_running:
            loop_start_time = time.perf_counter()
            elapsed_time = round(time.perf_counter() - start_time, 3)
            current_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

            ipg_data, pyro_data, camera_data = {}, {}, {}

            if self.testmode:
                for key in self.cnc_keys:
                    self.cnc_data[key] = round(random.gauss(50, 50), 3)
                for key in self.ipg_keys:
                    ipg_data[key] = random.gauss(500, 10)
                for key in self.pyro_keys:
                    pyro_data[key] = random.gauss(1600, 100)
            else:
                try:
                    if getattr(self, 'ipg_db', None):
                        ipg_data = self.ipg_db.retrieve_data() or {}
                except Exception as e:
                    print(f"[Warning] IPG retrieve fail: {e}")

                try:
                    if getattr(self, 'pyro_db', None):
                        pyro_data = self.pyro_db.retrieve_data() or {}
                except Exception as e:
                    print(f"[Warning] Pyrometer retrieve fail: {e}")

                try:
                    if getattr(self, 'cam_db', None):
                        tmp = self.cam_db.retrieve_data() or {}
                        if isinstance(tmp, np.ndarray):
                            camera_data = {"image": tmp}
                        elif isinstance(tmp, dict):
                            camera_data = dict(tmp)
                        else:
                            camera_data = {}
                        if "image" not in camera_data:
                            for k in ("Image", "img", "frame", "raw", "gray", "gray8"):
                                if k in camera_data:
                                    camera_data["image"] = camera_data.pop(k)
                                    break
                        if "melt_pool_area" not in camera_data:
                            for k in ("meltpool_area", "MP_area", "mp_area"):
                                if k in camera_data:
                                    camera_data["melt_pool_area"] = camera_data.pop(k)
                                    break
                except Exception as e:
                    print(f"[Warning] Camera retrieve fail: {e}")
                    camera_data = {}

            # ---- 머지 ----
            merged_data = {"time": current_time, "_t": elapsed_time}
            if self.cnc_data: merged_data.update(self.cnc_data)
            if ipg_data: merged_data.update(ipg_data)
            if pyro_data: merged_data.update(pyro_data)
            if isinstance(camera_data, dict) and camera_data:
                merged_data.update(camera_data)

            # ---- Basler meltpool 이미지 저장 ----
            try:
                frame = camera_data.get("image") if isinstance(camera_data, dict) else None
                power = float(ipg_data.get("outpower", 0.0)) if ipg_data else 0.0
                area = camera_data.get("melt_pool_area", 0.0) if camera_data else 0.0

                if power > 10 and frame is not None:
                    # 최초 CSV 경로 기반으로 저장 폴더 생성
                    if self.save_dir is None and getattr(self.MW, "csv_path", None):
                        base_dir = os.path.dirname(self.MW.csv_path)
                        self.save_dir = os.path.join(base_dir, "meltpool_images")
                        os.makedirs(self.save_dir, exist_ok=True)

                    if self.save_dir:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        filename = os.path.join(
                            self.save_dir,
                            f"meltpool_{self.frame_id:05d}_{timestamp}.png"
                        )
                        cv2.imwrite(filename, frame)
                        print(f"[SAVE] {filename} (Power={power:.1f} W, Area={area:.2f} mm²)")
                        self.frame_id += 1
            except Exception as e:
                print(f"[Warning] Meltpool image save error: {e}")

            # ---- HikRobot 합쳐진 이미지 저장 (1초마다) ----
            try:
                # 최초 CSV 경로 기반으로 저장 폴더 생성
                if not hasattr(self, "hik_save_dir"):
                    self.hik_save_dir = None
                if not hasattr(self, "last_hik_save"):
                    self.last_hik_save = 0

                if self.hik_save_dir is None and getattr(self.MW, "csv_path", None):
                    base_dir = os.path.dirname(self.MW.csv_path)
                    self.hik_save_dir = os.path.join(base_dir, "captures_hik")
                    os.makedirs(self.hik_save_dir, exist_ok=True)

                # 1초 간격으로 저장
                if (time.time() - self.last_hik_save) >= 1.0:
                    combined = self.get_combined_hik_image()
                    if combined is not None and self.hik_save_dir:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = os.path.join(
                            self.hik_save_dir,
                            f"hik_combined_{timestamp}.png"
                        )
                        cv2.imwrite(filename, combined)
                        print(f"[Hik SAVE] {filename}")
                    self.last_hik_save = time.time()
            except Exception as e:
                print(f"[Warning] HikRobot save error: {e}")

            # ---- 기존 로직 ----
            if len(merged_data) > 2:
                self.update_data_storage_list(merged_data)

            time.sleep(max(0, (1/self.sample_rate) - (time.perf_counter() - loop_start_time)))


# -------------------------------------------- Main 실행부 -------------------------------------------- #
if __name__ == '__main__':
    print(os.path.abspath(__file__))
    extra = {'font_size': '20px'}
    app = QApplication(sys.argv)
    myWindow = Mainwindow(testmode=args.testmode)
    apply_stylesheet(app, theme='light_blue.xml', extra=extra)
    myWindow.show()
    sys.exit(app.exec_())