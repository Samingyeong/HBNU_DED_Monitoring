import ctypes
import os
import threading
import time

class OptrisCamera:
    def __init__(self, dll_path=None):
        self.connected = False
        self.running = False
        self.lock = threading.Lock()
        self.temperature_data = None

        # DLL 후보 경로 리스트
        candidate_paths = [
            r"C:/Program Files (x86)/Optris GmbH/PIX Connect/ImagerIPC2.dll",
            r"C:/Program Files (x86)/Optris/PI Connect/ImagerIPC2.dll"
        ]
        fallback_path = os.path.abspath("./vendor/optris/ImagerIPC2.dll")

        if dll_path:
            if not os.path.exists(dll_path):
                raise FileNotFoundError(f"[OptrisCamera] 제공된 DLL 경로가 존재하지 않음: {dll_path}")
        else:
            for path in candidate_paths:
                if os.path.exists(path):
                    dll_path = path
                    break
            else:
                if os.path.exists(fallback_path):
                    dll_path = fallback_path
                else:
                    raise FileNotFoundError(
                        "[OptrisCamera] DLL을 다음 경로들에서 찾을 수 없습니다:\n"
                        + "\n".join(candidate_paths + [fallback_path])
                    )

        try:
            self.dll = ctypes.WinDLL(dll_path)

            # 함수 시그니처 지정
            self.dll.InitImagerIPC.restype = ctypes.c_int
            self.dll.RunImagerIPC.restype = ctypes.c_int
            self.dll.GetVisibleFrame2.restype = ctypes.POINTER(ctypes.c_ushort)

            self.width = 382
            self.height = 288
            self.frame_size = self.width * self.height

            if self.dll.InitImagerIPC() != 1:
                raise RuntimeError("[OptrisCamera] InitImagerIPC 실패")

            if self.dll.RunImagerIPC() != 1:
                raise RuntimeError("[OptrisCamera] RunImagerIPC 실패")

            self.connected = True
            self.running = True
            self.thread = threading.Thread(target=self.capture_loop, daemon=True)
            self.thread.start()
            print(f"[OptrisCamera] 연결 성공 - DLL 경로: {dll_path}")

        except Exception as e:
            print("[OptrisCamera] DLL 로딩 중 예외:", e)
            self.connected = False


    def capture_loop(self):
        while self.running:
            try:
                raw_ptr = self.dll.GetVisibleFrame2()
                if bool(raw_ptr):
                    array_type = ctypes.c_ushort * self.frame_size
                    buffer = ctypes.cast(raw_ptr, ctypes.POINTER(array_type)).contents

                    center_index = (self.height // 2) * self.width + (self.width // 2)
                    center_temp = buffer[center_index]
                    max_temp = max(buffer)

                    with self.lock:
                        self.temperature_data = {
                            'center_temp': center_temp,
                            'max_temp': max_temp
                        }
                time.sleep(0.1)

            except Exception as e:
                print("[OptrisCamera] 캡처 루프 오류:", e)
                self.connected = False
                break

    def get_data(self):
        with self.lock:
            return self.temperature_data.copy() if self.temperature_data else None

    def stop(self):
        self.running = False
        print("[OptrisCamera] 수집 중지됨")
