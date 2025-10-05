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
  rempos_x: number;
  rempos_y: number;
  rempos_z: number;
  rempos_a: number;
  rempos_c: number;
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
    rempos_x: 0.00, rempos_y: 0.00, rempos_z: 0.00, rempos_a: 0.00, rempos_c: 0.00,
    travel_speed: 150.00, feed_override: 100, rapid_override: 100,
    operating_time: "00:15:30", total_operating_time: "123:45:00",
    emergency: false,
  };

  const PositionBox = ({ title, prefix }: { title: string; prefix: 'curpos' | 'macpos' | 'rempos' }) => (
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
      
      <PositionBox title="현재 좌표" prefix="curpos" />
      <PositionBox title="기계 좌표" prefix="macpos" />
      <PositionBox title="남은 거리" prefix="rempos" />
      
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
          <div className="flex justify-between">
            <span className="text-gray-600">Emergency:</span>
            <span className={`px-2 py-1 rounded text-xs font-medium ${
              cncData.emergency ? 'status-disconnected' : 'status-connected'
            }`}>
              {cncData.emergency ? 'ON' : 'OFF'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

