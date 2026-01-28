import React from 'react';
import { useSensorData } from '../hooks/useSensorData';

interface CNCData {
  curpos_x?: number;
  curpos_y?: number;
  curpos_z?: number;
  curpos_a?: number;
  curpos_c?: number;
  macpos_x?: number;
  macpos_y?: number;
  macpos_z?: number;
  macpos_a?: number;
  macpos_c?: number;
  feed_rate?: number;
  feed_override?: number;
  rapid_override?: number;
  // Feed Rate 데이터 (GuiState.ini에서 읽음)
  feeder1_rpm?: number;
  feeder2_rpm?: number;
  feeder3_rpm?: number;
  // Gas 데이터 (GuiState.ini에서 읽음)
  powder_gas?: number;
  coaxial_gas?: number;
  shield_gas?: number;
}

export default function CNCStatus() {
  const { latestData, systemStatus } = useSensorData();

  // 정규화(flat) 또는 cnc_data 중 우선. flat: curpos_*, powder_gas, coaxial_gas, shield_gas
  const flat = (latestData || {}) as any;

  // 위치(curpos)는 기존 로직 유지: flat에만 있고 cnc_data가 없을 때만 사용
  const fromFlatPos =
    !flat.cnc_data && (flat.curpos_x != null || flat.curpos_y != null)
      ? {
          curpos_x: flat.curpos_x,
          curpos_y: flat.curpos_y,
          curpos_z: flat.curpos_z,
          curpos_a: flat.curpos_a,
          curpos_c: flat.curpos_c,
        }
      : {};

  // ✅ 가스/피더는 Measurement CSV에서 온 flat 값을 항상 우선 사용
  const fromFlatGasFeeder = {
    powder_gas: flat.powder_gas,
    coaxial_gas: flat.coaxial_gas,
    shield_gas: flat.shield_gas,
    feeder1_rpm: flat.feeder1_rpm,
    feeder2_rpm: flat.feeder2_rpm,
    feeder3_rpm: flat.feeder3_rpm,
  };

  const cncData: CNCData = {
    curpos_x: 0, curpos_y: 0, curpos_z: 0, curpos_a: 0, curpos_c: 0,
    macpos_x: 0, macpos_y: 0, macpos_z: 0, macpos_a: 0, macpos_c: 0,
    feed_rate: 0, feed_override: 0, rapid_override: 0,
    feeder1_rpm: 0, feeder2_rpm: 0, feeder3_rpm: 0,
    powder_gas: 0, coaxial_gas: 0, shield_gas: 0,
    // 1) CNC nested 데이터 (GuiState에서 온 기본값)
    ...(flat.cnc_data as CNCData | undefined || {}),
    // 2) 위치: flat curpos_* (cnc_data 없을 때만)
    ...fromFlatPos,
    // 3) 가스/피더: 항상 Measurement(flat) 값을 우선 사용
    ...fromFlatGasFeeder,
  };

  const formatValue = (value: number | undefined, decimals: number = 2): string => {
    if (value === undefined) return '0.00';
    return value.toFixed(decimals);
  };

  const PositionBox = ({ title, prefix }: { title: string; prefix: 'curpos' | 'macpos' }) => (
    <div className="bg-gray-50 p-1.5 rounded-lg">
      <h4 className="text-xs font-bold text-gray-900 mb-0.5 pb-0.5 border-b border-gray-300">{title}</h4>
      <div className="space-y-0.5">
        {['x', 'y', 'z', 'a', 'c'].map(axis => (
          <div key={axis} className="flex items-center justify-center gap-2">
            <span className="text-xs font-medium text-gray-600 uppercase">{axis}:</span>
            <span className="text-xs text-gray-900 font-mono">
              {formatValue(cncData[`${prefix}_${axis}` as keyof CNCData] as number)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="h-full flex flex-col">
      {/* 시스템 상태 제목 */}
      <div className="flex items-center mb-2">
        <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center mr-3">
          <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
          </svg>
        </div>
        <h3 className="text-sm font-bold text-gray-900">시스템 상태</h3>
      </div>
      
      <div className="flex-1 overflow-y-auto space-y-2">
        {/* 현재 좌표와 기계 좌표를 한 행에 2열로 배치 */}
        <div className="grid grid-cols-2 gap-2">
          <PositionBox title="절대좌표/기계좌표" prefix="macpos" />
          <PositionBox title="상대좌표/현재좌표" prefix="curpos" />
        </div>
        
        {/* Feed Rate 카드 */}
        <div className="bg-gray-50 p-1.5 rounded-lg">
          <h4 className="text-xs font-bold text-gray-900 mb-0.5 pb-0.5 border-b border-gray-300">Feeder RPM</h4>
          <div className="grid grid-cols-3 gap-2">
            {[
              { name: 'Feeder1', rpm: cncData.feeder1_rpm },
              { name: 'Feeder2', rpm: cncData.feeder2_rpm },
              { name: 'Feeder3', rpm: cncData.feeder3_rpm }
            ].map((feeder) => (
              <div key={feeder.name} className="text-center">
                <div className="text-xs font-medium text-gray-900 mb-0.5">{feeder.name}</div>
                <div className="text-sm font-mono text-gray-900">{feeder.rpm || 0}</div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Gas 카드 */}
        <div className="bg-gray-50 p-1.5 rounded-lg">
          <h4 className="text-xs font-bold text-gray-900 mb-0.5 pb-0.5 border-b border-gray-300">Gas (L/min)</h4>
          <div className="grid grid-cols-3 gap-2">
            {[
              { name: 'Powder', value: cncData.powder_gas },
              { name: 'Coaxial', value: cncData.coaxial_gas },
              { name: 'Shield', value: cncData.shield_gas }
            ].map((gas) => (
              <div key={gas.name} className="text-center">
                <div className="text-xs font-medium text-gray-900 mb-0.5">{gas.name}</div>
                <div className="text-sm font-mono text-gray-900">{formatValue(gas.value)}</div>
              </div>
            ))}
          </div>
        </div>

        {/* 센서 연결 상태 */}
        <div className="bg-gray-50 p-1.5 rounded-lg">
          <h4 className="text-xs font-bold text-gray-900 mb-0.5 pb-0.5 border-b border-gray-300">센서 연결 상태</h4>
          <div className="space-y-0.5">
            {[
              { name: 'Basler Camera', key: 'camera' },
              { name: '2color Pyrometer', key: 'pyrometer' },
              { name: 'Laser', key: 'laser' },
              { name: 'CNC', key: 'cnc' }
            ].map((sensor) => {
              const status = systemStatus?.sensors?.[sensor.key as keyof typeof systemStatus.sensors] || false;
              return (
                <div key={sensor.key} className="flex justify-between items-center text-xs">
                  <span className="text-gray-700">{sensor.name}</span>
                  <div className={`w-3 h-3 rounded-full ${status ? 'bg-green-500' : 'bg-red-500'}`}></div>
                </div>
              );
            })}
          </div>
        </div>

        {/* sys연결 상태 */}
        <div className="bg-blue-50 p-2 rounded-lg border-2 border-blue-300">
          <h4 className="text-xs font-bold text-blue-900 mb-1 pb-0.5 border-b border-blue-300">sys연결 상태</h4>
          <div className="space-y-1">
            <div className="flex justify-between items-center">
              <span className="text-xs font-medium text-blue-800">Backend:</span>
              <div className={`w-3 h-3 rounded-full ${true ? 'bg-green-500' : 'bg-red-500'}`}></div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-xs font-medium text-blue-800">Recording:</span>
              <div className="w-3 h-3 rounded-full bg-gray-400"></div>
            </div>
          </div>
        </div>

        {/* 마지막 업데이트 시간 */}
        {latestData?.timestamp && (
          <div className="text-xs text-gray-400 text-center">
            Last Update: {new Date(latestData.timestamp).toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  );
}

