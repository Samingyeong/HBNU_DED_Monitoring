"""
Measurement CSV 리더
====================

역할:
- C:\DED\Measurement (또는 D:\DED\Measurement) 폴더에서 가장 최근 CSV 파일을 찾고
- Time(dd_HH:mm:ss.fff) 컬럼을 실제 datetime으로 변환한 뒤
- 주어진 시각에 가장 가까운 행의 가스/피더 데이터를 반환

주의:
- Measurement CSV의 Time 형식: 예) 21_17:46:19.798
  → 파일 수정시간의 (year, month) + day=21, time=17:46:19.798 으로 보정
"""

import os
import csv
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any

from logging import getLogger

logger = getLogger(__name__)


@dataclass
class MeasurementRecord:
    """Measurement CSV 한 행의 데이터"""
    timestamp: datetime
    height_mm: float
    powder_gas: float
    coaxial_gas: float
    shield_gas: float
    feeder1_rpm: int
    feeder2_rpm: int
    feeder3_rpm: int


class MeasurementReader:
    """
    Measurement CSV 리더

    - Measurement 폴더에서 가장 최근 CSV 파일 자동 감지
    - 파일 변경 시 다시 로드
    - 주어진 시각에 가장 가까운 레코드의 값을 반환
    """

    MEASUREMENT_FOLDERS = [
        r"C:\DED\Measurement",
        r"D:\DED\Measurement",
    ]

    def __init__(self):
        self._lock = threading.Lock()
        self._current_file: Optional[str] = None
        self._current_mtime: float = 0.0
        self._records: List[MeasurementRecord] = []

    # -------------------------------
    # 공개 API
    # -------------------------------
    def get_values_at(self, ts: datetime, max_delta_ms: int = 500) -> Optional[Dict[str, Any]]:
        """
        주어진 시각(ts)에 가장 가까운 Measurement 값 반환.

        Args:
            ts: 기준 시각 (모니터링 데이터 timestamp)
            max_delta_ms: 허용 최대 시간 차이 (밀리초). 이보다 크면 None 반환.
        """
        try:
            self._ensure_latest_loaded()
        except Exception as e:
            logger.warning(f"Measurement 파일 로드 실패: {e}")
            return None

        with self._lock:
            if not self._records:
                return None

            # 가장 가까운 레코드 찾기 (간단한 선형 탐색; 파일이 매우 크면 최적화 가능)
            best_rec: Optional[MeasurementRecord] = None
            best_delta_ms: float = float("inf")

            for rec in self._records:
                delta_ms = abs((rec.timestamp - ts).total_seconds() * 1000.0)
                if delta_ms < best_delta_ms:
                    best_delta_ms = delta_ms
                    best_rec = rec

            if best_rec is None or best_delta_ms > max_delta_ms:
                return None

            return {
                "height_mm": best_rec.height_mm,
                "powder_gas": best_rec.powder_gas,
                "coaxial_gas": best_rec.coaxial_gas,
                "shield_gas": best_rec.shield_gas,
                "feeder1_rpm": best_rec.feeder1_rpm,
                "feeder2_rpm": best_rec.feeder2_rpm,
                "feeder3_rpm": best_rec.feeder3_rpm,
            }

    # -------------------------------
    # 내부 유틸
    # -------------------------------
    def _ensure_latest_loaded(self):
        """Measurement 폴더에서 가장 최근 CSV를 찾아 필요시 다시 로드"""
        latest_file, latest_mtime = self._find_latest_file()
        if not latest_file:
            return

        with self._lock:
            if (
                latest_file == self._current_file
                and abs(latest_mtime - self._current_mtime) < 1e-3
            ):
                # 파일 변경 없음
                return

            # 새 파일 또는 변경된 파일 로드
            self._current_file = latest_file
            self._current_mtime = latest_mtime
            self._records = self._load_file(latest_file)

            logger.info(
                f"✅ Measurement CSV 로드: {latest_file} (records={len(self._records)})"
            )

    def _find_latest_file(self) -> (Optional[str], float):
        """
        Measurement 폴더에서 가장 최근 **타임시리즈 Measurement CSV** 파일 찾기
        (헤더에 Time(dd_HH:mm:ss.fff) 같은 Time 컬럼이 있는 파일만 대상)
        """
        latest_file: Optional[str] = None
        latest_mtime: float = 0.0

        for folder in self.MEASUREMENT_FOLDERS:
            if not os.path.exists(folder):
                continue

            try:
                for fname in os.listdir(folder):
                    if not fname.lower().endswith(".csv"):
                        continue
                    path = os.path.join(folder, fname)
                    # 헤더에 Time 컬럼이 없는 설정용 CSV (예: Content,Usage,Value 형식) 은 제외
                    try:
                        if not self._has_time_column(path):
                            continue
                        mtime = os.path.getmtime(path)
                    except OSError:
                        continue
                    if mtime > latest_mtime:
                        latest_mtime = mtime
                        latest_file = path
            except OSError:
                continue

        return latest_file, latest_mtime

    def _has_time_column(self, path: str) -> bool:
        """
        파일 앞부분의 여러 줄 중에서 Time(dd_HH:mm:ss.fff) 같은 Time 컬럼이 있는지 확인.
        - Content,Usage,Value 형식 설정 CSV는 여기서 필터링됨.
        - 일부 Measurement CSV는 10~20행 이후에 Time 헤더가 등장할 수 있으므로 최대 50행까지 검사.
        """
        encodings = ["utf-8-sig", "cp949", "euc-kr", "latin-1"]

        for enc in encodings:
            try:
                with open(path, "r", encoding=enc, newline="") as f:
                    reader = csv.reader(f)
                    for _ in range(50):  # 앞에서 최대 50행까지 검사
                        row = next(reader, None)
                        if row is None:
                            break
                        for col in row:
                            s = (col or "").strip().lower().lstrip("\ufeff")
                            # 예시: "time(dd_hh:mm:ss.fff)"
                            if s.startswith("time(") or s.startswith("time(dd_") or "time(dd_" in s:
                                return True
                break
            except Exception:
                continue

        return False

    def _load_file(self, path: str) -> List[MeasurementRecord]:
        """CSV 파일을 읽어 MeasurementRecord 리스트로 변환"""
        records: List[MeasurementRecord] = []

        # 파일 mtime에서 year, month 추출 (day/time은 CSV Time컬럼에서)
        try:
            mtime_dt = datetime.fromtimestamp(os.path.getmtime(path))
            base_year = mtime_dt.year
            base_month = mtime_dt.month
        except Exception:
            now = datetime.now()
            base_year = now.year
            base_month = now.month

        # 다양한 인코딩 시도
        encodings = ["utf-8-sig", "cp949", "euc-kr", "latin-1"]
        last_error: Optional[Exception] = None

        for enc in encodings:
            try:
                with open(path, "r", encoding=enc, newline="") as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                last_error = None
                break
            except Exception as e:
                last_error = e
                continue

        if last_error is not None:
            raise last_error

        if not rows:
            return records

        # 실제 Time 헤더가 파일 중간(예: 17행)에 있을 수 있으므로,
        # rows에서 Time 컬럼을 포함한 행을 찾아 그 행을 header로 사용
        header: Optional[List[str]] = None
        header_index: int = 0

        def row_has_time(r: List[str]) -> bool:
            for col in r:
                s = (col or "").strip().lower().lstrip("\ufeff")
                if s.startswith("time(") or s.startswith("time(dd_") or "time(dd_" in s:
                    return True
            return False

        for idx, r in enumerate(rows):
            if row_has_time(r):
                header = r
                header_index = idx
                break

        if header is None:
            logger.warning(f"Measurement CSV에서 Time 헤더 행을 찾지 못했습니다: {path}")
            return records

        # 헤더 인덱스 찾기 (부분 문자열/소문자 매칭으로 유연하게)
        def find_col(predicate) -> Optional[int]:
            for i, col in enumerate(header):
                low = (col or "").strip().lower().lstrip("\ufeff")
                if predicate(low):
                    return i
            return None

        # Time(dd_HH:mm:ss.fff) 컬럼 찾기 (BOM/대소문자 변형 등을 폭넓게 허용)
        time_idx = find_col(lambda s: s.startswith("time(") or s.startswith("time(dd_") or "time(dd_" in s)
        height_idx = find_col(lambda s: "height(" in s and "mm" in s)
        powder_idx = find_col(lambda s: "poweder gas" in s or "powder gas" in s)
        coax_idx = find_col(lambda s: "coaxial gas" in s)
        shield_idx = find_col(lambda s: "shield gas" in s)

        feeder1_idx = find_col(lambda s: s == "feeder1")
        feeder2_idx = find_col(lambda s: s == "feeder2")
        feeder3_idx = find_col(lambda s: s == "feeder3")

        if time_idx is None:
            # _find_latest_file에서 이미 Time 컬럼이 있는 파일만 골라오므로
            # 여기에 오면 헤더 형식이 약간 다른 특수 케이스일 뿐, 경고만 남기고 빈 리스트 반환
            logger.warning(f"Measurement CSV에 Time 컬럼을 찾지 못했습니다(헤더 형식 확인 필요): {path}")
            return records

        # 헤더 다음 행부터 실제 데이터
        for row in rows[header_index + 1:]:
            if not row or len(row) <= time_idx:
                continue

            try:
                time_str = row[time_idx].strip()
                ts = self._parse_time(time_str, base_year, base_month)
            except Exception:
                continue

            def get_float(idx: Optional[int], default: float = 0.0) -> float:
                if idx is None or idx >= len(row):
                    return default
                try:
                    return float(row[idx])
                except Exception:
                    return default

            def get_int(idx: Optional[int], default: int = 0) -> int:
                if idx is None or idx >= len(row):
                    return default
                try:
                    return int(float(row[idx]))
                except Exception:
                    return default

            rec = MeasurementRecord(
                timestamp=ts,
                height_mm=get_float(height_idx, 0.0),
                powder_gas=get_float(powder_idx, 0.0),
                coaxial_gas=get_float(coax_idx, 0.0),
                shield_gas=get_float(shield_idx, 0.0),
                feeder1_rpm=get_int(feeder1_idx, 0),
                feeder2_rpm=get_int(feeder2_idx, 0),
                feeder3_rpm=get_int(feeder3_idx, 0),
            )
            records.append(rec)

        # timestamp 기준으로 정렬 (보통은 이미 정렬되어 있지만 방어 차원)
        records.sort(key=lambda r: r.timestamp)
        return records

    @staticmethod
    def _parse_time(time_str: str, year: int, month: int) -> datetime:
        """
        Time(dd_HH:mm:ss.fff) 형식 파싱
        예: '21_17:46:19.798' → day=21, time=17:46:19.798
        """
        time_str = time_str.strip()
        if not time_str:
            raise ValueError("empty time string")

        # 'dd_HH:mm:ss.fff' 또는 'dd_HH:mm:ss' 형태 가정
        if "_" not in time_str:
            raise ValueError(f"unexpected time format: {time_str}")

        day_part, hms_part = time_str.split("_", 1)
        day = int(day_part)

        # ms 유무에 따라 포맷 결정
        if "." in hms_part:
            dt_time = datetime.strptime(hms_part, "%H:%M:%S.%f")
        else:
            dt_time = datetime.strptime(hms_part, "%H:%M:%S")

        return datetime(
            year,
            month,
            day,
            dt_time.hour,
            dt_time.minute,
            dt_time.second,
            dt_time.microsecond,
        )


# 전역 인스턴스 (lazy singleton)
_measurement_reader: Optional[MeasurementReader] = None


def get_measurement_reader() -> MeasurementReader:
    """전역 Measurement 리더 가져오기"""
    global _measurement_reader
    if _measurement_reader is None:
        _measurement_reader = MeasurementReader()
    return _measurement_reader

