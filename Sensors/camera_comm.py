# Sensors/camera_comm.py
from pypylon import pylon
import cv2
import numpy as np
import time
import threading
from queue import Queue, Empty
import os

def _camera_error_hint(err: Exception) -> str:
    """Basler 연결 실패 시 원인 안내 메시지 반환"""
    msg = str(err)
    if "exclusively opened by another client" in msg or "exclusively opened" in msg.lower():
        return (
            "Basler 카메라가 다른 프로그램에서 이미 사용 중입니다. "
            "Pylon Viewer, DED 제어 프로그램 등 카메라를 사용하는 프로그램을 모두 종료한 뒤 다시 시도하세요."
        )
    if "No device" in msg or "no device" in msg.lower():
        return "Basler 카메라가 연결되지 않았거나 전원/USB를 확인하세요."
    return msg


class CameraCommunication:
    def __init__(self):
        connected = False
        last_error = None
        for i in range(3):
            try:
                self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
                self.camera.Open()
                self.cam_setting()
                print("Basler Camera Connected!")
                connected = True
                break
            except Exception as e:
                last_error = e
                hint = _camera_error_hint(e)
                # 재시도 시 같은 메시지 반복 출력 방지: 마지막 시도에서만 안내
                if i == 2:
                    print(f"[Basler] 연결 실패: {hint}")
                time.sleep(1)

        if not connected:
            hint = _camera_error_hint(last_error) if last_error else "카메라 연결을 확인하세요."
            raise Exception(hint)

        try:
            pf = self.camera.PixelFormat
            if "Mono8" in pf.Symbolics:
                pf.SetValue("Mono8")
        except Exception:
            pass

        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        fov_w, fov_h = 5.13, 4.10  # mm
        width, height = 720, 520
        self.pixel_size = (fov_w * fov_h) / (width * height)

    def cam_setting(self, expos=400, width=720, height=520):
        self.camera.ExposureTime.SetValue(expos)
        self.camera.Width.SetValue(width)
        self.camera.Height.SetValue(height)

    def get_data(self):
        img = None
        try:
            grab_result = self.camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
            if grab_result.GrabSucceeded():
                img = grab_result.Array.copy()
            grab_result.Release()
        except Exception as e:
            print(f"Error during image acquisition: {e}")
        return img

    def calculate_melt_pool_area(self, img, threshold=120):
        if img is None:
            return 0.0
        _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        pixel_count = np.sum(binary == 255)
        area = (pixel_count * self.pixel_size)
        return round(area, 3)

    def close(self):
        if self.camera.IsGrabbing():
            self.camera.StopGrabbing()
        self.camera.Close()
        print("Basler Camera Closed.")


class CameraDB:
    def __init__(self, max_size=30):
        self.data_queue: Queue = Queue(maxsize=max_size)
        self.last_valid = {"image": None, "melt_pool_area": 0.0}

    def store_data(self, data: dict):
        if self.data_queue.full():
            try:
                self.data_queue.get_nowait()
            except Empty:
                pass
        self.data_queue.put(data)

    def retrieve_data(self):
        last = None
        try:
            while True:
                last = self.data_queue.get_nowait()
        except Empty:
            pass
        if last:
            self.last_valid = last
        return self.last_valid


class CameraCollector(threading.Thread):
    def __init__(self, camera, db, sample_rate=30, save_interval=1.0):
        super().__init__(daemon=True)
        self.camera = camera
        self.db = db
        self.running = True
        self.sample_rate = sample_rate
        self.save_interval = save_interval
        self.last_save = 0
        self.save_dir = None  # 저장 경로 (None이면 저장 안 함)
        self._lock = threading.Lock()

    def set_save_dir(self, save_dir: str):
        """이미지 저장 경로 설정 (공정 시작 시 호출)"""
        with self._lock:
            self.save_dir = save_dir
            if save_dir:
                os.makedirs(save_dir, exist_ok=True)
                print(f"[Basler] 이미지 저장 경로 설정: {save_dir}")
    
    def stop_saving(self):
        """이미지 저장 중지 (공정 종료 시 호출)"""
        with self._lock:
            self.save_dir = None
            print("[Basler] 이미지 저장 중지")

    def run(self):
        frame_count = 0
        error_count = 0
        while self.running:
            loop_start = time.perf_counter()
            frame = self.camera.get_data()
            
            if frame is not None:
                area = self.camera.calculate_melt_pool_area(frame, threshold=120)
                data = {"image": frame, "melt_pool_area": area}
                self.db.store_data(data)
                frame_count += 1
                error_count = 0  # 성공하면 에러 카운트 리셋
                
                # 100프레임마다 디버그 로그 출력
                if frame_count % 100 == 0:
                    print(f"[Basler DEBUG] 프레임 수집 중: {frame_count}개, 멜팅풀 면적: {area:.3f} mm²")
                
                # 이미지 저장 (save_dir이 설정되어 있을 때만, 1초 간격)
                with self._lock:
                    current_save_dir = self.save_dir
                
                if current_save_dir:
                    now = time.time()
                    if now - self.last_save >= self.save_interval:
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        filename = os.path.join(current_save_dir, f"basler_{timestamp}.png")
                        cv2.imwrite(filename, frame)
                        print(f"[Basler SAVE] {filename}")
                        self.last_save = now
            else:
                error_count += 1
                # 100번 연속 실패시 경고 출력
                if error_count % 100 == 0:
                    print(f"[Basler WARNING] 프레임 없음! 연속 {error_count}회 실패, 총 수집: {frame_count}개")

            sleep_time = max(0, (1/self.sample_rate) - (time.perf_counter() - loop_start))
            time.sleep(sleep_time)

    def stop(self):
        self.running = False
        try:
            self.camera.close()
        except Exception:
            pass