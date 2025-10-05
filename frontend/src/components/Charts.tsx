import React from 'react';

interface ChartsProps {
  chartType: "meltpoolArea" | "meltpoolTemp" | "laserPower";
}

export default function Charts({ chartType }: ChartsProps) {
  const getTitle = () => {
    switch (chartType) {
      case "meltpoolArea": return "Melt Pool Area (㎟)";
      case "meltpoolTemp": return "Melt Pool Temperature (°C)";
      case "laserPower": return "Laser Power (W)";
      default: return "Chart";
    }
  };

  const getIcon = () => {
    switch (chartType) {
      case "meltpoolArea": 
        return (
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        );
      case "meltpoolTemp":
        return (
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        );
      case "laserPower":
        return (
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        );
      default:
        return null;
    }
  };

  // 샘플 데이터 포인트
  const sampleData = Array.from({ length: 20 }, (_, i) => ({
    time: i * 5,
    value: Math.random() * 100 + 50
  }));

  return (
    <div className="card h-full">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-900">{getTitle()}</h3>
        <div className="text-blue-500">
          {getIcon()}
        </div>
      </div>
      
      <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
        <div className="text-center text-gray-500">
          <div className="mb-2">
            {getIcon()}
          </div>
          <p className="text-sm font-medium">Real-time Chart</p>
          <p className="text-xs text-gray-400 mt-1">
            {sampleData.length} data points
          </p>
          <div className="mt-4 text-xs text-gray-400">
            Last value: {sampleData[sampleData.length - 1]?.value.toFixed(1)}
          </div>
        </div>
      </div>
    </div>
  );
}
