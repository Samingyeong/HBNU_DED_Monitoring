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
  // Feed Rate 데이터
  feeder1_rpm: number;
  feeder1_remaining: number;
  feeder1_status: boolean;
  feeder2_rpm: number;
  feeder2_remaining: number;
  feeder2_status: boolean;
  feeder3_rpm: number;
  feeder3_remaining: number;
  feeder3_status: boolean;
  // Gas 데이터
  coaxial_gas: number;
  feeding_gas: number;
  shield_gas: number;
}

export default function CNCStatus() {
  // 샘플 데이터
  const cncData: CNCData = {
    curpos_x: 3.92, curpos_y: 1.50, curpos_z: 6.24, curpos_a: 0.00, curpos_c: 0.00,
    macpos_x: -105.48, macpos_y: -149.20, macpos_z: -122.71, macpos_a: 0.00, macpos_c: 0.00,
    // Feed Rate 데이터
    feeder1_rpm: 1200, feeder1_remaining: 85, feeder1_status: true,
    feeder2_rpm: 800, feeder2_remaining: 92, feeder2_status: false,
    feeder3_rpm: 1500, feeder3_remaining: 78, feeder3_status: true,
    // Gas 데이터
    coaxial_gas: 15.5, feeding_gas: 8.2, shield_gas: 12.8,
  };

  const PositionBox = ({ title, prefix }: { title: string; prefix: 'curpos' | 'macpos' }) => (
    <div className="bg-gray-50 p-3 rounded-lg">
      <h4 className="text-xs font-bold text-gray-900 mb-2 pb-1 border-b border-gray-300">{title}</h4>
      <div className="space-y-2">
        {['x', 'y', 'z', 'a', 'c'].map(axis => (
          <div key={axis} className="flex items-center justify-center gap-2">
            <span className="text-xs font-medium text-gray-600 uppercase">{axis}:</span>
            <span className="text-xs text-gray-900 font-mono">
              {(cncData[`${prefix}_${axis}` as keyof CNCData] as number).toFixed(2)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="h-full">
      {/* 시스템 상태 제목 */}
      <div className="flex items-center mb-4">
        <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center mr-3">
          <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
          </svg>
        </div>
        <h3 className="text-sm font-bold text-gray-900">시스템 상태</h3>
      </div>
      
      <div className="space-y-3">
        {/* 현재 좌표와 기계 좌표를 한 행에 2열로 배치 */}
        <div className="grid grid-cols-2 gap-3">
          <PositionBox title="상대좌표/현재좌표" prefix="curpos" />
          <PositionBox title="절대좌표/기계좌표" prefix="macpos" />
        </div>
        
        {/* Feed Rate 카드 */}
        <div className="bg-gray-50 p-3 rounded-lg">
          <h4 className="text-xs font-bold text-gray-900 mb-2 pb-1 border-b border-gray-300">Feed Rate</h4>
          <div className="space-y-2">
            {/* 헤더 */}
            <div className="flex justify-center text-xs">
              <div className="w-20"></div>
              <div className="w-16 text-center text-gray-600 font-medium">[RPM]</div>
              <div className="w-16 text-center text-gray-600 font-medium">[잔량]</div>
            </div>
            
            {/* 피더 데이터 */}
            {[
              { name: 'Feeder1', rpm: cncData.feeder1_rpm, remaining: cncData.feeder1_remaining, status: cncData.feeder1_status },
              { name: 'Feeder2', rpm: cncData.feeder2_rpm, remaining: cncData.feeder2_remaining, status: cncData.feeder2_status },
              { name: 'Feeder3', rpm: cncData.feeder3_rpm, remaining: cncData.feeder3_remaining, status: cncData.feeder3_status }
            ].map((feeder) => (
              <div key={feeder.name} className="flex justify-center items-center text-xs">
                <div className="flex items-center gap-2 w-20">
                  <div className={`w-3 h-3 rounded-full ${feeder.status ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <span className="font-medium text-gray-900">{feeder.name}</span>
                </div>
                <div className="w-16 text-center font-mono text-gray-900">{feeder.rpm}</div>
                <div className="w-16 text-center font-mono text-gray-900">{feeder.remaining}%</div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Gas 카드 */}
        <div className="bg-gray-50 p-3 rounded-lg">
          <h4 className="text-xs font-bold text-gray-900 mb-2 pb-1 border-b border-gray-300">Gas (L/min)</h4>
          <div className="grid grid-cols-3 gap-3">
            {[
              { name: 'Coaxial', value: cncData.coaxial_gas },
              { name: 'Feeding', value: cncData.feeding_gas },
              { name: 'Shield', value: cncData.shield_gas }
            ].map((gas) => (
              <div key={gas.name} className="text-center">
                <div className="text-xs font-medium text-gray-900 mb-1">{gas.name}</div>
                <div className="text-sm font-mono text-gray-900">{gas.value}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

