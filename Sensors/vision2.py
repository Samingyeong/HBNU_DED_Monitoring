# vision2.py
import sys, os, time, threading
import cv2, numpy as np
from ctypes import *

SDK_PATH = r"C:\Program Files (x86)\MVS\Development\Samples\Python\MvImport"
if SDK_PATH not in sys.path:
    sys.path.append(SDK_PATH)

try:
    from MvCameraControl_class import *
    from CameraParams_const import *
    from PixelType_header import *
except ImportError as e:
    print("[ERROR] HikRobot SDK 모듈을 불러올 수 없습니다. SDK 경로 확인 필요:", e)
    raise e


class HikCameraThread(threading.Thread):
    def __init__(self, serial, on_new_frame=None, parent=None):
        super().__init__(daemon=True)
        self.serial = serial
        self.on_new_frame = on_new_frame
        self.running = True
        self.cam = MvCamera()
        self.parent = parent

    def run(self):
        deviceList = MV_CC_DEVICE_INFO_LIST()
        MvCamera.MV_CC_EnumDevices(MV_GIGE_DEVICE | MV_USB_DEVICE, deviceList)

        cam_info = None
        for i in range(deviceList.nDeviceNum):
            dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            raw = dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber
            s = "".join(chr(c) for c in raw if c != 0).strip()
            if self.serial == s:
                cam_info = dev_info
                break

        if cam_info is None:
            print(f"[{self.serial}] 카메라를 찾을 수 없습니다.")
            if self.parent: self.parent.hik_connected = False
            return

        if self.cam.MV_CC_CreateHandle(cam_info) != 0:
            print(f"[{self.serial}] 핸들 생성 실패.")
            if self.parent: self.parent.hik_connected = False
            return
        if self.cam.MV_CC_OpenDevice(MV_ACCESS_Control, 0) != 0:
            print(f"[{self.serial}] 장치 열기 실패.")
            if self.parent: self.parent.hik_connected = False
            return

        if self.parent:
            self.parent.hik_connected = True
            print(f"[{self.serial}] 카메라 연결 성공")

        self.cam.MV_CC_SetEnumValue("PixelFormat", PixelType_Gvsp_Mono8)
        self.cam.MV_CC_StartGrabbing()

        frame_info = MV_FRAME_OUT_INFO_EX()
        data_buf = (c_ubyte * (1920 * 1080))()

        while self.running:
            ret = self.cam.MV_CC_GetOneFrameTimeout(byref(data_buf), len(data_buf), frame_info, 1000)
            if ret == 0:
                img = np.frombuffer(data_buf, dtype=np.uint8, count=frame_info.nFrameLen)
                img = img.reshape(frame_info.nHeight, frame_info.nWidth)

                if self.on_new_frame:
                    self.on_new_frame(img)

        self.cam.MV_CC_StopGrabbing()
        self.cam.MV_CC_CloseDevice()
        self.cam.MV_CC_DestroyHandle()

        if self.parent:
            self.parent.hik_connected = False
            print(f"[{self.serial}] 카메라 연결 종료")

    def stop(self):
        self.running = False