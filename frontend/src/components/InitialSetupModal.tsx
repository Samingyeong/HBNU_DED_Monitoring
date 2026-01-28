/**
 * 초기 설정 모달 - 작업자명 및 Gcode 폴더 선택
 */
import React, { useState } from 'react';

interface InitialSetupModalProps {
  isOpen: boolean;
  onComplete: (combinedName: string) => void;
}

const InitialSetupModal: React.FC<InitialSetupModalProps> = ({ isOpen, onComplete }) => {
  const [processName, setProcessName] = useState('');
  const [operatorName, setOperatorName] = useState('');
  

  if (!isOpen) return null;

  // NC 업로드 제거: 파일 선택 기능 비활성화

  const handleSubmit = async () => {
    if (!processName.trim()) {
      alert('공정명을 입력해주세요.');
      return;
    }

    if (!operatorName.trim()) {
      alert('이름을 입력해주세요.');
      return;
    }

    // 공정명_이름 결합해서 전달 (예: 공정A_홍길동)
    const combinedName = `${processName.trim()}_${operatorName.trim()}`;
    onComplete(combinedName);
  };

  return (
    <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-70 flex items-center justify-center" style={{ zIndex: 9999 }}>
      <div className="bg-white rounded-2xl p-8 w-[500px] max-w-[90vw] shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="text-center mb-6">
          <div className="w-16 h-16 bg-blue-600 rounded-xl flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-2xl">H</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">공정 시작 설정</h2>
          <p className="text-sm text-gray-500">공정명과 작업자 이름을 입력해주세요</p>
        </div>

        <div className="space-y-4">
          {/* 공정명 입력 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              공정명 <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={processName}
              onChange={(e) => setProcessName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleSubmit();
                }
              }}
              placeholder="공정명을 입력하세요"
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              autoFocus
            />
          </div>

          {/* 작업자 이름 입력 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              작업자 이름 <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={operatorName}
              onChange={(e) => setOperatorName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleSubmit();
                }
              }}
              placeholder="작업자 이름을 입력하세요"
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* NC 업로드 제거됨 */}

          {/* 미리보기 */}
          {processName && operatorName && (
            <div className="bg-blue-50 p-3 rounded-lg">
              <p className="text-xs text-gray-600 mb-1">폴더명 미리보기:</p>
              <p className="text-sm font-mono text-blue-700">
                {(() => {
                  const now = new Date();
                  const year = String(now.getFullYear()).slice(2);
                  const month = String(now.getMonth() + 1).padStart(2, '0');
                  const day = String(now.getDate()).padStart(2, '0');
                  const hour = String(now.getHours()).padStart(2, '0');
                  const minute = String(now.getMinutes()).padStart(2, '0');
                  const second = String(now.getSeconds()).padStart(2, '0');
                  const combinedName = `${processName.trim()}_${operatorName.trim()}`;
                  return `${year}${month}${day}_${hour}${minute}${second}_${combinedName}`;
                })()}
              </p>
            </div>
          )}
        </div>

        <div className="mt-6 flex gap-3">
          <button
            onClick={handleSubmit}
            className="flex-1 px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium transition-colors"
          >
            시작하기
          </button>
        </div>
      </div>
    </div>
  );
};

export default InitialSetupModal;

