# ccd_camera.py
# ===== Hikrobot MVS SDK 경로 강제 등록 =====
import os
import sys

MVS_PY_DIR = r"C:\Program Files (x86)\MVS\Development\Samples\Python\MvImport"
MVS_DLL_DIR = r"C:\Program Files (x86)\MVS\Runtime\Win64_x64"

# Python 모듈 경로
if MVS_PY_DIR not in sys.path:
    sys.path.insert(0, MVS_PY_DIR)

# DLL 로딩 경로 (Python 3.8+ 필수)
try:
    os.add_dll_directory(MVS_PY_DIR)
except Exception:
    pass

if os.path.isdir(MVS_DLL_DIR):
    try:
        os.add_dll_directory(MVS_DLL_DIR)
    except Exception:
        pass
# =========================================

import sys
import logging
from ctypes import byref, c_ubyte, cast, POINTER

import numpy as np

from .base import BaseSensor
from .factory import register_sensor

logger = logging.getLogger("HBNU_Backend")

# ----------------------------
# Hikrobot SDK import 준비
# ----------------------------
# 예전 파일처럼 경로를 추가하던 방식 유지(필요 시 너희 환경에 맞게 수정)
# sys.path.append(r"C:\Program Files (x86)\MVS\Development\Samples\Python\MvImport")

MVS_AVAILABLE = False
try:
    from MvCameraControl_class import *
    from CameraParams_const import *
    from PixelType_header import *
    from MvErrorDefine_const import *
    MVS_AVAILABLE = True
except Exception as e:
    logger.warning(f"[CCDCamera] Hikrobot SDK import 실패: {e}")
    MVS_AVAILABLE = False


def _estimate_height_px(frame: np.ndarray) -> float | None:
    """
    melt pool 높이 추정 (픽셀 단위): 중앙 ROI 밝기 가중 y-센트로이드.
    - Mono8이면 그대로, BGR이면 그레이 변환
    - 캘리브레이션 전에는 경향성/상대값으로 사용 (mm 변환은 scale 적용)
    """
    if frame is None:
        return None
    if frame.ndim == 3:
        gray = (
            frame[:, :, 0].astype(np.float32) * 0.114
            + frame[:, :, 1].astype(np.float32) * 0.587
            + frame[:, :, 2].astype(np.float32) * 0.299
        )
    else:
        gray = frame.astype(np.float32)
    h, w = gray.shape[:2]
    x0, x1 = int(w * 0.35), int(w * 0.65)
    roi = gray[:, x0:x1]
    thr = np.percentile(roi, 95)
    mask = roi >= thr
    if mask.sum() < 50:
        return None
    ys = np.arange(h, dtype=np.float32)[:, None]
    weights = roi * mask
    s = weights.sum()
    if s <= 0:
        return None
    return float((ys * weights).sum() / s)


