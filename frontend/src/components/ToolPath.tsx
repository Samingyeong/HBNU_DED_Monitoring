/**
 * ToolPath 시각화 컴포넌트 - 2D Canvas를 사용한 경로 표시
 * NC코드 파일 업로드 → 백엔드에서 파싱 및 진행률 계산 → 프론트에서 시각화만
 */
import React, { useEffect, useRef, useState, useCallback } from 'react';
import axios from 'axios';

interface ToolPathProps {
  className?: string;
}

interface UploadStatus {
  isUploading: boolean;
  fileName: string | null;
  error: string | null;
}

interface PathPoint {
  x: number;
  y: number;
  z: number;
  line: number;
  type: string;
}

interface NCPathData {
  success?: boolean;
  path_points: PathPoint[];
  bounds: {
    x_min: number;
    x_max: number;
    y_min: number;
    y_max: number;
    z_min: number;
    z_max: number;
    x_range: number;
    y_range: number;
    z_range: number;
  };
  total_points: number;
}

// 백엔드에서 받는 진행률 데이터
interface ProgressData {
  success: boolean;
  has_nc_data: boolean;
  has_cnc_data?: boolean;
  progress: number;
  current_index: number;
  total_points: number;
  current_position: {
    x: number;
    y: number;
    z: number;
  };
  total_distance: number;
  remaining_distance: number;
}

