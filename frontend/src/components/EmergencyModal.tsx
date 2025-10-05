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
  const [showConfirm, setShowConfirm] = useState(false);

  const handleEmergencyClick = () => {
    if (emergency) {
      // 이미 Emergency 상태라면 바로 해제
      onEmergencyToggle(false);
      onClose();
    } else {
      // Emergency 활성화 확인
      setShowConfirm(true);
    }
  };

  const handleConfirmEmergency = () => {
    onEmergencyToggle(true);
    setShowConfirm(false);
    onClose();
  };

  const handleCancel = () => {
    setShowConfirm(false);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl shadow-xl max-w-md w-full mx-4">
        <div className="p-8 text-center">
          {!showConfirm ? (
            <>
              <div className="mb-6">
                <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Emergency</h2>
                <p className="text-gray-600">
                  {emergency ? 'Emergency 상태를 해제하시겠습니까?' : 'Emergency를 활성화하시겠습니까?'}
                </p>
              </div>

              <div className="flex space-x-3">
                <button
                  onClick={handleCancel}
                  className="flex-1 bg-gray-200 text-gray-800 px-6 py-3 rounded-xl hover:bg-gray-300 transition-colors font-medium"
                >
                  취소
                </button>
                <button
                  onClick={handleEmergencyClick}
                  className={`flex-1 px-6 py-3 rounded-xl font-medium transition-colors ${
                    emergency 
                      ? 'bg-green-500 text-white hover:bg-green-600' 
                      : 'bg-red-500 text-white hover:bg-red-600'
                  }`}
                >
                  {emergency ? '해제' : 'Emergency'}
                </button>
              </div>
            </>
          ) : (
            <>
              <div className="mb-6">
                <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold text-red-600 mb-2">정말 멈추시겠습니까?</h2>
                <p className="text-gray-600 mb-4">
                  Emergency를 활성화하면 모든 센서와 기계 동작이 즉시 중단됩니다.
                </p>
              </div>

              <div className="flex space-x-3">
                <button
                  onClick={handleCancel}
                  className="flex-1 bg-gray-200 text-gray-800 px-6 py-3 rounded-xl hover:bg-gray-300 transition-colors font-medium"
                >
                  취소
                </button>
                <button
                  onClick={handleConfirmEmergency}
                  className="flex-1 bg-red-500 text-white px-6 py-3 rounded-xl hover:bg-red-600 transition-colors font-medium"
                >
                  확인
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
