"""
NC코드 파서 - NC코드 파일을 파싱하여 경로 정보 추출
"""
import os
import re
from typing import List, Dict, Optional, Tuple


class NCParser:
    """NC코드 파일 파싱 및 경로 추출"""
    
    def __init__(self):
        self.commands = []
        self.path_points = []
        self.current_position = {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
        
    def parse_folder(self, folder_path: str) -> Dict:
        """폴더 내의 모든 NC코드 파일을 파싱"""
        if not os.path.exists(folder_path):
            return {
                "success": False,
                "error": "폴더를 찾을 수 없습니다"
            }
        
        nc_files = []
        for file in os.listdir(folder_path):
            if file.lower().endswith(('.nc', '.txt', '.tap', '.cnc')):
                nc_files.append(os.path.join(folder_path, file))
        
        if not nc_files:
            return {
                "success": False,
                "error": "NC코드 파일을 찾을 수 없습니다"
            }
        
        # 첫 번째 파일 파싱
        result = self.parse_file(nc_files[0])
        result['total_files'] = len(nc_files)
        result['files'] = [os.path.basename(f) for f in nc_files]
        
        return result
    
    def parse_file(self, file_path: str) -> Dict:
        """단일 NC코드 파일 파싱"""
        try:
            # 다양한 인코딩으로 시도
            encodings = ['utf-8', 'cp949', 'euc-kr', 'latin-1']
            lines = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        lines = f.readlines()
                    break
                except UnicodeDecodeError:
                    continue
            
            if lines is None:
                return {
                    "success": False,
                    "error": "파일 인코딩을 읽을 수 없습니다"
                }
            
            return self._parse_lines(lines, file_path)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def parse_content(self, content: str) -> Dict:
        """NC코드 내용 직접 파싱 (웹 환경용)"""
        try:
            lines = content.split('\n')
            return self._parse_lines(lines, "uploaded_file")
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_lines(self, lines: List[str], file_name: str) -> Dict:
        """라인 리스트 파싱 공통 메서드"""
        self.commands = []
        self.path_points = []
        self.current_position = {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
        
        for line_num, line in enumerate(lines, 1):
            self._parse_line(line.strip(), line_num)
        
        # 경로 데이터 분석
        bounds = self._calculate_bounds()
        
        return {
            "success": True,
            "file_path": file_name,
            "file_name": os.path.basename(file_name) if file_name != "uploaded_file" else "업로드된 파일",
            "total_lines": len(lines),
            "total_points": len(self.path_points),
            "path_points": self.path_points,
            "bounds": bounds,
            "commands": self.commands[:100]  # 처음 100개 명령만 반환
        }
    
    def _parse_line(self, line: str, line_num: int):
        """단일 NC코드 라인 파싱"""
        # 주석 제거 (NC코드는 보통 () 또는 ; 사용)
        if '(' in line and ')' in line:
            line = re.sub(r'\([^)]*\)', '', line).strip()
        if ';' in line:
            line = line.split(';')[0].strip()
        
        if not line:
            return
        
        # G 명령어 추출 (NC코드에서 일반적인 이동 명령어)
        g_match = re.search(r'G(\d+(?:\.\d+)?)', line, re.IGNORECASE)
        if not g_match:
            # G 명령어가 없어도 좌표만 있는 경우 처리
            x = self._extract_coordinate(line, 'X')
            y = self._extract_coordinate(line, 'Y')
            z = self._extract_coordinate(line, 'Z')
            
            if x is not None or y is not None or z is not None:
                # 좌표가 있으면 현재 위치 업데이트
                if x is not None:
                    self.current_position['X'] = x
                if y is not None:
                    self.current_position['Y'] = y
                if z is not None:
                    self.current_position['Z'] = z
                
                # 경로 포인트 저장 (좌표가 있으면 이동으로 간주)
                point = {
                    'line': line_num,
                    'x': self.current_position['X'],
                    'y': self.current_position['Y'],
                    'z': self.current_position['Z'],
                    'type': 'move'
                }
                self.path_points.append(point)
                
                # 명령어 저장
                self.commands.append({
                    'line': line_num,
                    'code': 'MOVE',
                    'x': self.current_position['X'],
                    'y': self.current_position['Y'],
                    'z': self.current_position['Z']
                })
            return
        
        try:
            g_code = float(g_match.group(1))
        except ValueError:
            return
        
        # 이동 명령어 처리 (G0: 급속이동, G1: 절삭이동, G2/G3: 원호이동)
        if g_code not in [0, 1, 2, 3]:
            return
        
        # 좌표 추출
        x = self._extract_coordinate(line, 'X')
        y = self._extract_coordinate(line, 'Y')
        z = self._extract_coordinate(line, 'Z')
        
        # 좌표가 있으면 현재 위치 업데이트
        if x is not None:
            self.current_position['X'] = x
        if y is not None:
            self.current_position['Y'] = y
        if z is not None:
            self.current_position['Z'] = z
        
        # 경로 포인트 저장 (G1: 절삭 이동, G2/G3: 원호 이동)
        if g_code in [1, 2, 3]:
            point = {
                'line': line_num,
                'x': self.current_position['X'],
                'y': self.current_position['Y'],
                'z': self.current_position['Z'],
                'type': 'linear' if g_code == 1 else 'arc'
            }
            self.path_points.append(point)
        
        # 명령어 저장
        self.commands.append({
            'line': line_num,
            'code': f'G{g_code}',
            'x': self.current_position['X'],
            'y': self.current_position['Y'],
            'z': self.current_position['Z']
        })
    
    def _extract_coordinate(self, line: str, axis: str) -> Optional[float]:
        """라인에서 특정 축의 좌표 추출"""
        pattern = f'{axis}([+-]?\\d+\\.?\\d*)'
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None
    
    def _calculate_bounds(self) -> Dict:
        """경로의 경계값 계산"""
        if not self.path_points:
            return {
                'x_min': 0, 'x_max': 0,
                'y_min': 0, 'y_max': 0,
                'z_min': 0, 'z_max': 0
            }
        
        x_coords = [p['x'] for p in self.path_points]
        y_coords = [p['y'] for p in self.path_points]
        z_coords = [p['z'] for p in self.path_points]
        
        return {
            'x_min': min(x_coords),
            'x_max': max(x_coords),
            'y_min': min(y_coords),
            'y_max': max(y_coords),
            'z_min': min(z_coords),
            'z_max': max(z_coords),
            'x_range': max(x_coords) - min(x_coords),
            'y_range': max(y_coords) - min(y_coords),
            'z_range': max(z_coords) - min(z_coords)
        }
    
    def get_path_at_progress(self, progress_percent: float) -> List[Dict]:
        """진행률에 따른 경로 포인트 반환 (0-100)"""
        if not self.path_points:
            return []
        
        total_points = len(self.path_points)
        current_index = int(total_points * progress_percent / 100)
        
        return self.path_points[:current_index]
    
    def find_current_position_index(self, x: float, y: float, z: float, tolerance: float = 0.5) -> Optional[int]:
        """현재 좌표와 가장 가까운 경로 포인트의 인덱스 찾기"""
        min_distance = float('inf')
        closest_index = None
        
        for i, point in enumerate(self.path_points):
            # 3D 거리 계산
            distance = ((point['x'] - x) ** 2 + 
                       (point['y'] - y) ** 2 + 
                       (point['z'] - z) ** 2) ** 0.5
            
            if distance < min_distance and distance < tolerance:
                min_distance = distance
                closest_index = i
        
        return closest_index


# 전역 파서 인스턴스
nc_parser = NCParser()

