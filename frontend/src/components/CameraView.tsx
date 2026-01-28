/**
 * 카메라 뷰 컴포넌트 - Basler 및 HikRobot 카메라 이미지 표시
 * MJPEG 스트리밍 방식으로 자연스러운 실시간 영상 표시
 */
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useSensorData } from '../hooks/useSensorData';

// MJPEG 스트리밍 URL (백엔드에서 실시간 영상 제공)
const MJPEG_STREAM_URL = {
  basler: 'http://localhost:8000/api/stream/basler',
  hik: 'http://localhost:8000/api/stream/hik'
};

interface CameraViewProps {
  cameraType?: 'basler' | 'hikrobot';
}

/**
 * 개별 스트림 디스플레이 컴포넌트
 */
const StreamDisplay = React.memo(({ 
  streamUrl, 
  title, 
  placeholder,
}: {
  streamUrl: string;
  title: string;
  placeholder: string;
}) => {
  const [status, setStatus] = useState<'loading' | 'streaming' | 'error'>('loading');
  const [retryCount, setRetryCount] = useState(0);
  const imgRef = useRef<HTMLImageElement>(null);
  const retryTimerRef = useRef<NodeJS.Timeout | null>(null);

  // 스트림 URL (리트라이 시 캐시 무효화)
  const currentStreamUrl = `${streamUrl}?retry=${retryCount}`;

  // 에러 발생 시 자동 재연결
  const handleError = useCallback(() => {
    setStatus('error');
    
    // 기존 타이머 취소
    if (retryTimerRef.current) {
      clearTimeout(retryTimerRef.current);
    }
    
    // 3초 후 재연결
    retryTimerRef.current = setTimeout(() => {
      console.log(`[Camera] 재연결 시도: ${title}`);
      setStatus('loading');
      setRetryCount(prev => prev + 1);
    }, 3000);
  }, [title]);

  const handleLoad = useCallback(() => {
    setStatus('streaming');
  }, []);

  // 컴포넌트 언마운트 시 타이머 정리
  useEffect(() => {
    return () => {
      if (retryTimerRef.current) {
        clearTimeout(retryTimerRef.current);
      }
    };
  }, []);

  return (
    <div className="h-full flex flex-col">
      {/* 헤더 */}
      <div className="flex items-center justify-between mb-2 flex-shrink-0">
        <h4 className="text-sm font-semibold text-gray-700">{title}</h4>
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${
            status === 'streaming' ? 'bg-green-500 animate-pulse' : 
            status === 'loading' ? 'bg-yellow-500 animate-pulse' : 'bg-red-500'
          }`} />
          <span className="text-xs text-gray-500">
            {status === 'streaming' ? 'Streaming' : 
             status === 'loading' ? 'Connecting...' : 'Reconnecting...'}
          </span>
        </div>
      </div>

      {/* 비디오 영역 - 고정 높이를 살짝 키워서 레이아웃 안정화 */}
      <div 
        className="flex-1 bg-gray-900 rounded-lg overflow-hidden relative"
        style={{ minHeight: '320px', maxHeight: '460px' }}
      >
        {/* 항상 img 태그 렌더링 (visibility로 제어) */}
        <img
          ref={imgRef}
          key={retryCount}
          src={currentStreamUrl}
          alt={title}
          className="absolute inset-0 w-full h-full object-contain"
          onError={handleError}
          onLoad={handleLoad}
          style={{ 
            visibility: status === 'streaming' ? 'visible' : 'hidden',
            backgroundColor: '#111'
          }}
        />
        
        {/* 로딩/에러 오버레이 */}
        {status !== 'streaming' && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-900">
            <div className="text-center text-gray-400">
              <div className="text-4xl mb-3">{placeholder}</div>
              <div className="text-sm">
                {status === 'loading' ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full animate-spin" />
                    스트림 연결 중...
                  </span>
                ) : (
                  '스트림 재연결 중...'
                )}
              </div>
            </div>
          </div>
        )}
        
        {/* LIVE 표시 */}
        {status === 'streaming' && (
          <div className="absolute bottom-2 right-2 bg-red-600 text-white text-xs font-bold px-2 py-1 rounded flex items-center gap-1">
            <span className="w-2 h-2 bg-white rounded-full animate-pulse" />
            LIVE
          </div>
        )}
      </div>
    </div>
  );
});

StreamDisplay.displayName = 'StreamDisplay';

const CameraView: React.FC<CameraViewProps> = ({ cameraType }) => {
  const { latestData, systemStatus } = useSensorData();
  const [activeTab, setActiveTab] = useState<'basler' | 'hik'>('basler');

  // 연결 상태 확인
  const baslerConnected = systemStatus?.sensors?.camera || false;
  const hikConnected = (systemStatus?.sensors?.hik_camera_1 && systemStatus?.sensors?.hik_camera_2) || false;

  // cameraType이 지정되지 않은 경우 기본 동작 (탭 방식)
  if (!cameraType) {
    return (
      <div className="h-full bg-white rounded-xl shadow-lg p-4 flex flex-col">
        {/* 탭 헤더 */}
        <div className="flex mb-3 flex-shrink-0">
          <button
            className={`px-4 py-2 text-sm font-medium rounded-l-lg border transition-colors ${
              activeTab === 'basler'
                ? 'bg-blue-500 text-white border-blue-500'
                : 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200'
            }`}
            onClick={() => setActiveTab('basler')}
          >
            Basler Camera
          </button>
          <button
            className={`px-4 py-2 text-sm font-medium rounded-r-lg border-t border-r border-b transition-colors ${
              activeTab === 'hik'
                ? 'bg-blue-500 text-white border-blue-500'
                : 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200'
            }`}
            onClick={() => setActiveTab('hik')}
          >
            HikRobot Camera
          </button>
        </div>

        {/* MJPEG 스트리밍 표시 영역 */}
        <div className="flex-1 min-h-0">
          {activeTab === 'basler' ? (
            <StreamDisplay
              streamUrl={MJPEG_STREAM_URL.basler}
              title="Basler Camera (MJPEG)"
              placeholder="📷"
            />
          ) : (
            <StreamDisplay
              streamUrl={MJPEG_STREAM_URL.hik}
              title="HikRobot Camera (MJPEG)"
              placeholder="📹"
            />
          )}
        </div>

        {/* 상태 표시 */}
        <div className="mt-3 pt-3 border-t border-gray-200 flex-shrink-0">
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="flex justify-between">
              <span className="text-gray-500">Basler:</span>
              <span className={baslerConnected ? 'text-green-600' : 'text-gray-400'}>
                {baslerConnected ? 'Connected' : 'N/A'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">HikRobot:</span>
              <span className={hikConnected ? 'text-green-600' : 'text-gray-400'}>
                {hikConnected ? 'Connected' : 'N/A'}
              </span>
            </div>
          </div>
          
          {latestData?.timestamp && (
            <div className="mt-2 text-xs text-gray-400 text-center">
              Last Update: {new Date(latestData.timestamp).toLocaleTimeString()}
            </div>
          )}
        </div>
      </div>
    );
  }

  // 개별 카메라 표시 (MJPEG 스트리밍)
  return (
    <div className="h-full bg-white rounded-xl shadow-lg p-4 flex flex-col">
      <div className="flex-1 min-h-0">
        {cameraType === 'basler' ? (
          <StreamDisplay
            streamUrl={MJPEG_STREAM_URL.basler}
            title="Basler Camera (MJPEG)"
            placeholder="📷"
          />
        ) : (
          <StreamDisplay
            streamUrl={MJPEG_STREAM_URL.hik}
            title="HikRobot Camera (MJPEG)"
            placeholder="📹"
          />
        )}
      </div>
    </div>
  );
};

export default CameraView;
