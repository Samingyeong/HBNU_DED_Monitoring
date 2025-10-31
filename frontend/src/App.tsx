import React, { useState } from 'react';
import Header from './components/Header';
import CNCStatus from './components/CNCStatus';
import ConnectionStatus from './components/ConnectionStatus';
import CameraView from './components/CameraView';
import Charts from './components/Charts';
import EmergencyModal from './components/EmergencyModal';
import InitialSetupModal from './components/InitialSetupModal';
// ToolPath 기능 제거

function App() {
  const [emergency, setEmergency] = useState(false);
  const [showEmergencyModal, setShowEmergencyModal] = useState(false);
  const [showInitialSetup, setShowInitialSetup] = useState(true);
  const [operatorName, setOperatorName] = useState('');
  
  const [folderName, setFolderName] = useState('');

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

  const handleInitialSetupComplete = (operator: string) => {
    setOperatorName(operator);
    
    // 폴더명 자동 생성: YYYYMMDD_HHMM_작업자명
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hour = String(now.getHours()).padStart(2, '0');
    const minute = String(now.getMinutes()).padStart(2, '0');
    
    const generatedFolderName = `${year}${month}${day}_${hour}${minute}_${operator}`;
    setFolderName(generatedFolderName);
    
    setShowInitialSetup(false);
    
    console.log('설정 완료:', {
      operatorName: operator,
      folderName: generatedFolderName
    });
  };

  return (
    <div className="h-screen bg-gray-100 flex flex-col items-center p-2 overflow-hidden">
      {/* Header */}
      <Header 
        emergency={emergency} 
        onEmergencyToggle={handleEmergencyToggle}
        folderName={folderName}
      />
      
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
          {/* 1열 - 카메라 */}
          <div className="w-full xl:w-1/3 flex flex-col gap-2">
            {/* 1행 - Basler 카메라 */}
            <div className="flex-1">
              <CameraView cameraType="basler" />
            </div>
            
            {/* 2행 - HikRobot 카메라 */}
            <div className="flex-1">
              <CameraView cameraType="hikrobot" />
            </div>
            
            {/* ToolPath 제거 */}
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
          Copyright by KITECH V2.0
        </div>
        <div className="flex space-x-2">
          <div className="text-xs text-gray-500">
            React + Electron + FastAPI
          </div>
        </div>
      </div>

      {/* Initial Setup Modal */}
      <InitialSetupModal
        isOpen={showInitialSetup}
        onComplete={handleInitialSetupComplete}
      />

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