import React from 'react';
import { useSensorData } from '../hooks/useSensorData';

interface SensorStatus {
  camera: boolean;
  pyrometer: boolean;
  laser: boolean;
  hik_camera_1: boolean;
  hik_camera_2: boolean;
  cnc: boolean;
}

export default function ConnectionStatus() {
  const { systemStatus, isConnected, isWebSocketConnected } = useSensorData();

  // 실제 센서 상태 또는 기본값
  const status: SensorStatus = systemStatus?.sensors || {
    camera: false,
    pyrometer: false,
    laser: false,
    hik_camera_1: false,
    hik_camera_2: false,
    cnc: false,
  };


  const sensors = [
    { key: 'camera', label: 'Basler Camera' },
    { key: 'hik_camera_1', label: 'HikRobot-1' },
    { key: 'hik_camera_2', label: 'HikRobot-2' },
    { key: 'pyrometer', label: '2color Pyrometer' },
    { key: 'laser', label: 'Laser' },
    { key: 'cnc', label: 'CNC' },
  ] as const;

  return (
    <div className="h-full">
      <div className="flex items-center mb-4">
        <div className={`w-6 h-6 rounded-full flex items-center justify-center mr-3 ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}>
          <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        </div>
        <h3 className="text-sm font-bold text-gray-900">연결 상태</h3>
      </div>
      
      {/* 백엔드 연결 상태 */}
      <div className="mb-3 p-2 rounded-lg bg-blue-50">
        <div className="flex items-center justify-between">
          <span className="text-xs font-medium text-gray-700">Backend API</span>
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xs font-medium text-gray-700">WebSocket</span>
          <div className={`w-2 h-2 rounded-full ${isWebSocketConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
        </div>
      </div>
      
      <div className="bg-gray-50 p-3 rounded-lg">
        <div className="grid grid-cols-2 gap-1">
          {sensors.map(({ key, label }) => {
            const isConnected = status[key as keyof SensorStatus];
            return (
              <div key={key} className="flex items-center space-x-1.5 p-1">
                <div className={`w-2.5 h-2.5 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
                <span className="text-xs font-medium text-gray-700">{label}</span>
              </div>
            );
          })}
        </div>
      </div>
      
      {/* 시스템 상태 정보 */}
      {systemStatus && (
        <div className="mt-3 p-2 rounded-lg bg-green-50">
          <div className="text-xs text-gray-600 text-center">
            System: {systemStatus.system_status}
          </div>
          <div className="text-xs text-gray-500 text-center">
            Last Update: {new Date(systemStatus.timestamp).toLocaleTimeString()}
          </div>
        </div>
      )}
    </div>
  );
}

