import React, { useState } from 'react';

interface EmergencyModalProps {
  isOpen: boolean;
  onClose: () => void;
  emergency: boolean;
  onEmergencyToggle: (emergency: boolean) => void;
}

export default function EmergencyModal({ 
  isOpen, 
  onClose, 
  emergency, 
  onEmergencyToggle 
}: EmergencyModalProps) {
  const [localEmergency, setLocalEmergency] = useState(emergency);

  const handleEmergencyToggle = () => {
    const newEmergency = !localEmergency;
    setLocalEmergency(newEmergency);
    onEmergencyToggle(newEmergency);
  };

  const handleSave = () => {
    onClose();
  };

  const handleCancel = () => {
    setLocalEmergency(emergency); // 원래 상태로 복원
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Emergency 설정</h2>
            <button
              onClick={handleCancel}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="mb-6">
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className={`w-4 h-4 rounded-full ${localEmergency ? 'bg-red-500' : 'bg-green-500'}`} />
                <span className="text-lg font-medium text-gray-900">Emergency 상태</span>
              </div>
              <button
                onClick={handleEmergencyToggle}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  localEmergency 
                    ? 'bg-red-100 text-red-700 hover:bg-red-200' 
                    : 'bg-green-100 text-green-700 hover:bg-green-200'
                }`}
              >
                {localEmergency ? 'ON' : 'OFF'}
              </button>
            </div>
            
            <p className="text-sm text-gray-600 mt-3">
              Emergency가 ON 상태일 때는 모든 기계 동작이 중단됩니다.
            </p>
          </div>

          <div className="flex space-x-3">
            <button
              onClick={handleSave}
              className="flex-1 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors font-medium"
            >
              저장
            </button>
            <button
              onClick={handleCancel}
              className="flex-1 bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors font-medium"
            >
              취소
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
