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

  const getStatusIcon = (isConnected: boolean) => (
    <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
  );

  const getStatusText = (isConnected: boolean) => (
    <span className={`text-xs font-medium ${isConnected ? 'text-green-700' : 'text-red-700'}`}>
      {isConnected ? 'Connected' : 'Disconnected'}
    </span>
  );

  const sensors = [
    { key: 'camera', label: 'Camera' },
    { key: 'pyrometer', label: 'Pyrometer' },
    { key: 'laser', label: 'Laser' },
    { key: 'hikrobot1', label: 'HikRobot-1' },
    { key: 'hikrobot2', label: 'HikRobot-2' },
  ] as const;

  return (
    <div className="h-full overflow-y-auto p-4">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">연결 상태</h2>
      <div className="space-y-3">
        {sensors.map(({ key, label }) => {
          const isConnected = status[key];
          return (
            <div key={key} className="card">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(isConnected)}
                  <span className="text-sm font-medium text-gray-700">{label}</span>
                </div>
                {getStatusText(isConnected)}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