def _concat_side_by_side(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    """좌/우 결합. (해상도 다르면 높이 기준으로 pad)"""
    if img1 is None and img2 is None:
        return None
    if img1 is None:
        return img2
    if img2 is None:
        return img1

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    h = max(h1, h2)

    def pad_to_h(im, target_h):
        hh, ww = im.shape[:2]
        if hh == target_h:
            return im
        pad = target_h - hh
        if im.ndim == 2:
            return np.pad(im, ((0, pad), (0, 0)), mode="constant", constant_values=0)
        return np.pad(im, ((0, pad), (0, 0), (0, 0)), mode="constant", constant_values=0)

    img1p = pad_to_h(img1, h)
    img2p = pad_to_h(img2, h)
    return np.hstack((img1p, img2p))


class HikRobotCamera:
    """
    예전 vision_stream.py의 HikRobotStream 구조를 센서용으로 정리한 클래스
    - SerialNumber로 장치 탐색
    - MV_ACCESS_Monitor로 OpenDevice
    - Mono8 / BGR8_Packed 처리
    """
    def __init__(self, serial_number: str, buffer_bytes: int = 1920 * 1080 * 3):
        self.serial_number = serial_number
        self.cam = None
        self.connected = False
        self.frame_info = None
        self.data_buf = None
        self.buffer_bytes = buffer_bytes

    def open(self) -> bool:
        if not MVS_AVAILABLE:
            logger.error("[HikRobotCamera] MVS SDK 사용 불가")
            return False

        self.cam = MvCamera()
        self.frame_info = MV_FRAME_OUT_INFO_EX()

        deviceList = MV_CC_DEVICE_INFO_LIST()
        ret = MvCamera.MV_CC_EnumDevices(MV_GIGE_DEVICE | MV_USB_DEVICE, deviceList)
        if ret != 0 or deviceList.nDeviceNum == 0:
            logger.error(f"[HikRobotCamera] 장치 검색 실패 ret={ret}, n={deviceList.nDeviceNum}")
            return False

        target = None
        for i in range(deviceList.nDeviceNum):
            dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents

            # 예전 코드처럼 USB3VInfo에서 SN 읽기(현장 대부분 USB 카메라라 이게 잘 맞음)
            # GigE 모델이면 stGigEInfo 쪽을 추가로 읽어야 할 수도 있음
            try:
                sn = bytes(dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber).decode("utf-8").strip("\x00")
            except Exception:
                sn = ""

            if sn == self.serial_number:
                target = dev_info
                break

        if target is None:
            logger.error(f"[HikRobotCamera] SN={self.serial_number} 장치 못 찾음")
            return False

        ret = self.cam.MV_CC_CreateHandle(target)
        if ret != 0:
            logger.error(f"[HikRobotCamera] CreateHandle 실패 ret={ret}")
            return False

        # 예전 코드처럼 Monitor 모드로 Open
        ret = self.cam.MV_CC_OpenDevice(MV_ACCESS_Monitor, 0)
        if ret != 0:
            logger.error(f"[HikRobotCamera] OpenDevice 실패 ret={ret}")
            return False

        ret = self.cam.MV_CC_StartGrabbing()
        if ret != 0:
            logger.error(f"[HikRobotCamera] StartGrabbing 실패 ret={ret}")
            return False

        self.data_buf = (c_ubyte * self.buffer_bytes)()
        self.connected = True
        logger.info(f"[HikRobotCamera] 연결 성공 SN={self.serial_number} (Monitor 모드)")
        return True

    def close(self):
        if not self.cam:
            return
        try:
            try:
                self.cam.MV_CC_StopGrabbing()
            except Exception:
                pass
            try:
                self.cam.MV_CC_CloseDevice()
            except Exception:
                pass
            try:
                self.cam.MV_CC_DestroyHandle()
            except Exception:
                pass
        finally:
            self.cam = None
            self.connected = False
            self.data_buf = None
            self.frame_info = None

    def get_frame(self, timeout_ms: int = 1000):
        if not self.connected:
            return None

        ret = self.cam.MV_CC_GetOneFrameTimeout(
            byref(self.data_buf),
            len(self.data_buf),
            self.frame_info,
            timeout_ms
        )
        if ret != 0:
            return None

        w = int(self.frame_info.nWidth)
        h = int(self.frame_info.nHeight)

        # pixel type에 따라 reshape
        if self.frame_info.enPixelType == PixelType_Gvsp_Mono8:
            frame = np.frombuffer(self.data_buf, dtype=np.uint8, count=w * h)
            return frame.reshape((h, w)).copy()

        if self.frame_info.enPixelType == PixelType_Gvsp_BGR8_Packed:
            frame = np.frombuffer(self.data_buf, dtype=np.uint8, count=w * h * 3)
            return frame.reshape((h, w, 3)).copy()

        # 다른 포맷이면 우선 None 처리 (필요하면 ConvertPixelType 추가 가능)
        return None


@register_sensor("ccd_camera")
class CCDCameraSensor(BaseSensor):
    """
    Hikrobot CCD 2대 통합 센서

    반환 형태(기존 data_storage.py가 기대하는 형태에 맞춤):
    - hik_image_available: bool
    - combined_image: np.ndarray | None
    - image_1, image_2: np.ndarray | None  (디버깅용)
    """
    def __init__(self, config_path=None):
        super().__init__(config_path=config_path, name="Hikrobot CCD")

        # 여기 2개만 너희 실장비 SN으로 바꾸면 됨
        # (추후 config로 빼도 됨)
        self.serial_1 = "02J81094725"
        self.serial_2 = "02J75405689"
        self._height_mm_per_px = 1.0
        if config_path and os.path.isfile(config_path):
            try:
                import configparser
                cfg = configparser.ConfigParser()
                cfg.read(config_path, encoding="utf-8")
                if cfg.has_section("ccd_camera") and cfg.has_option("ccd_camera", "height_mm_per_px"):
                    self._height_mm_per_px = float(cfg.get("ccd_camera", "height_mm_per_px"))
            except Exception:
                pass

        self.cam1 = HikRobotCamera(self.serial_1)
        self.cam2 = HikRobotCamera(self.serial_2)

        self._last_combined = None

    def _do_connect(self):
        if not self.cam1.open():
            raise RuntimeError(f"CCD cam1 연결 실패 SN={self.serial_1}")
        if not self.cam2.open():
            raise RuntimeError(f"CCD cam2 연결 실패 SN={self.serial_2}")

    def _do_disconnect(self):
        self.cam1.close()
        self.cam2.close()
        self._last_combined = None

    def _do_get_data(self):
        f1 = self.cam1.get_frame()
        f2 = self.cam2.get_frame()

        available = (f1 is not None) and (f2 is not None)
        combined = _concat_side_by_side(f1, f2) if available else None

        if combined is not None:
            self._last_combined = combined

        # melt pool 높이 추정 (px 및 mm). mm = px * scale, scale=1.0(캘리브 전에는 상대값)
        scale = getattr(self, "_height_mm_per_px", 1.0)
        h1_px = _estimate_height_px(f1) if f1 is not None else None
        h2_px = _estimate_height_px(f2) if f2 is not None else None
        havg_px = None
        if h1_px is not None and h2_px is not None:
            havg_px = (h1_px + h2_px) / 2.0
        elif h1_px is not None:
            havg_px = h1_px
        elif h2_px is not None:
            havg_px = h2_px

        h1_mm = h1_px * scale if h1_px is not None else None
        h2_mm = h2_px * scale if h2_px is not None else None
        havg_mm = havg_px * scale if havg_px is not None else None

        return {
            "hik_image_available": bool(available),
            "image_1": f1,
            "image_2": f2,
            "combined_image": combined,
            "ccd_height_px_1": h1_px,
            "ccd_height_px_2": h2_px,
            "ccd_height_px_avg": havg_px,
            "ccd_height_mm_1": h1_mm,
            "ccd_height_mm_2": h2_mm,
            "ccd_height_mm_avg": havg_mm,
        }

    def get_combined_image(self):
        return self._last_combined
