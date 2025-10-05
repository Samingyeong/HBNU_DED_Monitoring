import React from 'react';

interface SensorStatus {
  camera: boolean;
  pyrometer: boolean;
  laser: boolean;
  hikrobot1: boolean;
  hikrobot2: boolean;
}

export default function ConnectionStatus() {
  // 샘플 데이터
  const status: SensorStatus = {
    camera: true,
    pyrometer: false,
    laser: true,
    hikrobot1: true,
    hikrobot2: false,
  };


  const sensors = [
    { key: 'camera', label: 'Basler Camera' },
    { key: 'hikrobot1', label: 'HikRobot-1' },
    { key: 'hikrobot2', label: 'HikRobot-2' },
    { key: 'pyrometer', label: '2color Pyrometer' },
    { key: 'laser', label: 'Laser' },
  ] as const;

  return (
    <div className="h-full">
      <div className="flex items-center mb-4">
        <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center mr-3">
          <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        </div>
        <h3 className="text-sm font-bold text-gray-900">연결 상태</h3>
      </div>
      <div className="bg-gray-50 p-3 rounded-lg">
        <div className="grid grid-cols-2 gap-1">
          {sensors.map(({ key, label }) => {
            const isConnected = status[key];
            return (
              <div key={key} className="flex items-center space-x-1.5 p-1">
                <div className={`w-2.5 h-2.5 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
                <span className="text-xs font-medium text-gray-700">{label}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

