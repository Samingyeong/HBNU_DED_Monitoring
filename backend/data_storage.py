"""
데이터 스토리지 - 센서 데이터 저장 및 관리
기존 CSV 저장 로직을 백엔드로 이동
"""
import os
import csv
import json
import asyncio
import time
import threading
import shutil
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import deque
import cv2
import numpy as np

from .measurement_reader import MeasurementReader, get_measurement_reader


class DataStorage:
    """센서 데이터 저장 및 관리 클래스"""

    def __init__(self, max_history_size: int = 5000):
        self.max_history_size = max_history_size
        self.data_history = deque(maxlen=max_history_size)

        # ✅ main.py에서 bind_sensor_manager()로 주입받음
        self.sensor_manager = None

        # 저장 관련 상태
        self.is_saving = False
        self.current_save_path = None
        self.save_folder = None
        self.save_task = None

        # 임시 저장 관련 (자동저장 데이터 보관)
        self.temp_storage = deque(maxlen=10000)  # 최대 10,000개 데이터 보관
        self.temp_storage_start_time = None
        self.temp_storage_session_id = None
        self.temp_storage_cleanup_task = None
        self.temp_csv_path = None  # 자동저장 시 실시간 CSV 경로 (process_start에서 설정)

        # 이미지 저장 관련
        self.image_save_dir = None
        self.hik_save_dir = None
        self.frame_id = 0
        self.last_hik_save = 0

        # CSV 동시 쓰기 방지 및 실시간 flush용
        self._csv_lock = threading.Lock()

        # 데이터베이스 경로 설정
        # 최종 요구사항: C:\장비 모니터링 데이터\DED\M250_AM Solutions 경로를 직접 사용
        self.base_db_path = r"C:\장비 모니터링 데이터\DED\M250_AM Solutions"
        os.makedirs(self.base_db_path, exist_ok=True)

        # 이미지 저장 경로 설정
        self.images_path = os.path.join(os.path.dirname(__file__), "images")
        os.makedirs(self.images_path, exist_ok=True)

        # Measurement CSV 리더 (C:\DED\Measurement 연동)
        self.measurement_reader: MeasurementReader | None = None

    # ✅ __init__ 밖(클래스 레벨)에 있어야 함!
    def bind_sensor_manager(self, sensor_manager):
        """main.py에서 주입한 sensor_manager를 보관 (이미지 저장 등에서 사용 가능)"""
        self.sensor_manager = sensor_manager

    def bind_measurement_reader(self, reader: MeasurementReader):
        """main.py에서 주입한 MeasurementReader를 보관 (Measurement CSV 값 병합용)"""
        self.measurement_reader = reader

    def store_data(self, sensor_data: Dict[str, Any]):
        """센서 데이터를 히스토리에 저장"""
        try:
            # 데이터 정규화
            normalized_data = self._normalize_data(sensor_data)

            # 히스토리에 추가
            self.data_history.append(normalized_data)

            # 이미지 저장 처리 (저장 중일 때만; 불필요한 태스크·오류 방지)
            if self.is_saving:
                asyncio.create_task(self._save_images_async(normalized_data))

            # 저장 중이면 CSV에 추가 (수동: current_save_path / 자동: temp_csv_path) → 실시간 flush
            if (self.is_saving and self.save_folder) or (self.temp_storage_session_id and getattr(self, "temp_csv_path", None)):
                asyncio.create_task(self._save_to_csv_async(normalized_data))

            # 임시 저장 중이면 임시 스토리지에 추가
            if self.temp_storage_session_id:
                self.temp_storage.append(normalized_data)

        except Exception as e:
            print(f"❌ 데이터 저장 오류: {e}")

    def _normalize_data(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """센서 데이터를 정규화"""
        normalized = {
            "timestamp": sensor_data.get("timestamp", ""),
            "time_elapsed": 0.0,
            "curpos_x": None,
            "curpos_y": None,
            "curpos_z": None,
            "curpos_a": None,
            "curpos_c": None,
            "mpt": None,  # melt pool temperature
            "1ct": None,  # 1-color temperature
            "2ct": None,  # 2-color temperature
            "outpower": None,
            "setpower": None,
            "melt_pool_area": None,
            # Measurement Height (mm)
            "height_mm": None,
            # 가스 데이터 (GuiState.ini에서 읽음)
            "powder_gas": None,
            "coaxial_gas": None,
            "shield_gas": None,
            # 피더 RPM (Measurement / GuiState에서 읽음)
            "feeder1_rpm": None,
            "feeder2_rpm": None,
            "feeder3_rpm": None,
            "ccd_height_px_1": None,
            "ccd_height_px_2": None,
            "ccd_height_px_avg": None,
            "ccd_height_1_mm": None,
            "ccd_height_2_mm": None,
            "ccd_height_avg_mm": None,
            "image_available": False,
            "hik_image_available": False
        }

        # CNC 데이터 처리 (좌표 + 가스 데이터 포함)
        if sensor_data.get("cnc_data"):
            cnc_data = sensor_data["cnc_data"]
            normalized.update({
                "curpos_x": cnc_data.get("curpos_x"),
                "curpos_y": cnc_data.get("curpos_y"),
                "curpos_z": cnc_data.get("curpos_z"),
                "curpos_a": cnc_data.get("curpos_a"),
                "curpos_c": cnc_data.get("curpos_c"),
                # 가스 데이터 (GuiState.ini에서 병합됨)
                "powder_gas": cnc_data.get("powder_gas"),
                "coaxial_gas": cnc_data.get("coaxial_gas"),
                "shield_gas": cnc_data.get("shield_gas")
            })

        # 레이저 데이터 처리
        if sensor_data.get("laser_data"):
            laser_data = sensor_data["laser_data"]
            normalized.update({
                "outpower": laser_data.get("outpower"),
                "setpower": laser_data.get("setpower")
            })

        # Pyrometer 데이터 처리
        if sensor_data.get("pyrometer_data"):
            pyro_data = sensor_data["pyrometer_data"]
            normalized.update({
                "mpt": pyro_data.get("mpt"),
                "1ct": pyro_data.get("1ct"),
                "2ct": pyro_data.get("2ct")
            })

        # 카메라 데이터 처리 (sensor_manager에서 이미 변환된 데이터)
        if sensor_data.get("camera_data"):
            camera_data = sensor_data["camera_data"]
            normalized.update({
                "melt_pool_area": camera_data.get("melt_pool_area"),
                # sensor_manager에서 이미 image_available 필드로 변환됨
                "image_available": camera_data.get("image_available", False)
            })

        # HikRobot/CCD 카메라 데이터 처리
        if sensor_data.get("hik_camera_data"):
            hik_data = sensor_data["hik_camera_data"] or {}

            normalized["hik_image_available"] = hik_data.get(
                "hik_image_available",
                (hik_data.get("combined_image") is not None) or (hik_data.get("hik_image") is not None)
            )

            # ✅ CCD 높이 값 (Factory CCD가 넣어주는 키에서 읽기)
            h1 = hik_data.get("ccd_height_mm_1")
            h2 = hik_data.get("ccd_height_mm_2")
            havg = hik_data.get("ccd_height_mm_avg")

            if h1 is not None:
                normalized["ccd_height_1_mm"] = h1
            if h2 is not None:
                normalized["ccd_height_2_mm"] = h2
            if havg is not None:
                normalized["ccd_height_avg_mm"] = havg
            elif (h1 is not None) and (h2 is not None):
                try:
                    normalized["ccd_height_avg_mm"] = (float(h1) + float(h2)) / 2.0
                except Exception:
                    pass

        # Measurement CSV 값 병합 (C:\DED\Measurement)
        # - Time(dd_HH:mm:ss.fff) 기준 Measurement와 모니터링 timestamp를 시간으로 매칭
        # - powder/coaxial/shield 가스 + feeder1~3 RPM을 덮어씀
        if self.measurement_reader:
            ts_str = sensor_data.get("timestamp") or normalized.get("timestamp")
            if ts_str:
                try:
                    from datetime import datetime as _dt

                    # main.py collect_sensor_data에서 timestamp는 ISO 형식으로 생성됨
                    ts = _dt.fromisoformat(ts_str)
                    # Measurement CSV와 시간 오차를 조금 넉넉히 허용 (기본 2초)
                    mvals = self.measurement_reader.get_values_at(ts, max_delta_ms=2000)
                    if mvals:
                        # 높이 값 (Measurement Height) 덮어쓰기
                        if "height_mm" in mvals:
                            normalized["height_mm"] = mvals["height_mm"]

                        # 가스 값 덮어쓰기
                        if "powder_gas" in mvals:
                            normalized["powder_gas"] = mvals["powder_gas"]
                        if "coaxial_gas" in mvals:
                            normalized["coaxial_gas"] = mvals["coaxial_gas"]
                        if "shield_gas" in mvals:
                            normalized["shield_gas"] = mvals["shield_gas"]
                        # 피더 RPM 덮어쓰기
                        if "feeder1_rpm" in mvals:
                            normalized["feeder1_rpm"] = mvals["feeder1_rpm"]
                        if "feeder2_rpm" in mvals:
                            normalized["feeder2_rpm"] = mvals["feeder2_rpm"]
                        if "feeder3_rpm" in mvals:
                            normalized["feeder3_rpm"] = mvals["feeder3_rpm"]
                except Exception as _e:
                    # Measurement 연동 실패 시 전체 수집을 막지 않고 무시
                    print(f"⚠️ Measurement 병합 오류: {_e}")

        return normalized

    async def _save_images_async(self, data: Dict[str, Any]):
        """이미지 저장 (비동기). is_saving일 때만 store_data에서 호출됨."""
        try:
            # Basler 카메라 이미지 저장 (이미지·경로는 레거시 camera collector에서 직접 처리)
            outpower = data.get("outpower")
            try:
                outpower_ok = outpower is not None and float(outpower) > 10
            except (TypeError, ValueError):
                outpower_ok = False
            if data.get("image_available") and outpower_ok and self.image_save_dir:
                # Basler: sensor_manager.collectors["camera"]의 save_dir이 image_save_dir로 설정되어
                # 스레드 내부에서 1초마다 저장. 여기서는 별도 이미지 전달 없음.
                pass

            # HikRobot/CCD 이미지 저장 (1초마다)
            if (
                data.get("hik_image_available")
                and self.hik_save_dir
                and (time.time() - self.last_hik_save) >= 1.0
            ):
                self.last_hik_save = time.time()
                if self.sensor_manager:
                    ccd = getattr(self.sensor_manager, "_factory_sensors", {}).get("ccd_camera")
                    if ccd is not None and hasattr(ccd, "get_combined_image"):
                        img = ccd.get_combined_image()
                        if img is not None:
                            self.save_hik_image(img)
        except Exception as e:
            print(f"⚠️ 이미지 저장 오류: {e}")

    async def _save_to_csv_async(self, data: Dict[str, Any]):
        """CSV 파일에 데이터 저장 (비동기). 수동 저장·자동 저장 모두 실시간 flush."""
        try:
            path = self.current_save_path if self.is_saving else getattr(self, "temp_csv_path", None)
            if not path:
                return

            # CSV에 저장할 데이터 준비
            csv_data = {
                "timestamp": data["timestamp"],
                "curpos_x": data["curpos_x"],
                "curpos_y": data["curpos_y"],
                "curpos_z": data["curpos_z"],
                "curpos_a": data["curpos_a"],
                "curpos_c": data["curpos_c"],
                "mpt": data["mpt"],
                "melt_pool_area": data["melt_pool_area"],
                # Measurement Height (mm)
                "height_mm": data.get("height_mm"),
                "outpower": data["outpower"],
                "setpower": data["setpower"],
                # 가스 데이터 추가
                "powder_gas": data["powder_gas"],
                "coaxial_gas": data["coaxial_gas"],
                "shield_gas": data["shield_gas"],
                 # 피더 RPM 데이터 추가 (Measurement 연동)
                "feeder1_rpm": data.get("feeder1_rpm"),
                "feeder2_rpm": data.get("feeder2_rpm"),
                "feeder3_rpm": data.get("feeder3_rpm"),
            }

            # CSV 파일에 추가 (실시간 디스크 반영)
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._write_csv_row, path, csv_data)

        except Exception as e:
            print(f"⚠️ CSV 저장 오류: {e}")

    def _write_csv_row(self, filepath: str, data: Dict):
        """CSV 파일에 행 추가 (동기). flush+fsync로 실시간 디스크 반영, lock으로 동시 쓰기 방지."""
        try:
            with self._csv_lock:
                # 상위 폴더가 없으면 생성 (자동/수동 저장 모두 대비)
                parent = os.path.dirname(filepath)
                if parent:
                    os.makedirs(parent, exist_ok=True)
                file_exists = os.path.exists(filepath)
                with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
                    fieldnames = list(data.keys())
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(data)
                    csvfile.flush()  # Python 버퍼 → OS
                    try:
                        os.fsync(csvfile.fileno())  # OS 버퍼 → 디스크 (실시간으로 다른 프로그램에서 확인 가능)
                    except OSError:
                        pass  # 일부 환경에서 fsync 미지원 시 스킵
        except Exception as e:
            print(f"❌ CSV 쓰기 오류: {e}")

    # 과거: 내부 ASCII 경로 → 사용자 한글 경로로 미러링하던 기능은 제거 (직접 한글 경로 사용)

    async def start_saving(self, folder_name: str) -> str:
        """데이터 저장 시작

        folder_name으로 전달된 공정명을 사용해
        DB 폴더를 `YYMMDD_HHMMSS_공정명` 형식으로 생성한다.
        """
        if self.is_saving:
            raise Exception("이미 저장 중입니다")

        try:
            # 기본 타임스탬프 (YYMMDD_HHMMSS 형식)
            timestamp = datetime.now().strftime("%y%m%d_%H%M%S")

            # 공정명(폴더명) 정리: 공백 제거 + Windows 금지 문자만 치환
            # → 한글/비ASCII 문자는 그대로 두고, 경로에 사용할 수 없는 문자만 '_'로 변경
            safe_name = ""
            if folder_name:
                raw = str(folder_name).strip()
                if raw:
                    # Windows에서 사용할 수 없는 문자: \ / : * ? " < > |
                    invalid_chars = '\\/:*?"<>|'
                    table = str.maketrans({ch: "_" for ch in invalid_chars})
                    safe_name = raw.translate(table)

            # 최종 폴더 이름: YYMMDD_HHMMSS_공정명 (공정명이 없으면 기존처럼 타임스탬프만)
            if safe_name:
                folder_basename = f"{timestamp}_{safe_name}"
            else:
                folder_basename = timestamp

            self.save_folder = os.path.join(
                self.base_db_path,
                folder_basename
            )
            os.makedirs(self.save_folder, exist_ok=True)

            # Basler 이미지 저장 폴더: DB\YYMMDD_HHMMSS\image
            self.image_save_dir = os.path.join(self.save_folder, "image")
            os.makedirs(self.image_save_dir, exist_ok=True)

            # Hik 이미지 저장 경로는 그대로 메인 폴더 사용
            self.hik_save_dir = self.save_folder

            # CSV 파일 경로 설정 (DB\YYMMDD_HHMMSS_공정명\YYMMDD_HHMMSS_공정명.csv)
            self.current_save_path = os.path.join(
                self.save_folder,
                f"{folder_basename}.csv"
            )

            self.is_saving = True
            self.frame_id = 0
            self.last_hik_save = 0

            # 1시간마다 새 CSV 파일 생성하는 태스크 시작
            self.save_task = asyncio.create_task(self._csv_rotation_task())

            print(f"✅ 데이터 저장 시작: {self.save_folder}")
            return self.save_folder

        except Exception as e:
            self.is_saving = False
            raise Exception(f"저장 시작 실패: {str(e)}")

    async def stop_saving(self):
        """데이터 저장 중지"""
        if not self.is_saving:
            return

        try:
            self.is_saving = False

            # CSV 로테이션 태스크 정지
            if self.save_task:
                self.save_task.cancel()
                try:
                    await self.save_task
                except asyncio.CancelledError:
                    pass

            self.current_save_path = None
            self.save_folder = None
            self.image_save_dir = None
            self.hik_save_dir = None

            print("✅ 데이터 저장 중지 완료")

        except Exception as e:
            raise Exception(f"저장 중지 실패: {str(e)}")

    async def _csv_rotation_task(self):
        """1시간마다 새 CSV 파일 생성"""
        while self.is_saving:
            try:
                # 1시간 대기
                await asyncio.sleep(3600)

                if self.is_saving and self.save_folder:
                    # 새 CSV 파일 생성
                    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
                    self.current_save_path = os.path.join(
                        self.save_folder,
                        f"{timestamp}.csv"
                    )
                    print(f"📄 새 CSV 파일 생성: {self.current_save_path}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"⚠️ CSV 로테이션 오류: {e}")

    def get_latest_data(self) -> Optional[Dict[str, Any]]:
        """최신 데이터 조회"""
        if self.data_history:
            return dict(self.data_history[-1])
        return None

    def get_history_data(self, limit: int = 100) -> List[Dict[str, Any]]:
        """히스토리 데이터 조회"""
        if not self.data_history:
            return []

        # 최근 limit개 데이터 반환
        recent_data = list(self.data_history)[-limit:]
        return [dict(item) for item in recent_data]

    def save_camera_image(self, image: np.ndarray, power: float, area: float) -> Optional[str]:
        """Basler 카메라 이미지 저장"""
        if not self.image_save_dir or image is None:
            return None

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = os.path.join(
                self.image_save_dir,
                f"meltpool_{self.frame_id:05d}_{timestamp}.png"
            )
            cv2.imwrite(filename, image)
            self.frame_id += 1

            print(f"📸 Basler 이미지 저장: {filename} (Power={power:.1f}W, Area={area:.2f}mm²)")
            return filename

        except Exception as e:
            print(f"⚠️ Basler 이미지 저장 오류: {e}")
            return None

    def save_hik_image(self, combined_image: np.ndarray) -> Optional[str]:
        """HikRobot 합쳐진 이미지 저장"""
        if not self.hik_save_dir or combined_image is None:
            return None

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(
                self.hik_save_dir,
                f"hik_combined_{timestamp}.png"
            )
            cv2.imwrite(filename, combined_image)

            print(f"📹 HikRobot 이미지 저장: {filename}")
            return filename

        except Exception as e:
            print(f"⚠️ HikRobot 이미지 저장 오류: {e}")
            return None

    async def start_temp_storage(self, session_id: str):
        """임시 저장 시작 (자동저장 데이터 보관)"""
        try:
            self.temp_storage_session_id = session_id
            self.temp_storage_start_time = datetime.now()
            self.temp_storage.clear()  # 기존 임시 데이터 초기화

            # 30분 후 자동 정리 태스크 시작
            self.temp_storage_cleanup_task = asyncio.create_task(self._temp_storage_cleanup())

            print(f"📦 임시 저장 시작: {session_id}")

        except Exception as e:
            print(f"❌ 임시 저장 시작 실패: {e}")
            raise Exception(f"임시 저장 시작 실패: {str(e)}")

    async def stop_temp_storage(self):
        """임시 저장 중지"""
        try:
            if self.temp_storage_cleanup_task:
                self.temp_storage_cleanup_task.cancel()
                try:
                    await self.temp_storage_cleanup_task
                except asyncio.CancelledError:
                    pass

            self.temp_storage_session_id = None
            self.temp_storage_start_time = None
            self.temp_csv_path = None

            print("📦 임시 저장 중지 완료")

        except Exception as e:
            print(f"❌ 임시 저장 중지 실패: {e}")

    async def save_temp_storage_to_permanent(self, folder_name: str) -> str:
        """임시 저장된 데이터를 영구 저장으로 이동"""
        if not self.temp_storage_session_id or not self.temp_storage:
            raise Exception("저장할 임시 데이터가 없습니다")

        try:
            # 영구 저장 폴더 생성 (folder_name을 그대로 사용, 타임스탬프 추가 안 함)
            permanent_folder = os.path.join(self.base_db_path, folder_name)
            os.makedirs(permanent_folder, exist_ok=True)

            # 이미지 저장 폴더 생성
            image_save_dir = os.path.join(permanent_folder, "image")
            os.makedirs(image_save_dir, exist_ok=True)

            # CSV 파일 경로 설정 (folder_name 기준으로 파일명 생성)
            csv_path = os.path.join(permanent_folder, f"{folder_name}.csv")

            # 자동저장에서 실시간 CSV 기록 중이었으면 덮어쓰지 않음
            if getattr(self, "temp_csv_path", None) and os.path.normpath(csv_path) == os.path.normpath(self.temp_csv_path):
                print(f"✅ 임시 데이터 영구 저장 완료 (CSV 실시간 기록됨): {csv_path}")
                await self.stop_temp_storage()
                return permanent_folder

            # 임시 데이터를 CSV로 저장
            temp_data_list = list(self.temp_storage)
            if temp_data_list:
                # CSV 헤더 작성
                fieldnames = list(temp_data_list[0].keys())

                with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()

                    # 데이터 행들 작성
                    for data in temp_data_list:
                        writer.writerow(data)

                print(f"✅ 임시 데이터 영구 저장 완료: {csv_path} ({len(temp_data_list)}개 데이터)")

                # 🔄 자동저장 동안 생성된 Basler 이미지도 함께 복사
                try:
                    session_id = self.temp_storage_session_id
                    if session_id:
                        temp_image_dir = os.path.join(self.base_db_path, session_id, "image")
                        if os.path.isdir(temp_image_dir):
                            temp_files = [
                                f for f in os.listdir(temp_image_dir)
                                if os.path.isfile(os.path.join(temp_image_dir, f))
                            ]
                            copied = 0
                            for fname in temp_files:
                                src = os.path.join(temp_image_dir, fname)
                                dst = os.path.join(image_save_dir, fname)
                                # 동일 파일명은 덮어쓰지 않고 건너뜀
                                if not os.path.exists(dst):
                                    shutil.copy2(src, dst)
                                    copied += 1
                            print(f"📸 임시 이미지 {copied}개를 영구 폴더로 복사: {image_save_dir}")
                except Exception as img_e:
                    print(f"⚠️ 임시 이미지 복사 중 오류: {img_e}")

                # 임시 저장 중지
                await self.stop_temp_storage()

                return permanent_folder
            else:
                raise Exception("저장할 데이터가 없습니다")

        except Exception as e:
            print(f"❌ 임시 데이터 영구 저장 실패: {e}")
            raise Exception(f"임시 데이터 영구 저장 실패: {str(e)}")

    async def save_temp_storage_to_path(self, dest_path: str) -> str:
        """임시 저장 데이터를 사용자가 지정한 절대 경로에 저장"""
        if not self.temp_storage_session_id or not self.temp_storage:
            raise Exception("저장할 임시 데이터가 없습니다")

        try:
            # 대상 경로 정규화 및 폴더 생성
            dest_path = os.path.abspath(dest_path)
            os.makedirs(dest_path, exist_ok=True)

            # CSV 및 이미지 저장 경로 설정
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_path = os.path.join(dest_path, f"{timestamp}.csv")
            dest_image_dir = os.path.join(dest_path, "image")
            os.makedirs(dest_image_dir, exist_ok=True)

            temp_data_list = list(self.temp_storage)
            if temp_data_list:
                fieldnames = list(temp_data_list[0].keys())
                with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for data in temp_data_list:
                        writer.writerow(data)
                print(f"✅ 임시 데이터 사용자 경로로 저장 완료: {csv_path} ({len(temp_data_list)}개 데이터)")

                # 🔄 자동저장 동안 생성된 Basler 이미지도 함께 복사
                try:
                    session_id = self.temp_storage_session_id
                    if session_id:
                        temp_image_dir = os.path.join(self.base_db_path, session_id, "image")
                        if os.path.isdir(temp_image_dir):
                            temp_files = [
                                f for f in os.listdir(temp_image_dir)
                                if os.path.isfile(os.path.join(temp_image_dir, f))
                            ]
                            copied = 0
                            for fname in temp_files:
                                src = os.path.join(temp_image_dir, fname)
                                dst = os.path.join(dest_image_dir, fname)
                                if not os.path.exists(dst):
                                    shutil.copy2(src, dst)
                                    copied += 1
                            print(f"📸 임시 이미지 {copied}개를 사용자 경로로 복사: {dest_image_dir}")
                except Exception as img_e:
                    print(f"⚠️ 사용자 경로로 임시 이미지 복사 중 오류: {img_e}")

                # 임시 저장은 유지(자동저장 계속) — 요청 시에만 중지
                return dest_path
            else:
                raise Exception("저장할 데이터가 없습니다")
        except Exception as e:
            print(f"❌ 사용자 경로 저장 실패: {e}")
            raise Exception(f"사용자 경로 저장 실패: {str(e)}")

    async def _temp_storage_cleanup(self):
        """30분 후 임시 저장 데이터 자동 정리"""
        try:
            # 30분 대기
            await asyncio.sleep(1800)  # 30분 = 1800초

            if self.temp_storage_session_id:
                print(f"🧹 임시 저장 데이터 자동 정리: {self.temp_storage_session_id}")
                await self.stop_temp_storage()

        except asyncio.CancelledError:
            print("🧹 임시 저장 정리 태스크 취소됨")
        except Exception as e:
            print(f"❌ 임시 저장 정리 오류: {e}")

    def get_temp_storage_info(self) -> Dict[str, Any]:
        """임시 저장 정보 조회"""
        if not self.temp_storage_session_id:
            return {
                "has_temp_data": False,
                "session_id": None,
                "data_count": 0,
                "start_time": None,
                "remaining_time": 0
            }

        remaining_seconds = 0
        if self.temp_storage_start_time:
            elapsed = (datetime.now() - self.temp_storage_start_time).total_seconds()
            remaining_seconds = max(0, 1800 - elapsed)  # 30분 - 경과시간

        return {
            "has_temp_data": True,
            "session_id": self.temp_storage_session_id,
            "data_count": len(self.temp_storage),
            "start_time": self.temp_storage_start_time.isoformat() if self.temp_storage_start_time else None,
            "remaining_time": int(remaining_seconds)
        }