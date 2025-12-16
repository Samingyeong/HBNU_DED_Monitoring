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
      setNcData(pathResponse.data);
      
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
        console.log('기존 NC코드 데이터 발견:', response.data);
        setNcData(response.data);
      } catch (error: any) {
        if (error.response?.status === 404) {
          console.log('NC코드 데이터 없음 - 파일 업로드 대기');
        }
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
    if (!canvasRef.current || !ncData) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Canvas 크기 설정
    const container = canvas.parentElement;
    const size = container ? Math.min(container.clientWidth, container.clientHeight, 350) : 300;
    canvas.width = size;
    canvas.height = size;

    // 배경 초기화
    ctx.fillStyle = '#f9fafb';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const { bounds, path_points } = ncData;

    // 좌표 변환 함수 (NC코드 좌표 → Canvas 좌표)
    const padding = 25;
    const scaleX = (canvas.width - 2 * padding) / (bounds.x_range || 1);
    const scaleY = (canvas.height - 2 * padding) / (bounds.y_range || 1);
    const scale = Math.min(scaleX, scaleY);

    const toCanvasX = (x: number) => padding + (x - bounds.x_min) * scale;
    const toCanvasY = (y: number) => canvas.height - padding - (y - bounds.y_min) * scale;

    // 백엔드에서 받은 진행률 데이터 사용
    const currentIndex = progressData?.current_index || 0;
    const currentX = progressData?.current_position?.x || path_points[0]?.x || 0;
    const currentY = progressData?.current_position?.y || path_points[0]?.y || 0;
    const progress = progressData?.progress || 0;
    const totalDistance = progressData?.total_distance || 0;
    const remainingDistance = progressData?.remaining_distance || 0;

    // 전체 경로 그리기 (G00: 빨강 점선, G01: 초록 실선)
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
      
      // G00 (rapid) = 빨간색 점선, G01 (linear) = 초록색 실선
      if (p2.type === 'rapid') {
        ctx.strokeStyle = '#fca5a5';  // 연한 빨강 (G00)
        ctx.setLineDash([4, 4]);
        ctx.lineWidth = 1;
      } else {
        ctx.strokeStyle = '#86efac';  // 연한 초록 (G01)
        ctx.setLineDash([]);
        ctx.lineWidth = 1.5;
      }
      
      ctx.stroke();
    }
    ctx.setLineDash([]);

    // 완료된 경로 강조 (진한 색, 굵은 선)
    if (currentIndex > 0) {
      for (let i = 0; i < currentIndex; i++) {
        const p1 = path_points[i];
        const p2 = path_points[i + 1];
        if (!p2) continue;
        
        const x1 = toCanvasX(p1.x);
        const y1 = toCanvasY(p1.y);
        const x2 = toCanvasX(p2.x);
        const y2 = toCanvasY(p2.y);
        
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        
        if (p2.type === 'rapid') {
          ctx.strokeStyle = '#dc2626';  // 진한 빨강
          ctx.setLineDash([4, 4]);
          ctx.lineWidth = 2;
        } else {
          ctx.strokeStyle = '#16a34a';  // 진한 초록
          ctx.setLineDash([]);
          ctx.lineWidth = 2.5;
        }
        
        ctx.stroke();
      }
      ctx.setLineDash([]);
    }

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
        <span className="flex items-center"><span className="w-3 h-0.5 bg-red-400 mr-1"></span>G00</span>
        <span className="flex items-center"><span className="w-3 h-0.5 bg-green-500 mr-1"></span>G01</span>
        <span className="flex items-center"><span className="w-2 h-2 bg-blue-500 rounded-full mr-1"></span>시작</span>
        <span className="flex items-center"><span className="w-2 h-2 bg-orange-500 rounded-full mr-1"></span>현재</span>
      </div>
      
      {/* Canvas */}
      <div className="flex-1 flex items-center justify-center">
        <canvas
          ref={canvasRef}
          className="border border-gray-200 rounded-lg"
        />
      </div>
    </div>
  );
};

export default ToolPath;
