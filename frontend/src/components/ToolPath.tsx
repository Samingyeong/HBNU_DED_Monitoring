/**
 * ToolPath 시각화 컴포넌트 - 2D Canvas를 사용한 경로 표시
 */
import React, { useEffect, useRef, useState } from 'react';
import { useSensorData } from '../hooks/useSensorData';

interface ToolPathProps {
  className?: string;
}

interface PathPoint {
  x: number;
  y: number;
  z: number;
  line: number;
  type: string;
}

interface NCPathData {
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

const ToolPath: React.FC<ToolPathProps> = ({ className }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [ncData, setNcData] = useState<NCPathData | null>(null);
  const [loading, setLoading] = useState(false);
  const { latestData } = useSensorData();

  // NC코드 경로 데이터 로드
  useEffect(() => {
    const loadNCData = async () => {
      setLoading(true);
      try {
        console.log('NC코드 데이터 로드 시도...');
        const response = await fetch('http://127.0.0.1:8000/api/nc/path');
        console.log('응답 상태:', response.status);
        
        if (response.ok) {
          const data = await response.json();
          console.log('NC코드 데이터 로드 성공:', data);
          setNcData(data);
        } else if (response.status === 404) {
          // NC코드가 파싱되지 않은 경우
          console.log('NC코드 데이터 없음 (404)');
          setNcData(null);
        } else {
          console.log('응답 오류:', response.status, response.statusText);
          setNcData(null);
        }
      } catch (error) {
        console.error('NC코드 경로 데이터 로드 실패:', error);
        setNcData(null);
      } finally {
        setLoading(false);
      }
    };

    loadNCData();
    
    // 2초마다 NC코드 데이터 다시 로드 (새로운 파일이 파싱되었을 때 감지)
    const interval = setInterval(loadNCData, 2000);
    
    return () => clearInterval(interval);
  }, []);

  // Canvas 렌더링
  useEffect(() => {
    if (!canvasRef.current || !ncData) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Canvas 크기 설정
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;

    // 배경 초기화
    ctx.fillStyle = '#f9fafb';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const { bounds, path_points } = ncData;

    // 좌표 변환 함수 (NC코드 좌표 → Canvas 좌표)
    const padding = 20;
    const scaleX = (canvas.width - 2 * padding) / (bounds.x_range || 1);
    const scaleY = (canvas.height - 2 * padding) / (bounds.y_range || 1);
    const scale = Math.min(scaleX, scaleY);

    const toCanvasX = (x: number) => {
      return padding + (x - bounds.x_min) * scale;
    };

    const toCanvasY = (y: number) => {
      // Y축 반전 (Canvas는 위에서 아래로 증가)
      return canvas.height - padding - (y - bounds.y_min) * scale;
    };

    // 현재 CNC 위치
    const currentX = latestData?.cnc_data?.curpos_x || 0;
    const currentY = latestData?.cnc_data?.curpos_y || 0;

    // 현재 위치와 가장 가까운 경로 포인트 찾기
    let closestIndex = 0;
    let minDistance = Infinity;
    let remainingDistance = 0;
    
    path_points.forEach((point, index) => {
      const distance = Math.sqrt(
        Math.pow(point.x - currentX, 2) + 
        Math.pow(point.y - currentY, 2)
      );
      if (distance < minDistance) {
        minDistance = distance;
        closestIndex = index;
      }
    });

    // 남은 거리 계산 (현재 위치부터 끝까지의 경로 길이)
    for (let i = closestIndex; i < path_points.length - 1; i++) {
      const p1 = path_points[i];
      const p2 = path_points[i + 1];
      remainingDistance += Math.sqrt(
        Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2)
      );
    }

    // 전체 경로 길이 계산
    let totalDistance = 0;
    for (let i = 0; i < path_points.length - 1; i++) {
      const p1 = path_points[i];
      const p2 = path_points[i + 1];
      totalDistance += Math.sqrt(
        Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2)
      );
    }

    // 진행률 계산
    const progress = totalDistance > 0 ? ((totalDistance - remainingDistance) / totalDistance) * 100 : 0;

    // 전체 경로 그리기 (회색)
    ctx.strokeStyle = '#d1d5db';
    ctx.lineWidth = 1;
    ctx.beginPath();
    path_points.forEach((point, index) => {
      const canvasX = toCanvasX(point.x);
      const canvasY = toCanvasY(point.y);
      
      if (index === 0) {
        ctx.moveTo(canvasX, canvasY);
      } else {
        ctx.lineTo(canvasX, canvasY);
      }
    });
    ctx.stroke();

    // 완료된 경로 그리기 (초록색)
    if (closestIndex > 0) {
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let i = 0; i <= closestIndex; i++) {
        const point = path_points[i];
        const canvasX = toCanvasX(point.x);
        const canvasY = toCanvasY(point.y);
        
        if (i === 0) {
          ctx.moveTo(canvasX, canvasY);
        } else {
          ctx.lineTo(canvasX, canvasY);
        }
      }
      ctx.stroke();
    }

