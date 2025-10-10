/**
 * 카메라 뷰 컴포넌트 - Basler 및 HikRobot 카메라 이미지 표시
 */
import React, { useState, useEffect } from 'react';
import { useSensorData } from '../hooks/useSensorData';

interface CameraViewProps {
  cameraType?: 'basler' | 'hikrobot';
}

const CameraView: React.FC<CameraViewProps> = ({ cameraType }) => {
  const { latestData } = useSensorData();
  const [baslerImageUrl, setBaslerImageUrl] = useState<string | null>(null);
  const [hikImageUrl, setHikImageUrl] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'basler' | 'hik'>('basler');

  // 이미지 로딩 상태
  const [baslerLoading, setBaslerLoading] = useState(false);
  const [hikLoading, setHikLoading] = useState(false);

  // Basler 이미지 로드
  useEffect(() => {
    const loadBaslerImage = async () => {
      if ((latestData?.camera_data as any)?.image_available) {
        setBaslerLoading(true);
        try {
          const imageUrl = await import('../services/api').then(api => 
            api.ApiService.getImage('basler')
          );
          setBaslerImageUrl(imageUrl);
        } catch (error) {
          console.error('Basler 이미지 로드 실패:', error);
        } finally {
          setBaslerLoading(false);
        }
      }
    };

    loadBaslerImage();
  }, [(latestData?.camera_data as any)?.image_available]);

  // HikRobot 이미지 로드
  useEffect(() => {
    const loadHikImage = async () => {
      if ((latestData?.hik_camera_data as any)?.hik_image_available) {
        setHikLoading(true);
        try {
          const imageUrl = await import('../services/api').then(api => 
            api.ApiService.getImage('hik')
          );
          setHikImageUrl(imageUrl);
        } catch (error) {
          console.error('HikRobot 이미지 로드 실패:', error);
        } finally {
          setHikLoading(false);
        }
      }
    };

    loadHikImage();
  }, [(latestData?.hik_camera_data as any)?.hik_image_available]);

  const ImageDisplay = ({ 
    imageUrl, 
    loading, 
    available, 
    title, 
    placeholder 
  }: {
    imageUrl: string | null;
    loading: boolean;
    available: boolean;
    title: string;
    placeholder: string;
  }) => (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-2">
        <h4 className="text-sm font-semibold text-gray-700">{title}</h4>
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${available ? 'bg-green-500' : 'bg-red-500'}`}></div>
          <span className="text-xs text-gray-500">
            {available ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      <div className="flex-1 bg-gray-100 rounded-lg overflow-hidden relative">
        {loading ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
              <div className="text-sm text-gray-500">이미지 로딩 중...</div>
            </div>
          </div>
        ) : imageUrl ? (
          <img
            src={imageUrl}
            alt={title}
            className="w-full h-full object-contain"
            onError={() => {
              console.error(`${title} 이미지 로드 실패`);
            }}
          />
        ) : (
          <div className="h-full flex items-center justify-center">
            <div className="text-center text-gray-500">
              <div className="text-4xl mb-2">{placeholder}</div>
              <div className="text-sm">
                {available ? '이미지를 불러오는 중...' : '카메라가 연결되지 않았습니다'}
              </div>
            </div>
          </div>
        )}
      </div>

    </div>
  );

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

          {/* 이미지 표시 영역 */}
          <div className="flex-1 min-h-0">
            {activeTab === 'basler' ? (
              <ImageDisplay
                imageUrl={baslerImageUrl}
                loading={baslerLoading}
                available={(latestData?.camera_data as any)?.image_available || false}
                title="Basler Camera"
                placeholder="📷"
              />
            ) : (
              <ImageDisplay
                imageUrl={hikImageUrl}
                loading={hikLoading}
                available={(latestData?.hik_camera_data as any)?.hik_image_available || false}
                title="HikRobot Camera"
                placeholder="📹"
              />
            )}
          </div>

          {/* 전체 상태 표시 */}
          <div className="mt-3 pt-3 border-t border-gray-200">
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="flex justify-between">
                <span className="text-gray-500">Basler:</span>
                <span className={(latestData?.camera_data as any)?.image_available ? 'text-green-600' : 'text-red-600'}>
                  {(latestData?.camera_data as any)?.image_available ? 'Active' : 'Inactive'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">HikRobot:</span>
                <span className={(latestData?.hik_camera_data as any)?.hik_image_available ? 'text-green-600' : 'text-red-600'}>
                  {(latestData?.hik_camera_data as any)?.hik_image_available ? 'Active' : 'Inactive'}
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

  // 개별 카메라 표시
  return (
    <div className="h-full bg-white rounded-xl shadow-lg p-4">
      <div className="h-full flex flex-col">
        {/* 이미지 표시 영역 */}
        <div className="flex-1 min-h-0">
          {cameraType === 'basler' ? (
            <ImageDisplay
              imageUrl={baslerImageUrl}
              loading={baslerLoading}
              available={(latestData?.camera_data as any)?.image_available || false}
              title="Basler Camera"
              placeholder="📷"
            />
          ) : (
            <ImageDisplay
              imageUrl={hikImageUrl}
              loading={hikLoading}
              available={(latestData?.hik_camera_data as any)?.hik_image_available || false}
              title="HikRobot Camera"
              placeholder="📹"
            />
          )}
        </div>

      </div>
    </div>
  );
};

export default CameraView;