/**
 * 차트 컴포넌트 - Recharts를 사용한 실시간 데이터 시각화
 */
import React, { useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useSensorData } from '../hooks/useSensorData';

interface ChartsProps {
  chartType: 'meltpoolTemp' | 'meltpoolArea' | 'laserPower' | 'height';
}

const Charts: React.FC<ChartsProps> = ({ chartType }) => {
  const { historyData } = useSensorData();

  // 차트 데이터 변환
  const chartData = useMemo(() => {
    return historyData.map((data, index) => {
      const baseData = {
        time: index,
        timestamp: data.timestamp
      };

      // 정규화(flat) 우선: mpt, 1ct, melt_pool_area, outpower, setpower, ccd_height_avg_mm
      const d = data as Record<string, unknown>;
      switch (chartType) {
        case 'meltpoolTemp':
          return {
            ...baseData,
            meltPoolTemp: d.mpt ?? (data as any).pyrometer_data?.mpt ?? 0,
            oneColorTemp: d['1ct'] ?? (data as any).pyrometer_data?.['1ct'] ?? 0,
          };

        case 'meltpoolArea':
          return {
            ...baseData,
            meltPoolArea: d.melt_pool_area ?? (data as any).camera_data?.melt_pool_area ?? 0,
          };

        case 'laserPower':
          return {
            ...baseData,
            outputPower: d.outpower ?? (data as any).laser_data?.outpower ?? 0,
            setPower: d.setpower ?? (data as any).laser_data?.setpower ?? 0,
          };

        case 'height':
          return {
            ...baseData,
            // ✅ CCD 높이 대신 Measurement CSV의 Height(mm) 사용
            height: (data as any).height_mm ?? 0,
          };
        
        default:
          return baseData;
      }
    }).slice(-100); // 최근 100개 데이터만 표시
  }, [historyData, chartType]);

  const getChartConfig = () => {
    switch (chartType) {
      case 'meltpoolTemp':
        return {
          title: 'Melt Pool Temperature',
          yAxisLabel: 'Temperature (°C)',
          lines: [
            { dataKey: 'meltPoolTemp', name: 'Melt Pool Temp', color: '#ef4444', stroke: '#ef4444' },
            { dataKey: 'oneColorTemp', name: '1-Color Temp', color: '#22c55e', stroke: '#22c55e', strokeDasharray: '5 5' }
          ],
          // Y축 범위를 500 ~ 2000°C로 고정
          yAxisDomain: [500, 2000],
          yAxisTicks: undefined
        };
      
      case 'meltpoolArea':
        return {
          title: 'Melt Pool Area',
          yAxisLabel: 'Area (mm²)',
          lines: [
            { dataKey: 'meltPoolArea', name: 'Melt Pool Area', color: '#3b82f6', stroke: '#3b82f6' }
          ],
          yAxisDomain: [-0.5, 5],
          yAxisTicks: undefined
        };
      
      case 'laserPower':
        return {
          title: 'Laser Power',
          yAxisLabel: 'Power (W)',
          lines: [
            { dataKey: 'outputPower', name: 'Output Power', color: '#f97316', stroke: '#f97316' },
            { dataKey: 'setPower', name: 'Set Power', color: '#f97316', stroke: '#f97316', strokeDasharray: '5 5' }
          ],
          // Y축 범위를 0 ~ 1000W로 고정
          yAxisDomain: [0, 1000],
          yAxisTicks: undefined
        };
      
      case 'height':
        return {
          title: 'Height (Measurement CSV)',
          yAxisLabel: 'Height (mm)',
          lines: [
            { dataKey: 'height', name: 'Melt Pool Height', color: '#8b5cf6', stroke: '#8b5cf6' }
          ],
          yAxisDomain: [-1, 2],
          yAxisTicks: [-1, 0, 1, 2]
        };
      
      default:
        return {
          title: 'Unknown Chart',
          yAxisLabel: 'Value',
          lines: [],
          yAxisDomain: [0, 100],
          yAxisTicks: undefined
        };
    }
  };

  const config = getChartConfig();

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-300 rounded-lg shadow-lg">
          <p className="text-sm text-gray-600 mb-2">
            Time: {label}
          </p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {`${entry.name}: ${entry.value?.toFixed(2) || 'N/A'}`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="h-full bg-white rounded-xl shadow-lg p-2">
      <div className="h-full flex flex-col">
        {/* 차트 제목 */}
        <div className="mb-2">
          <h3 className="text-lg font-semibold text-gray-800 text-center">
            {config.title}
          </h3>
          <p className="text-sm text-gray-500 text-center">
            {config.yAxisLabel}
          </p>
        </div>

        {/* 차트 영역 */}
        <div className="flex-1 min-h-0">
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={chartData}
                margin={{
                  top: 10,
                  right: 30,
                  left: 20,
                  bottom: 20,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="time"
                  stroke="#6b7280"
                  fontSize={12}
                  tick={{ fontSize: 10 }}
                />
                <YAxis 
                  domain={config.yAxisDomain}
                  {...(config.yAxisTicks && { ticks: config.yAxisTicks })}
                  stroke="#6b7280"
                  fontSize={12}
                  tick={{ fontSize: 10 }}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend 
                  wrapperStyle={{ fontSize: '12px' }}
                  iconType="line"
                />
                
                {config.lines.map((line, index) => (
                  <Line
                    key={index}
                    type="monotone"
                    dataKey={line.dataKey}
                    stroke={line.stroke}
                    strokeWidth={2}
                    dot={false}
                    name={line.name}
                    strokeDasharray={line.strokeDasharray}
                    connectNulls={false}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center">
              <div className="text-center text-gray-500">
                <div className="text-lg mb-2">📊</div>
                <div className="text-sm">데이터를 수집 중입니다...</div>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default Charts;