    // 시작점 표시 (파란색)
    if (path_points.length > 0) {
      const startPoint = path_points[0];
      ctx.fillStyle = '#3b82f6';
      ctx.beginPath();
      ctx.arc(toCanvasX(startPoint.x), toCanvasY(startPoint.y), 5, 0, 2 * Math.PI);
      ctx.fill();
    }

    // 현재 위치 표시 (빨간색)
    ctx.fillStyle = '#ef4444';
    ctx.beginPath();
    ctx.arc(toCanvasX(currentX), toCanvasY(currentY), 6, 0, 2 * Math.PI);
    ctx.fill();
    
    // 현재 위치에 테두리
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.stroke();

    // 진행률 바 그리기
    const progressBarWidth = 200;
    const progressBarHeight = 20;
    const progressBarX = canvas.width - progressBarWidth - 10;
    const progressBarY = 10;
    
    // 진행률 바 배경
    ctx.fillStyle = '#e5e7eb';
    ctx.fillRect(progressBarX, progressBarY, progressBarWidth, progressBarHeight);
    
    // 진행률 바 채우기
    ctx.fillStyle = '#3b82f6';
    ctx.fillRect(progressBarX, progressBarY, (progressBarWidth * progress) / 100, progressBarHeight);
    
    // 진행률 바 테두리
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 1;
    ctx.strokeRect(progressBarX, progressBarY, progressBarWidth, progressBarHeight);
    
    // 진행률 텍스트
    ctx.fillStyle = '#1f2937';
    ctx.font = 'bold 12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`${progress.toFixed(1)}%`, progressBarX + progressBarWidth / 2, progressBarY + 14);
    
    // 상세 정보 텍스트
    ctx.textAlign = 'left';
    ctx.font = 'bold 12px sans-serif';
    ctx.fillText(`진행률: ${progress.toFixed(1)}%`, 10, 20);
    ctx.fillText(`남은 거리: ${remainingDistance.toFixed(2)}mm`, 10, 35);
    ctx.fillText(`전체 거리: ${totalDistance.toFixed(2)}mm`, 10, 50);
    ctx.fillText(`포인트: ${closestIndex + 1} / ${path_points.length}`, 10, 65);
    ctx.fillText(`현재 위치: (${currentX.toFixed(2)}, ${currentY.toFixed(2)})`, 10, 80);

  }, [ncData, latestData]);

  if (loading) {
    return (
      <div className={`h-full bg-white shadow-lg rounded-2xl flex items-center justify-center ${className}`}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-3"></div>
          <p className="text-sm text-gray-500">NC코드 로딩 중...</p>
        </div>
      </div>
    );
  }

  if (!ncData) {
    return (
      <div className={`h-full bg-white shadow-lg rounded-2xl flex items-center justify-center ${className}`}>
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-3 bg-gray-200 rounded-xl flex items-center justify-center">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m-6 3l6-3" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-700 mb-1">ToolPath</h3>
          <p className="text-sm text-gray-500">NC코드를 불러오는 중...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`h-full bg-white shadow-lg rounded-2xl p-3 flex flex-col ${className}`}>
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-sm font-semibold text-gray-800">ToolPath 진행상황</h3>
        <div className="flex items-center space-x-2 text-xs text-gray-500">
          <span>🔵 시작점</span>
          <span>🟢 완료구간</span>
          <span>🔴 현재위치</span>
          <span>⚪ 남은구간</span>
        </div>
      </div>
      
      <canvas
        ref={canvasRef}
        className="flex-1 w-full h-full border border-gray-200 rounded-lg"
      />
    </div>
  );
};

export default ToolPath;