const ToolPath: React.FC<ToolPathProps> = ({ className }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [ncData, setNcData] = useState<NCPathData | null>(null);
  const [progressData, setProgressData] = useState<ProgressData | null>(null);
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>({
    isUploading: false,
    fileName: null,
    error: null
  });

  // NC코드 파일 업로드 핸들러
  const handleFileUpload = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploadStatus({ isUploading: true, fileName: file.name, error: null });

    try {
      const formData = new FormData();
      formData.append('file', file);

      console.log('📤 NC코드 파일 업로드 시작:', file.name);
      
      const response = await axios.post('http://127.0.0.1:8000/api/nc/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('✅ NC코드 업로드 성공:', response.data);
      
      // 업로드 성공 후 경로 데이터 로드
      const pathResponse = await axios.get('http://127.0.0.1:8000/api/nc/path');
      console.log('📊 NC경로 데이터 수신:', pathResponse.data);
      
      // 데이터 유효성 검증
      if (pathResponse.data?.path_points && pathResponse.data.path_points.length > 0) {
        console.log(`✅ 경로 포인트 ${pathResponse.data.path_points.length}개 로드됨`);
        console.log('📍 첫 번째 포인트:', pathResponse.data.path_points[0]);
        console.log('📍 마지막 포인트:', pathResponse.data.path_points[pathResponse.data.path_points.length - 1]);
        setNcData(pathResponse.data);
      } else {
        console.error('❌ 경로 포인트가 비어있음!', pathResponse.data);
        setUploadStatus({ 
          isUploading: false, 
          fileName: null, 
          error: 'NC 파일에서 경로를 추출할 수 없습니다' 
        });
        return;
      }
      
      setUploadStatus({ 
        isUploading: false, 
        fileName: file.name, 
        error: null 
      });
    } catch (error: any) {
      console.error('❌ NC코드 업로드 실패:', error);
      setUploadStatus({ 
        isUploading: false, 
        fileName: null, 
        error: error.response?.data?.detail || '파일 업로드에 실패했습니다' 
      });
    }

    // 파일 입력 초기화 (같은 파일 다시 선택 가능하도록)
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, []);

  // NC코드 데이터 초기화 핸들러
  const handleClearData = useCallback(async () => {
    try {
      await axios.delete('http://127.0.0.1:8000/api/nc/clear');
      setNcData(null);
      setProgressData(null);
      setUploadStatus({ isUploading: false, fileName: null, error: null });
      console.log('🗑️ NC코드 데이터 초기화됨');
    } catch (error) {
      console.error('NC코드 데이터 초기화 실패:', error);
    }
  }, []);

  // 앱 시작 시 서버에 NC 데이터가 있는지 확인
  useEffect(() => {
    const checkExistingData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/nc/path');
        console.log('[ToolPath] 초기 NC 데이터 확인:', response.data);
        
        // has_data 필드 확인 (데이터가 없으면 null로 설정)
        if (response.data?.has_data === false) {
          console.log('[ToolPath] NC코드 데이터 없음 - 파일 업로드 대기');
          setNcData(null);
        } else if (response.data?.path_points && response.data.path_points.length > 0) {
          console.log(`[ToolPath] ✅ 기존 NC 데이터 발견: ${response.data.path_points.length}개 포인트`);
          setNcData(response.data);
        } else {
          console.log('[ToolPath] NC 데이터 있지만 경로 포인트 없음');
          setNcData(null);
        }
      } catch (error: any) {
        console.log('[ToolPath] NC코드 데이터 조회 실패:', error.message);
        setNcData(null);
      }
    };

    checkExistingData();
  }, []);

  // 백엔드에서 진행률 데이터 주기적 조회 (500ms 간격)
  useEffect(() => {
    if (!ncData) return;

    const fetchProgress = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/nc/progress');
        setProgressData(response.data);
      } catch (error) {
        console.error('진행률 조회 실패:', error);
      }
    };

    // 초기 로드
    fetchProgress();

    // 500ms 간격으로 진행률 업데이트
    const interval = setInterval(fetchProgress, 500);

    return () => clearInterval(interval);
  }, [ncData]);

  // Canvas 렌더링 (시각화만 담당, 계산은 백엔드에서)
  useEffect(() => {
    console.log('[ToolPath Canvas] 렌더링 시작, ncData:', ncData ? `${ncData.path_points?.length || 0}개 포인트` : 'null');
    
    if (!canvasRef.current || !ncData) {
      console.log('[ToolPath Canvas] 렌더링 스킵 - canvasRef:', !!canvasRef.current, 'ncData:', !!ncData);
      return;
    }

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      console.error('[ToolPath Canvas] 2D 컨텍스트 생성 실패');
      return;
    }

    // Canvas 크기 설정 (고정 크기로 설정하여 크기 변화 방지)
    const FIXED_SIZE = 300;  // 고정 크기
    if (canvas.width !== FIXED_SIZE || canvas.height !== FIXED_SIZE) {
      canvas.width = FIXED_SIZE;
      canvas.height = FIXED_SIZE;
      console.log('[ToolPath Canvas] 캔버스 크기 고정:', FIXED_SIZE, 'x', FIXED_SIZE);
    }

    // 배경 초기화
    ctx.fillStyle = '#f9fafb';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const { bounds, path_points } = ncData;
    
    if (!path_points || path_points.length === 0) {
      console.warn('[ToolPath Canvas] 경로 포인트가 비어있음!');
      ctx.fillStyle = '#666';
      ctx.font = '14px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('경로 데이터 없음', canvas.width / 2, canvas.height / 2);
      return;
    }
    
    console.log('[ToolPath Canvas] 경로 그리기 시작:', path_points.length, '개 포인트');
    console.log('[ToolPath Canvas] bounds:', bounds);

    // 좌표 변환 함수 (NC코드 좌표 → Canvas 좌표)
    const padding = 25;
    // 범위가 0이거나 음수인 경우를 방지
    const xRange = Math.max(bounds.x_range || 1, 0.001);
    const yRange = Math.max(bounds.y_range || 1, 0.001);
    const scaleX = (canvas.width - 2 * padding) / xRange;
    const scaleY = (canvas.height - 2 * padding) / yRange;
    const scale = Math.min(scaleX, scaleY);

    const toCanvasX = (x: number) => padding + (x - bounds.x_min) * scale;
    const toCanvasY = (y: number) => canvas.height - padding - (y - bounds.y_min) * scale;

    // 백엔드에서 받은 진행률 데이터 사용
    const currentIndex = progressData?.current_index || 0;
    const currentX = progressData?.current_position?.x || path_points[0]?.x || 0;
    const currentY = progressData?.current_position?.y || path_points[0]?.y || 0;
    const currentZ =
      progressData?.current_position?.z ??
      path_points[Math.min(currentIndex, path_points.length - 1)]?.z ??
      path_points[0]?.z ??
      0;
    const progress = progressData?.progress || 0;
    const totalDistance = progressData?.total_distance || 0;
    const remainingDistance = progressData?.remaining_distance || 0;

    // 전체 경로를 빨간 점선으로 먼저 그리기 (모든 레이어 공통 베이스 경로)
    ctx.strokeStyle = '#ef4444';  // 빨간색
    ctx.setLineDash([4, 4]);  // 점선
    ctx.lineWidth = 1.5;
    
    for (let i = 0; i < path_points.length - 1; i++) {
      const p1 = path_points[i];
      const p2 = path_points[i + 1];
      const x1 = toCanvasX(p1.x);
      const y1 = toCanvasY(p1.y);
      const x2 = toCanvasX(p2.x);
      const y2 = toCanvasY(p2.y);
      
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
    }
    
    // 헤드가 실제로 지나간 "현재 레이어(Z)"의 경로만 빨간 실선으로 덮어그리기
    // → currentIndex가 0일 때(아직 적층 시작 전)에는 실선이 나오지 않도록 함
    // → Z가 다른 레이어의 경로는 계속 점선으로만 남게 함
    if (currentIndex > 0 && path_points.length > 1) {
      const lastIndex = Math.min(currentIndex, path_points.length - 1);
      const layerTolerance =
        bounds.z_range > 0 ? Math.max(bounds.z_range * 0.01, 0.05) : 0.05; // 전체 Z범위의 1% 또는 최소 0.05mm

      ctx.strokeStyle = '#ef4444';  // 빨간색 (점선과 동일한 색상)
      ctx.setLineDash([]);          // 실선
      ctx.lineWidth = 2;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      // 1) 현재 레이어(Z 근처)에 있는 선분만 실선으로 다시 그리기
      for (let i = 0; i < lastIndex; i++) {
        const p1 = path_points[i];
        const p2 = path_points[i + 1];

        const onCurrentLayer =
          Math.abs(p1.z - currentZ) <= layerTolerance &&
          Math.abs(p2.z - currentZ) <= layerTolerance;

        if (!onCurrentLayer) continue;

        ctx.beginPath();
        ctx.moveTo(toCanvasX(p1.x), toCanvasY(p1.y));
        ctx.lineTo(toCanvasX(p2.x), toCanvasY(p2.y));
        ctx.stroke();
      }

      // 2) 현재 레이어 중에서, 현재 위치와 가장 가까운 포인트를 찾아
      //    그 포인트에서 실제 currentX/currentY까지 짧은 빨간 선으로 이어줌
      let nearestIndex = -1;
      let nearestDist = Number.MAX_VALUE;
      for (let i = 0; i <= lastIndex; i++) {
        const p = path_points[i];
        const onCurrentLayer = Math.abs(p.z - currentZ) <= layerTolerance;
        if (!onCurrentLayer) continue;
        const dx = p.x - currentX;
        const dy = p.y - currentY;
        const dist2 = dx * dx + dy * dy;
        if (dist2 < nearestDist) {
          nearestDist = dist2;
          nearestIndex = i;
        }
      }

      if (nearestIndex >= 0) {
        const p = path_points[nearestIndex];
        ctx.beginPath();
        ctx.moveTo(toCanvasX(p.x), toCanvasY(p.y));
        ctx.lineTo(toCanvasX(currentX), toCanvasY(currentY));
        ctx.stroke();
      }

      // 디버그: 콘솔에 진행 상태 출력 (개발 중에만)
      if (currentIndex % 10 === 0) {
        console.log(
          `[ToolPath] 진행: ${currentIndex}/${path_points.length}, 위치: (${currentX.toFixed(
            1
          )}, ${currentY.toFixed(1)}, Z=${currentZ.toFixed(2)})`
        );
      }
    }
    
    ctx.setLineDash([]);

    // 시작점 표시 (파란색)
    if (path_points.length > 0) {
      const startPoint = path_points[0];
      ctx.fillStyle = '#3b82f6';
      ctx.beginPath();
      ctx.arc(toCanvasX(startPoint.x), toCanvasY(startPoint.y), 5, 0, 2 * Math.PI);
      ctx.fill();
    }

    // 현재 위치 표시 (주황색)
    ctx.fillStyle = '#f97316';
    ctx.beginPath();
    ctx.arc(toCanvasX(currentX), toCanvasY(currentY), 6, 0, 2 * Math.PI);
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.stroke();

    // 상태 정보 표시 (왼쪽 상단)
    ctx.fillStyle = '#1f2937';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'left';
    
    const hasCncData = progressData?.has_cnc_data;
    const statusText = hasCncData ? '🟢 CNC 연결됨' : '⚪ CNC 대기';
    ctx.fillText(statusText, 8, 15);
    ctx.fillText(`진행률: ${progress.toFixed(1)}%`, 8, 30);
    ctx.fillText(`위치: (${currentX.toFixed(1)}, ${currentY.toFixed(1)})`, 8, 45);
    ctx.fillText(`남은거리: ${remainingDistance.toFixed(1)}mm`, 8, 60);

    // 진행률 바 (하단)
    const barWidth = canvas.width - 20;
    const barHeight = 8;
    const barX = 10;
    const barY = canvas.height - 15;
    
    ctx.fillStyle = '#e5e7eb';
    ctx.fillRect(barX, barY, barWidth, barHeight);
    
    ctx.fillStyle = '#3b82f6';
    ctx.fillRect(barX, barY, (barWidth * progress) / 100, barHeight);
    
    ctx.strokeStyle = '#9ca3af';
    ctx.lineWidth = 1;
    ctx.strokeRect(barX, barY, barWidth, barHeight);

  }, [ncData, progressData]);
    
  // 파일 선택 버튼 클릭 핸들러
  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  if (loading && !ncData) {
    return (
      <div className={`h-full bg-white shadow-lg rounded-2xl flex items-center justify-center ${className}`}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-3"></div>
          <p className="text-sm text-gray-500">NC코드 로딩 중...</p>
        </div>
      </div>
    );
  }

  // NC 파일 업로드 대기 화면
  if (!ncData) {
    return (
      <div className={`h-full bg-white shadow-lg rounded-2xl flex items-center justify-center p-4 ${className}`}>
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-3 bg-blue-100 rounded-xl flex items-center justify-center">
            <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-700 mb-2">ToolPath</h3>
          <p className="text-sm text-gray-500 mb-4">NC코드 파일을 업로드하세요</p>
          
          <input
            ref={fileInputRef}
            type="file"
            accept=".nc,.txt,.tap,.cnc,.gcode"
            onChange={handleFileUpload}
            className="hidden"
          />
          <button
            onClick={handleUploadClick}
            disabled={uploadStatus.isUploading}
            className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            {uploadStatus.isUploading ? '업로드 중...' : 'NC파일 선택'}
          </button>
          
          <p className="text-xs text-gray-400 mt-2">.nc, .txt, .tap, .gcode</p>
          
          {uploadStatus.error && (
            <p className="text-xs text-red-500 mt-2">{uploadStatus.error}</p>
          )}
        </div>
      </div>
    );
  }

  // NC 데이터 있을 때 - 시각화 화면
  return (
    <div className={`bg-white shadow-lg rounded-2xl p-3 flex flex-col h-full ${className}`}>
      {/* 헤더 */}
      <div className="flex justify-between items-center mb-1">
        <div className="flex items-center space-x-2">
          <h3 className="text-sm font-semibold text-gray-800">ToolPath</h3>
          {uploadStatus.fileName && (
            <span className="px-1.5 py-0.5 bg-green-100 text-green-700 text-xs rounded-full truncate max-w-[80px]" title={uploadStatus.fileName}>
              {uploadStatus.fileName}
            </span>
          )}
        </div>
        
        <div className="flex items-center space-x-1">
          <input
            ref={fileInputRef}
            type="file"
            accept=".nc,.txt,.tap,.cnc,.gcode"
            onChange={handleFileUpload}
            className="hidden"
          />
          <button
            onClick={handleUploadClick}
            disabled={uploadStatus.isUploading}
            className="p-1 text-gray-500 hover:text-blue-500 hover:bg-blue-50 rounded transition-colors"
            title="NC파일 업로드"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </button>
          <button
            onClick={handleClearData}
            className="p-1 text-gray-500 hover:text-red-500 hover:bg-red-50 rounded transition-colors"
            title="초기화"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
      
      {/* 범례 */}
      <div className="flex items-center justify-center space-x-3 text-xs text-gray-500 mb-1">
        <span className="flex items-center">
          <span className="w-3 h-0.5 border-t-2 border-dashed border-red-500 mr-1"></span>예정 경로
        </span>
        <span className="flex items-center">
          <span className="w-3 h-0.5 bg-red-500 mr-1"></span>완료 경로
        </span>
        <span className="flex items-center"><span className="w-2 h-2 bg-blue-500 rounded-full mr-1"></span>시작</span>
        <span className="flex items-center"><span className="w-2 h-2 bg-orange-500 rounded-full mr-1"></span>현재</span>
      </div>
      
      {/* Canvas */}
      <div className="flex-1 flex items-center justify-center">
        <canvas
          ref={canvasRef}
          className="border border-gray-200 rounded-lg w-[300px] h-[300px] flex-none"
        />
      </div>
    </div>
  );
};

export default ToolPath;
