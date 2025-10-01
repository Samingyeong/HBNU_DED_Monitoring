# Sensors/camera_comm.py
from pypylon import pylon
import cv2
import numpy as np
import time
import threading
from queue import Queue, Empty
import os

class CameraCommunication:
    def __init__(self):
        connected = False
        for i in range(3):
            try:
                self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
                self.camera.Open()
                self.cam_setting()
                print("Basler Camera Connected!")
                connected = True
                break
            except Exception as e:
                print(f"Connection attempt {i+1} failed. Error: {e}")
                time.sleep(1)

        if not connected:
            raise Exception("No device is available. Please check the camera connection.")

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

    def run(self):
        while self.running:
            loop_start = time.perf_counter()
            frame = self.camera.get_data()
            if frame is not None:
                area = self.camera.calculate_melt_pool_area(frame, threshold=120)
                data = {"image": frame, "melt_pool_area": area}
                self.db.store_data(data)

                now = time.time()
                if now - self.last_save >= self.save_interval:
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    folder = "captures_basler"
                    os.makedirs(folder, exist_ok=True)
                    filename = os.path.join(folder, f"basler_{timestamp}.png")
                    cv2.imwrite(filename, frame)
                    print(f"[Basler SAVE] {filename}")
                    self.last_save = now

            sleep_time = max(0, (1/self.sample_rate) - (time.perf_counter() - loop_start))
            time.sleep(sleep_time)

    def stop(self):
        self.running = False
        try:
            self.camera.close()
        except Exception:
            pass