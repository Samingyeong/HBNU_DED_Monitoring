"""
카메라 센서 (Basler Camera)
===========================

역할:
- Basler 카메라 연결 및 이미지 수집
- 멜트풀 면적 계산

통신 방식:
- pypylon 라이브러리 (Pylon SDK)
"""
import os
import sys
import logging
from typing import Dict, Any, Optional

import cv2
import numpy as np

from .base import BaseSensor
from .factory import register_sensor

logger = logging.getLogger("HBNU_Backend")

# pypylon 임포트 (선택적)
try:
    from pypylon import pylon
    PYLON_AVAILABLE = True
except ImportError:
    PYLON_AVAILABLE = False
    logger.warning("pypylon 모듈을 찾을 수 없습니다. 카메라 기능이 비활성화됩니다.")


@register_sensor('camera')
class CameraSensor(BaseSensor):
    """
    Basler 카메라 센서
    
    기능:
    - 카메라 연결/해제
    - 이미지 수집
    - 멜트풀 면적 계산
    """
    
    # 기본 카메라 설정
    DEFAULT_EXPOSURE = 400
    DEFAULT_WIDTH = 720
    DEFAULT_HEIGHT = 520
    FOV_WIDTH_MM = 5.13
    FOV_HEIGHT_MM = 4.10
    
    def __init__(self, config_path: Optional[str] = None):
        super().__init__(config_path=config_path, name="Basler Camera")
        
        self._camera = None
        self._pixel_size = (self.FOV_WIDTH_MM * self.FOV_HEIGHT_MM) / (
            self.DEFAULT_WIDTH * self.DEFAULT_HEIGHT
        )
    
    def _do_connect(self) -> None:
        """Basler 카메라 연결"""
        if not PYLON_AVAILABLE:
            raise RuntimeError("pypylon 모듈이 설치되지 않았습니다")
        
        # 연결 시도 (최대 3회)
        for attempt in range(3):
            try:
                self._camera = pylon.InstantCamera(
                    pylon.TlFactory.GetInstance().CreateFirstDevice()
                )
                self._camera.Open()
                self._configure_camera()
                
                # 픽셀 포맷 설정
                try:
                    pf = self._camera.PixelFormat
                    if "Mono8" in pf.Symbolics:
                        pf.SetValue("Mono8")
                except Exception:
                    pass
                
                # 이미지 수집 시작
                self._camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                
                logger.info(f"[{self._name}] 연결 성공 (시도 {attempt + 1})")
                return
                
            except Exception as e:
                logger.warning(f"[{self._name}] 연결 시도 {attempt + 1} 실패: {e}")
                if attempt < 2:
                    import time
                    time.sleep(1)
        
        raise RuntimeError("카메라 연결 실패 (3회 시도)")
    
    def _configure_camera(self, exposure: int = None, width: int = None, 
                          height: int = None) -> None:
        """카메라 설정"""
        if self._camera is None:
            return
        
        exposure = exposure or self.DEFAULT_EXPOSURE
        width = width or self.DEFAULT_WIDTH
        height = height or self.DEFAULT_HEIGHT
        
        self._camera.ExposureTime.SetValue(exposure)
        self._camera.Width.SetValue(width)
        self._camera.Height.SetValue(height)
    
    def _do_disconnect(self) -> None:
        """카메라 연결 해제"""
        if self._camera is not None:
            if self._camera.IsGrabbing():
                self._camera.StopGrabbing()
            self._camera.Close()
            self._camera = None
    
    def _do_get_data(self) -> Dict[str, Any]:
        """이미지 수집 및 멜트풀 면적 계산"""
        if self._camera is None or not self._camera.IsGrabbing():
            return {"image": None, "melt_pool_area": 0.0}
        
        try:
            grab_result = self._camera.RetrieveResult(
                1000, pylon.TimeoutHandling_ThrowException
            )
            
            if grab_result.GrabSucceeded():
                image = grab_result.Array.copy()
                grab_result.Release()
                
                # 멜트풀 면적 계산
                melt_pool_area = self._calculate_melt_pool_area(image)
                
                return {
                    "image": image,
                    "melt_pool_area": melt_pool_area
                }
            
            grab_result.Release()
            
        except Exception as e:
            logger.warning(f"[{self._name}] 이미지 수집 오류: {e}")
        
        return {"image": None, "melt_pool_area": 0.0}
    
    def _calculate_melt_pool_area(self, image: np.ndarray, 
                                   threshold: int = 120) -> float:
        """
        멜트풀 면적 계산
        
        Args:
            image: 그레이스케일 이미지
            threshold: 이진화 임계값
            
        Returns:
            float: 멜트풀 면적 (mm²)
        """
        if image is None:
            return 0.0
        
        _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        pixel_count = np.sum(binary == 255)
        area = pixel_count * self._pixel_size
        
        return round(area, 3)
    
    def get_image(self) -> Optional[np.ndarray]:
        """이미지만 반환"""
        data = self.get_data()
        return data.get("image") if data else None
