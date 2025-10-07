import React, { useState } from 'react';
import Header from './components/Header';
import CNCStatus from './components/CNCStatus';
import ConnectionStatus from './components/ConnectionStatus';
import CameraView from './components/CameraView';
import Charts from './components/Charts';
import EmergencyModal from './components/EmergencyModal';

function App() {
  const [emergency, setEmergency] = useState(false);
  const [showEmergencyModal, setShowEmergencyModal] = useState(false);

  const handleEmergencyToggle = (newEmergency: boolean) => {
    if (newEmergency && !emergency) {
      // 비상 정지 요청 시 모달 표시
      setShowEmergencyModal(true);
    } else {
      setEmergency(newEmergency);
    }
  };

  const handleEmergencyConfirm = () => {
    setEmergency(true);
    setShowEmergencyModal(false);
    // 여기에 실제 비상 정지 로직 추가
    console.log('🚨 비상 정지 실행됨');
  };

  const handleEmergencyCancel = () => {
    setShowEmergencyModal(false);
  };

  return (
    <div className="h-screen bg-gray-100 flex flex-col items-center p-2 overflow-hidden">
      {/* Header */}
      <Header emergency={emergency} onEmergencyToggle={handleEmergencyToggle} />
      
      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden w-[98%] my-4">
        {/* Left Panel - CNC Status & Connection Status */}
        <div className="w-80 bg-white shadow-lg rounded-2xl flex flex-col">
          <div className="flex-[2] p-3 rounded-t-2xl">
            <CNCStatus />
          </div>
          <div className="flex-[1] border-t border-gray-200 p-2 rounded-b-2xl">
            <ConnectionStatus />
          </div>
        </div>
    
        {/* Right Panel - Camera View & Charts */}
        <div className="flex-1 flex flex-col p-3 space-y-2">
          {/* Top Row - Camera View & Melt Pool Area Chart */}
          <div className="flex space-x-2 h-1/2">
            <div className="flex-1">
              <CameraView />
            </div>
            <div className="flex-1">
              <Charts chartType="meltpoolArea" />
            </div>
          </div>
          
          {/* Bottom Row - Temperature & Laser Power Charts */}
          <div className="flex space-x-2 h-1/2">
            <div className="flex-1">
              <Charts chartType="meltpoolTemp" />
            </div>
            <div className="flex-1">
              <Charts chartType="laserPower" />
            </div>
          </div>
        </div>
      </div>
      
      {/* Bottom Bar */}
      <div className="h-8 bg-white border-t border-gray-200 flex items-center justify-between px-4 w-[98%] rounded-xl shadow-sm">
        <div className="text-xs text-gray-500">
          Copyright by KITECH V2.0 - Backend API Connected
        </div>
        <div className="flex space-x-2">
          <div className="text-xs text-gray-500">
            React + Electron + FastAPI
          </div>
        </div>
      </div>

      {/* Emergency Modal */}
      <EmergencyModal
        isOpen={showEmergencyModal}
        onClose={handleEmergencyCancel}
        onConfirm={handleEmergencyConfirm}
      />
    </div>
  );
}

export default App;