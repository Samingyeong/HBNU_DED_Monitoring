/**
 * 헤더 컴포넌트 - 시스템 제어 및 상태 표시
 */
import React, { useState, useEffect } from 'react';
import { useAutoSave } from '../hooks/useAutoSave';
import { useSensorData } from '../hooks/useSensorData';

interface HeaderProps {
  emergency: boolean;
  onEmergencyToggle: (emergency: boolean) => void;
}

const Header: React.FC<HeaderProps> = ({ emergency, onEmergencyToggle }) => {
  const [isSavingLoading, setIsSavingLoading] = useState(false);
  const [saveFolderName, setSaveFolderName] = useState('');
  
  // 실제 센서 데이터
  const { 
    isConnected, 
    saveStatus, 
    error: sensorError,
    startSaving, 
    stopSaving 
  } = useSensorData();
  
  // 자동저장 시스템
  const { 
    isAutoSaving, 
    currentSession, 
    hasException, 
    error: autoSaveError,
    resetAutoSave 
  } = useAutoSave();

  // 자동저장 상태에 따라 수동 저장 상태 동기화
  useEffect(() => {
    if (isAutoSaving && !saveStatus?.is_saving) {
      console.log('🔄 자동저장 활성화됨:', currentSession);
    } else if (!isAutoSaving && saveStatus?.is_saving && !isSavingLoading) {
      console.log('🔄 자동저장 비활성화됨');
    }
  }, [isAutoSaving, saveStatus?.is_saving, isSavingLoading, currentSession]);

  const handleSaveToggle = async () => {
    if (isSavingLoading) return;

    try {
      setIsSavingLoading(true);
      
      if (saveStatus?.is_saving) {
        await stopSaving();
        resetAutoSave(); // 자동저장 상태도 리셋
        console.log('수동 저장 중지됨');
      } else {
        const folderName = saveFolderName || `monitoring_${new Date().toISOString().slice(0, 19).replace(/[:.]/g, '-')}`;
        await startSaving(folderName);
        console.log('수동 저장 시작됨:', folderName);
      }
    } catch (error) {
      console.error('저장 토글 실패:', error);
    } finally {
      setIsSavingLoading(false);
    }
  };

  const handleEmergencyToggle = () => {
    onEmergencyToggle(!emergency);
  };

  return (
    <div className="w-full bg-white shadow-lg rounded-2xl p-4 mb-4">
      <div className="flex items-center justify-between">
        {/* 왼쪽: 로고 및 제목 */}
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center">
            <span className="text-white font-bold text-xl">H</span>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-800">DED Monitoring System</h1>
            <p className="text-sm text-gray-500">Real-time Process Monitoring</p>
          </div>
        </div>

        {/* 중앙: 시스템 상태 */}
        <div className="flex items-center space-x-6">
          {/* 백엔드 연결 상태 */}
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm font-medium text-gray-700">
              Backend: {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          {/* 저장 상태 */}
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${
              saveStatus?.is_saving 
                ? (isAutoSaving ? 'bg-green-500' : 'bg-blue-500')
                : 'bg-gray-400'
            }`}></div>
            <span className="text-sm font-medium text-gray-700">
              Recording: {saveStatus?.is_saving ? (isAutoSaving ? 'Auto-Active' : 'Manual-Active') : 'Inactive'}
            </span>
          </div>

          {/* Exception 상태 */}
          {hasException && (
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <span className="text-sm font-medium text-red-700">
                Exception Detected
              </span>
            </div>
          )}

          {/* 자동저장 에러 */}
          {autoSaveError && (
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <span className="text-sm font-medium text-yellow-700">
                Auto-Save Error
              </span>
            </div>
          )}
        </div>

        {/* 오른쪽: 컨트롤 버튼들 */}
        <div className="flex items-center space-x-3">
          {/* 저장 폴더 입력 */}
          {!saveStatus?.is_saving && (
            <input
              type="text"
              placeholder="폴더명"
              value={saveFolderName}
              onChange={(e) => setSaveFolderName(e.target.value)}
              className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          )}

          {/* 저장 토글 버튼 */}
          <button
            onClick={handleSaveToggle}
            disabled={isSavingLoading || !isConnected}
            className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
              saveStatus?.is_saving
                ? 'bg-red-500 hover:bg-red-600 text-white'
                : 'bg-blue-500 hover:bg-blue-600 text-white'
            } ${(isSavingLoading || !isConnected) ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {isSavingLoading ? (
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Processing...</span>
              </div>
            ) : saveStatus?.is_saving ? (
              'Stop Recording'
            ) : (
              'Start Recording'
            )}
          </button>

          {/* 비상 정지 버튼 */}
          <button
            onClick={handleEmergencyToggle}
            className={`px-6 py-2 text-sm font-bold rounded-lg transition-colors ${
              emergency
                ? 'bg-red-600 hover:bg-red-700 text-white'
                : 'bg-gray-300 hover:bg-gray-400 text-gray-700'
            }`}
          >
            {emergency ? 'EMERGENCY STOP' : 'EMERGENCY'}
          </button>

          {/* 설정 버튼 */}
          <button className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>
        </div>
      </div>

      {/* 저장 경로 및 상태 표시 */}
      {saveStatus?.is_saving && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">Saving to:</span>
              <span className="text-sm font-mono text-blue-600 bg-blue-50 px-2 py-1 rounded">
                {currentSession || saveStatus.save_path || saveFolderName || `monitoring_${new Date().toISOString().slice(0, 19).replace(/[:.]/g, '-')}`}
              </span>
            </div>
            
            {isAutoSaving && (
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-xs text-green-600 font-medium">Auto-Save Active</span>
              </div>
            )}
          </div>
          
          {(autoSaveError || sensorError) && (
            <div className="mt-2 text-xs text-red-600 bg-red-50 px-2 py-1 rounded">
              {autoSaveError || sensorError}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Header;