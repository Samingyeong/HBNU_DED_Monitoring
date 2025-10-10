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
      <div className="flex-1 flex flex-col xl:flex-row overflow-hidden w-[98%] mt-0 xl:mt-1 mb-2 xl:mb-4 gap-2 xl:gap-2">
        {/* Left Panel - CNC Status Only */}
        <div className="w-full xl:w-80 bg-white shadow-lg rounded-2xl flex flex-col">
          <div className="flex-1 px-2 xl:px-3 pt-2 xl:pt-3 pb-0 xl:pb-0">
            <CNCStatus />
          </div>
        </div>
    
        {/* Right Panel - 2열 3행 레이아웃 */}
        <div className="flex-1 flex flex-col xl:flex-row gap-2">
          {/* 1열 - 카메라 및 ToolPath */}
          <div className="w-full xl:w-1/3 flex flex-col gap-2">
            {/* 1행 - Basler 카메라 */}
            <div className="flex-1">
              <CameraView cameraType="basler" />
            </div>
            
            {/* 2행 - HikRobot 카메라 */}
            <div className="flex-1">
              <CameraView cameraType="hikrobot" />
            </div>
            
            {/* 3행 - ToolPath (준비중) */}
            <div className="flex-1 bg-white shadow-lg rounded-2xl flex items-center justify-center">
              <div className="text-center">
                <div className="w-8 h-8 xl:w-16 xl:h-16 mx-auto mb-2 xl:mb-3 bg-gray-200 rounded-xl flex items-center justify-center">
                  <svg className="w-4 h-4 xl:w-8 xl:h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m-6 3l6-3" />
                  </svg>
                </div>
                <h3 className="text-sm xl:text-lg font-semibold text-gray-700 mb-1">ToolPath</h3>
                <p className="text-xs xl:text-sm text-gray-500">준비중입니다</p>
              </div>
            </div>
          </div>

          {/* 2열 - 차트들 */}
          <div className="w-full xl:w-2/3 flex flex-col gap-2">
            {/* 1행 - Melt Pool Area */}
            <div className="flex-1">
              <Charts chartType="meltpoolArea" />
            </div>
            
            {/* 2행 - Height (CCD 카메라) */}
            <div className="flex-1">
              <Charts chartType="height" />
            </div>
            
            {/* 3행 - Temperature & Laser Power (2열로 나눔) */}
            <div className="flex-1 flex flex-col xl:flex-row gap-2">
              {/* 왼쪽 - Melt Pool Temperature */}
              <div className="flex-1">
                <Charts chartType="meltpoolTemp" />
              </div>
              
              {/* 오른쪽 - Laser Power */}
              <div className="flex-1">
                <Charts chartType="laserPower" />
              </div>
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