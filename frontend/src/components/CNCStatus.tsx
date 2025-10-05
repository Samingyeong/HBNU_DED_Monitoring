import React from 'react';

interface CNCData {
  curpos_x: number;
  curpos_y: number;
  curpos_z: number;
  curpos_a: number;
  curpos_c: number;
  macpos_x: number;
  macpos_y: number;
  macpos_z: number;
  macpos_a: number;
  macpos_c: number;
  travel_speed: number;
  feed_override: number;
  rapid_override: number;
  operating_time: string;
  total_operating_time: string;
  emergency: boolean;
}

export default function CNCStatus() {
  // 샘플 데이터
  const cncData: CNCData = {
    curpos_x: 100.00, curpos_y: 50.00, curpos_z: 20.00, curpos_a: 0.00, curpos_c: 0.00,
    macpos_x: 100.00, macpos_y: 50.00, macpos_z: 20.00, macpos_a: 0.00, macpos_c: 0.00,
    travel_speed: 150.00, feed_override: 100, rapid_override: 100,
    operating_time: "00:15:30", total_operating_time: "123:45:00",
    emergency: false,
  };

  const PositionBox = ({ title, prefix }: { title: string; prefix: 'curpos' | 'macpos' }) => (
    <div className="card mb-4">
      <h3 className="text-lg font-medium text-gray-900 mb-3">{title}</h3>
      <div className="grid grid-cols-2 gap-3">
        {['x', 'y', 'z', 'a', 'c'].map(axis => (
          <div key={axis} className="flex justify-between">
            <span className="text-sm font-medium text-gray-600 uppercase">{axis}:</span>
            <span className="text-sm text-gray-900 font-mono">
              {(cncData[`${prefix}_${axis}` as keyof CNCData] as number).toFixed(2)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="h-full overflow-y-auto p-4">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">CNC Machine Status</h2>
      
      {/* 현재 좌표와 기계 좌표를 한 행에 2열로 배치 */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <PositionBox title="현재 좌표" prefix="curpos" />
        <PositionBox title="기계 좌표" prefix="macpos" />
      </div>
      
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-3">운전 정보</h3>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">Travel Speed:</span>
            <span className="font-mono">{cncData.travel_speed} mm/min</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Feed Override:</span>
            <span className="font-mono">{cncData.feed_override}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Rapid Override:</span>
            <span className="font-mono">{cncData.rapid_override}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Operating Time:</span>
            <span className="font-mono">{cncData.operating_time}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Total Time:</span>
            <span className="font-mono">{cncData.total_operating_time}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

