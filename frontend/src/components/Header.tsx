/**
 * 헤더 컴포넌트 - 시스템 제어 및 상태 표시
 */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAutoSave } from '../hooks/useAutoSave';
import { useSensorData } from '../hooks/useSensorData';
import ConfigViewerModal from './ConfigViewerModal';
import { ApiService } from '../services/api';

interface HeaderProps {
  emergency: boolean;
  onEmergencyToggle: (emergency: boolean) => void;
  folderName?: string;
}

const Header: React.FC<HeaderProps> = ({ emergency, onEmergencyToggle, folderName }) => {
  const [isSavingLoading, setIsSavingLoading] = useState(false);
  const [saveFolderName, setSaveFolderName] = useState('');
  const [tempStorageInfo, setTempStorageInfo] = useState<any>(null);
  const [showConnectionModal, setShowConnectionModal] = useState(false);
  const [showConfigModal, setShowConfigModal] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  // 시간 줄 및 모달에서 사용할 공정명/작업자
  const [processNameInput, setProcessNameInput] = useState('');
  const [operatorNameInput, setOperatorNameInput] = useState('');
  const [currentProcessLabel, setCurrentProcessLabel] = useState<string | null>(null);
  const [isProcessSaving, setIsProcessSaving] = useState(false);
  
  // 실제 센서 데이터
  const { 
    isConnected, 
    saveStatus, 
    systemStatus,
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

  // 현재 시간 실시간 업데이트
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // 임시 저장 정보 주기적으로 업데이트
  useEffect(() => {
    const fetchTempStorageInfo = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/save/temp-info', {
          timeout: 3000 // 3초 타임아웃
        });
        setTempStorageInfo(response.data);
      } catch (error: any) {
        // 404나 503 에러는 정상 (임시 저장 데이터가 없는 경우)
        if (error.response?.status === 404 || error.response?.status === 503) {
          setTempStorageInfo(null);
        } else if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
          // 연결 거부 에러는 조용히 무시 (백엔드가 아직 시작 안됨)
          console.warn('⚠️ 백엔드 연결 대기 중...');
        } else {
          console.error('임시 저장 정보 조회 실패:', error.message);
        }
      }
    };

    // 초기 로드는 1초 지연 (백엔드 초기화 대기)
    const initialTimeout = setTimeout(fetchTempStorageInfo, 1000);
    
    // 5초마다 임시 저장 정보 업데이트
    const interval = setInterval(fetchTempStorageInfo, 5000);

    return () => {
      clearTimeout(initialTimeout);
      clearInterval(interval);
    };
  }, []);

  // Save Now: 임시저장 중인 데이터를 즉시 디스크에 저장 (자동저장 유지)
  const handleSaveNow = async () => {
    if (isSavingLoading || !tempStorageInfo?.has_temp_data) return;
    try {
      setIsSavingLoading(true);
      const inputValue = saveFolderName?.trim();
      const isAbsolutePath = !!inputValue && (inputValue.includes(':') || inputValue.startsWith('\\') || inputValue.includes('\\'));
      const body: any = isAbsolutePath
        ? { dest_path: inputValue }
        : { folder_name: inputValue || `manual_save_${new Date().toISOString().slice(0, 19).replace(/[:.]/g, '-')}` };

      const response = await axios.post('http://127.0.0.1:8000/api/save/temp-to-permanent', body);
      console.log('✅ 즉시 저장 완료:', response.data.save_path);
    } catch (error) {
      console.error('즉시 저장 중 오류:', error);
    } finally {
      setIsSavingLoading(false);
    }
  };

  const handleSaveTempData = async () => {
    if (isSavingLoading || !tempStorageInfo?.has_temp_data) return;

    try {
      setIsSavingLoading(true);
      
      const folderName = saveFolderName || `temp_save_${new Date().toISOString().slice(0, 19).replace(/[:.]/g, '-')}`;
      
      const response = await axios.post('http://127.0.0.1:8000/api/save/temp-to-permanent', {
        folder_name: folderName
      });
      
      console.log('✅ 임시 데이터 영구 저장 완료:', response.data.save_path);
      setTempStorageInfo(null); // 임시 저장 정보 초기화
      setSaveFolderName(''); // 폴더명 초기화
    } catch (error) {
      console.error('임시 데이터 저장 실패:', error);
    } finally {
      setIsSavingLoading(false);
    }
  };

  const handleEmergencyToggle = () => {
    onEmergencyToggle(!emergency);
  };

  // 상단 시간 줄/모달에서 공정명/작업자 적용
  const handleProcessNameApply = async () => {
    const proc = processNameInput.trim();
    const oper = operatorNameInput.trim();

    if (!proc) {
      alert('공정명을 입력해주세요.');
      return;
    }
    if (!oper) {
      alert('작업자 이름을 입력해주세요.');
      return;
    }

    const combined = `${proc}_${oper}`;

    try {
      setIsProcessSaving(true);
      await ApiService.setProcessName({ process_name: combined });
      setCurrentProcessLabel(combined);
      console.log('✅ 공정명/이름 설정:', combined);
    } catch (e: any) {
      console.error('공정명 설정 실패:', e);
      alert('공정명을 설정하는 중 오류가 발생했습니다. 콘솔 로그를 확인해주세요.');
    } finally {
      setIsProcessSaving(false);
    }
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

        {/* 오른쪽: 시간 및 컨트롤 버튼들 */}
        <div className="flex items-center space-x-4">
          {/* 현재 시간 + 공정명/작업자 (한 줄) */}
          <div className="flex flex-col items-end space-y-1">
            <div className="flex items-center space-x-3">
              <div className="text-base font-medium text-gray-600">
                {currentTime.toLocaleDateString('ko-KR', { 
                  year: 'numeric', 
                  month: '2-digit', 
                  day: '2-digit' 
                })} {currentTime.toLocaleTimeString('ko-KR', { 
                  hour12: true, 
                  hour: 'numeric', 
                  minute: '2-digit', 
                  second: '2-digit' 
                })}
              </div>
              <div className="flex items-center space-x-3 text-sm text-gray-700">
                <span className="font-medium">공정명</span>
                <input
                  type="text"
                  value={processNameInput}
                  onChange={(e) => setProcessNameInput(e.target.value)}
                  placeholder="예: 공정A"
                  className="px-3 py-2 border rounded-lg w-40"
                />
                <span className="font-medium">작업자명</span>
                <input
                  type="text"
                  value={operatorNameInput}
                  onChange={(e) => setOperatorNameInput(e.target.value)}
                  placeholder="예: 홍길동"
                  className="px-3 py-2 border rounded-lg w-32"
                />
                <button
                  onClick={handleProcessNameApply}
                  disabled={isProcessSaving}
                  className={`px-3 py-2 text-xs rounded-lg border ${
                    isProcessSaving
                      ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                      : 'bg-blue-50 text-blue-700 border-blue-300 hover:bg-blue-100'
                  }`}
                >
                  {isProcessSaving ? '저장중' : '적용'}
                </button>
              </div>
            </div>
            {currentProcessLabel && (
              <div className="text-[11px] text-gray-500">
                현재 공정: <span className="font-medium">{currentProcessLabel}</span>
              </div>
            )}
          </div>
          
          {/* 폴더명 / 현재 공정 표시 (파란 박스) */}
          {(currentProcessLabel || folderName) && (
            <div className="px-3 py-2 text-sm bg-blue-50 border border-blue-300 rounded-lg text-blue-700 font-medium">
              {currentProcessLabel || folderName}
            </div>
          )}

          {/* Save Now: 자동저장 중에도 사용 가능 */}
          {tempStorageInfo?.has_temp_data && (
            <>
              <input
                type="text"
                value={saveFolderName}
                onChange={(e) => setSaveFolderName(e.target.value)}
                placeholder="절대 경로 또는 폴더명"
                className="px-3 py-2 text-sm border rounded-lg"
              />
              <button
                onClick={handleSaveNow}
                disabled={isSavingLoading || !isConnected}
                className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors bg-green-500 hover:bg-green-600 text-white ${
                  (isSavingLoading || !isConnected) ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {isSavingLoading ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Saving...</span>
                  </div>
                ) : (
                  `Save Now (${tempStorageInfo.data_count})`
                )}
              </button>
            </>
          )}

          {/* Recording 버튼 제거됨 */}

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
          <button 
            onClick={() => setShowConfigModal(true)}
            className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
            title="설정 파일 보기"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>
        </div>
      </div>

      {/* 저장 경로 및 상태 표시 */}
      {(saveStatus?.is_saving || tempStorageInfo?.has_temp_data) && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">
                {saveStatus?.is_saving ? 'Saving to:' : 'Temp Data:'}
              </span>
              <span className={`text-sm font-mono px-2 py-1 rounded ${
                saveStatus?.is_saving 
                  ? 'text-blue-600 bg-blue-50'
                  : 'text-yellow-600 bg-yellow-50'
              }`}>
                {saveStatus?.is_saving 
                  ? (currentSession || saveStatus.save_path || saveFolderName || `monitoring_${new Date().toISOString().slice(0, 19).replace(/[:.]/g, '-')}`)
                  : `${tempStorageInfo.session_id} (${tempStorageInfo.data_count} items)`
                }
              </span>
            </div>
            
            <div className="flex items-center space-x-2">
              {isAutoSaving && (
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-xs text-green-600 font-medium">Auto-Save Active</span>
                </div>
              )}
              
              {tempStorageInfo?.has_temp_data && (
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
                  <span className="text-xs text-yellow-600 font-medium">
                    Temp Storage ({Math.floor(tempStorageInfo.remaining_time / 60)}:{(tempStorageInfo.remaining_time % 60).toString().padStart(2, '0')})
                  </span>
                </div>
              )}
            </div>
          </div>
          
          {(autoSaveError || sensorError) && (
            <div className="mt-2 text-xs text-red-600 bg-red-50 px-2 py-1 rounded">
              {autoSaveError || sensorError}
            </div>
          )}
        </div>
      )}

      {/* Config 파일 뷰어 모달 */}
      <ConfigViewerModal
        isOpen={showConfigModal}
        onClose={() => setShowConfigModal(false)}
      />

      {/* 연결 상태 모달 */}
      {showConnectionModal && (
        <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 max-w-[90vw] max-h-[80vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">연결 상태</h2>
              <button 
                onClick={() => setShowConnectionModal(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            
            {/* 공정명 / 작업자명 설정 (연결 상태 모달 상단) */}
            <div className="mb-4 p-3 rounded-lg bg-gray-50">
              <div className="text-xs font-semibold text-gray-700 mb-2">
                공정명 / 작업자 설정
              </div>
              <div className="space-y-2 text-xs">
                <div className="flex items-center space-x-2">
                  <span className="w-14 text-gray-700">공정명</span>
                  <input
                    type="text"
                    value={processNameInput}
                    onChange={(e) => setProcessNameInput(e.target.value)}
                    placeholder="예: 공정A"
                    className="flex-1 px-2 py-1 border rounded-lg"
                  />
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-14 text-gray-700">작업자</span>
                  <input
                    type="text"
                    value={operatorNameInput}
                    onChange={(e) => setOperatorNameInput(e.target.value)}
                    placeholder="예: 홍길동"
                    className="flex-1 px-2 py-1 border rounded-lg"
                  />
                  <button
                    onClick={handleProcessNameApply}
                    disabled={isProcessSaving}
                    className={`px-3 py-1 rounded-lg border ${
                      isProcessSaving
                        ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                        : 'bg-blue-50 text-blue-700 border-blue-300 hover:bg-blue-100'
                    }`}
                  >
                    {isProcessSaving ? '저장중' : '적용'}
                  </button>
                </div>
                {currentProcessLabel && (
                  <div className="text-[11px] text-gray-700 mt-1">
                    현재 공정: <span className="font-medium">{currentProcessLabel}</span>
                  </div>
                )}
              </div>
            </div>
            
            {/* 백엔드 연결 상태 */}
            <div className="mb-4 p-3 bg-blue-50 rounded">
              <h3 className="font-semibold mb-2">백엔드 연결</h3>
              <div className="flex justify-between">
                <span>Backend API:</span>
                <span className={isConnected ? 'text-green-600' : 'text-red-600'}>
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>WebSocket:</span>
                <span className={isConnected ? 'text-green-600' : 'text-red-600'}>
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
            </div>
            
            {/* 센서 연결 상태 */}
            <div>
              <h3 className="font-semibold mb-2">센서 연결 상태</h3>
              {systemStatus?.sensors ? (
                <div className="space-y-2">
                  {Object.entries(systemStatus.sensors).map(([key, status]) => {
                    // Hik 카메라는 UI에서 숨김
                    if (key === 'hik_camera_1' || key === 'hik_camera_2') {
                      return null;
                    }
                    const labels: { [key: string]: string } = {
                      camera: 'Basler Camera',
                      pyrometer: '2color Pyrometer',
                      laser: 'Laser',
                      cnc: 'CNC'
                    };
                    
                    return (
                      <div key={key} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                        <span>{labels[key] || key}</span>
                        <div className="flex items-center space-x-2">
                          <div className={`w-3 h-3 rounded-full ${status ? 'bg-green-500' : 'bg-red-500'}`}></div>
                          <span className={status ? 'text-green-600' : 'text-red-600'}>
                            {status ? 'Connected' : 'Disconnected'}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="text-gray-500">센서 상태 정보를 불러오는 중...</p>
              )}
            </div>
            
            <div className="mt-4">
              <button
                onClick={() => setShowConnectionModal(false)}
                className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
              >
                닫기
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Header;