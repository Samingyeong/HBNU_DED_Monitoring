import React, { useState } from 'react';
import Header from './components/Header';
import CNCStatus from './components/CNCStatus';
import ConnectionStatus from './components/ConnectionStatus';
import CameraView from './components/CameraView';
import Charts from './components/Charts';
import EmergencyModal from './components/EmergencyModal';
import InitialSetupModal from './components/InitialSetupModal';
import ToolPath from './components/ToolPath';
import { ApiService } from './services/api';

function App() {
  const [emergency, setEmergency] = useState(false);
  const [showEmergencyModal, setShowEmergencyModal] = useState(false);
  const [showInitialSetup, setShowInitialSetup] = useState(true);
  const [processName, setProcessName] = useState('');
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

  const handleInitialSetupComplete = async (process: string) => {
    setProcessName(process);
    
    // 폴더명 자동 생성: YYMMDD_HHMMSS_공정명
    const now = new Date();
    const year = String(now.getFullYear()).slice(2);
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hour = String(now.getHours()).padStart(2, '0');
    const minute = String(now.getMinutes()).padStart(2, '0');
    const second = String(now.getSeconds()).padStart(2, '0');
    
    const generatedFolderName = `${year}${month}${day}_${hour}${minute}${second}_${process}`;
    setFolderName(generatedFolderName);

    // 백엔드에 공정명 전달 (자동저장 세션 ID에 반영되도록)
    try {
      await ApiService.setProcessName({ process_name: process });
    } catch (e) {
      console.error('공정명 설정 API 호출 실패:', e);
    }
    
    setShowInitialSetup(false);
    
    console.log('설정 완료:', {
      processName: process,
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
    
        {/* Right Panel - 2열 레이아웃 */}
        <div className="flex-1 flex flex-col xl:flex-row gap-2">
          {/* 1열 - 카메라 + 툴패스 (세로 배치) */}
          <div className="w-full xl:w-[380px] flex flex-col gap-2">
            {/* 바슬러 카메라 (카드 아웃라인을 내부 영상 높이에 맞게 확대) */}
            <div className="h-[380px]">
              <CameraView cameraType="basler" />
            </div>
            
            {/* 하이크로봇 카메라 (장비 SW와 카메라 자원 충돌 때문에 임시 비활성화)
            <div className="h-[200px]">
              <CameraView cameraType="hikrobot" />
            </div>
            */}
            
            {/* 툴패스 (정사각형) */}
            <div className="flex-1 min-h-[300px]">
              <ToolPath className="h-full w-full" />
            </div>
          </div>

          {/* 2열 - 차트들 */}
          <div className="flex-1 flex flex-col gap-2">
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
      
      {/* Bottom Bar (정보만 표시) */}
      <div className="bg-white border-t border-gray-200 flex items-center justify-between px-4 py-2 w-[98%] rounded-xl shadow-sm">
        {/* 좌측: 여백 또는 간단한 설명 자리 (현재 비워둠) */}
        <div />

        {/* 우측: 정보 */}
        <div className="flex flex-col items-end space-y-1 text-xs text-gray-500">
          <div className="text-xs text-gray-500">
            Copyright by KITECH V2.0
          </div>
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