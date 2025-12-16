/**
 * 카메라 뷰 컴포넌트 - Basler 및 HikRobot 카메라 이미지 표시
 * MJPEG 스트리밍 방식으로 자연스러운 실시간 영상 표시
 */
import React, { useState } from 'react';
import { useSensorData } from '../hooks/useSensorData';

// MJPEG 스트리밍 URL (백엔드에서 실시간 영상 제공)
const MJPEG_STREAM_URL = {
  basler: 'http://localhost:8000/api/stream/basler',
  hik: 'http://localhost:8000/api/stream/hik'
};

interface CameraViewProps {
  cameraType?: 'basler' | 'hikrobot';
}

const CameraView: React.FC<CameraViewProps> = ({ cameraType }) => {
  const { latestData } = useSensorData();
  const [activeTab, setActiveTab] = useState<'basler' | 'hik'>('basler');
  
  // 스트림 에러 상태 (연결 끊김 감지용)
  const [baslerError, setBaslerError] = useState(false);
  const [hikError, setHikError] = useState(false);

  /**
   * MJPEG 스트리밍 이미지 디스플레이 컴포넌트
   * <img src>로 MJPEG 스트림을 직접 표시 (가장 안정적인 방식)
   */
  const StreamDisplay = ({ 
    streamUrl, 
    available, 
    title, 
    placeholder,
    hasError,
    onError,
    onLoad
  }: {
    streamUrl: string;
    available: boolean;
    title: string;
    placeholder: string;
    hasError: boolean;
    onError: () => void;
    onLoad: () => void;
  }) => (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-2">
        <h4 className="text-sm font-semibold text-gray-700">{title}</h4>
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${available && !hasError ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
          <span className="text-xs text-gray-500">
            {available && !hasError ? 'Streaming' : 'Disconnected'}
          </span>
        </div>
      </div>

      <div className="flex-1 bg-gray-900 rounded-lg overflow-hidden relative">
        {available && !hasError ? (
          /* MJPEG 스트리밍: img 태그로 직접 표시 (산업용 표준) */
          <img
            src={streamUrl}
            alt={title}
            className="w-full h-full object-contain"
            onError={onError}
            onLoad={onLoad}
          />
        ) : (
          <div className="h-full flex items-center justify-center">
            <div className="text-center text-gray-400">
              <div className="text-4xl mb-2">{placeholder}</div>
              <div className="text-sm">
                {hasError ? '스트림 연결 끊김 - 재연결 중...' : '카메라가 연결되지 않았습니다'}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  // 연결 상태 확인 (WebSocket 데이터 기반)
  const baslerAvailable = (latestData?.camera_data as any)?.image_available || false;
  const hikAvailable = (latestData?.hik_camera_data as any)?.hik_image_available || false;

  // cameraType이 지정되지 않은 경우 기본 동작 (탭 방식)
  if (!cameraType) {
    return (
      <div className="h-full bg-white rounded-xl shadow-lg p-4">
        <div className="h-full flex flex-col">
          {/* 탭 헤더 */}
          <div className="flex mb-4">
            <button
              className={`px-4 py-2 text-sm font-medium rounded-l-lg border ${
                activeTab === 'basler'
                  ? 'bg-blue-500 text-white border-blue-500'
                  : 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200'
              }`}
              onClick={() => setActiveTab('basler')}
            >
              Basler Camera
            </button>
            <button
              className={`px-4 py-2 text-sm font-medium rounded-r-lg border-t border-r border-b ${
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
                available={baslerAvailable}
                title="Basler Camera (MJPEG)"
                placeholder="📷"
                hasError={baslerError}
                onError={() => setBaslerError(true)}
                onLoad={() => setBaslerError(false)}
              />
            ) : (
              <StreamDisplay
                streamUrl={MJPEG_STREAM_URL.hik}
                available={hikAvailable}
                title="HikRobot Camera (MJPEG)"
                placeholder="📹"
                hasError={hikError}
                onError={() => setHikError(true)}
                onLoad={() => setHikError(false)}
              />
            )}
          </div>

          {/* 전체 상태 표시 */}
          <div className="mt-3 pt-3 border-t border-gray-200">
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="flex justify-between">
                <span className="text-gray-500">Basler:</span>
                <span className={baslerAvailable ? 'text-green-600' : 'text-red-600'}>
                  {baslerAvailable ? 'Streaming' : 'Inactive'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">HikRobot:</span>
                <span className={hikAvailable ? 'text-green-600' : 'text-red-600'}>
                  {hikAvailable ? 'Streaming' : 'Inactive'}
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
      </div>
    );
  }

  // 개별 카메라 표시 (MJPEG 스트리밍)
  return (
    <div className="h-full bg-white rounded-xl shadow-lg p-4">
      <div className="h-full flex flex-col">
        {/* MJPEG 스트리밍 표시 영역 */}
        <div className="flex-1 min-h-0">
          {cameraType === 'basler' ? (
            <StreamDisplay
              streamUrl={MJPEG_STREAM_URL.basler}
              available={baslerAvailable}
              title="Basler Camera (MJPEG)"
              placeholder="📷"
              hasError={baslerError}
              onError={() => setBaslerError(true)}
              onLoad={() => setBaslerError(false)}
            />
          ) : (
            <StreamDisplay
              streamUrl={MJPEG_STREAM_URL.hik}
              available={hikAvailable}
              title="HikRobot Camera (MJPEG)"
              placeholder="📹"
              hasError={hikError}
              onError={() => setHikError(true)}
              onLoad={() => setHikError(false)}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default CameraView;