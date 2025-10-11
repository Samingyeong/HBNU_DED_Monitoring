/**
 * 초기 설정 모달 - 작업자명 및 Gcode 폴더 선택
 */
import React, { useState } from 'react';

interface InitialSetupModalProps {
  isOpen: boolean;
  onComplete: (operatorName: string, gcodeFolderPath: string) => void;
}

const InitialSetupModal: React.FC<InitialSetupModalProps> = ({ isOpen, onComplete }) => {
  const [operatorName, setOperatorName] = useState('');
  const [gcodeFolderPath, setGcodeFolderPath] = useState('');
  const [fileContent, setFileContent] = useState<string>('');

  if (!isOpen) return null;

  const handleSelectFile = async () => {
    try {
      // 모든 환경에서 HTML5 파일 API 사용
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = '.nc,.txt,.tap,.cnc';
      input.multiple = false;
      
      input.onchange = (e) => {
        const target = e.target as HTMLInputElement;
        if (target.files && target.files.length > 0) {
          const file = target.files[0];
          // 파일명 표시
          setGcodeFolderPath(file.name);
          
          // 파일 내용을 읽어서 백엔드로 전송할 수 있도록 준비
          const reader = new FileReader();
          reader.onload = (event) => {
            const content = event.target?.result as string;
            setFileContent(content);
            console.log('선택된 파일:', file.name);
            console.log('파일 내용 미리보기:', content.substring(0, 200) + '...');
          };
          reader.readAsText(file);
        }
      };
      
      input.click();
    } catch (error) {
      console.error('파일 선택 오류:', error);
    }
  };

  const handleSubmit = async () => {
    if (!operatorName.trim()) {
      alert('작업자명을 입력해주세요.');
      return;
    }

    if (!gcodeFolderPath.trim()) {
      alert('NC코드 파일을 선택해주세요.');
      return;
    }

    if (!fileContent.trim()) {
      alert('파일 내용을 읽을 수 없습니다. 파일을 다시 선택해주세요.');
      return;
    }

    // 백엔드로 NC코드 파일 전송 및 파싱
    try {
      // 모든 환경에서 파일 내용 사용
      const requestBody = {
        file_content: fileContent
      };
      
      const response = await fetch('http://127.0.0.1:8000/api/nc/parse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (response.ok) {
        const result = await response.json();
        console.log('NC코드 파싱 성공:', result);
        onComplete(operatorName, gcodeFolderPath);
      } else {
        const error = await response.json();
        alert(`NC코드 파싱 실패: ${error.detail || '알 수 없는 오류'}`);
      }
    } catch (error) {
      console.error('NC코드 파싱 오류:', error);
      alert('백엔드 서버와 통신 중 오류가 발생했습니다.');
    }
  };

  return (
    <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-70 flex items-center justify-center" style={{ zIndex: 9999 }}>
      <div className="bg-white rounded-2xl p-8 w-[500px] max-w-[90vw] shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="text-center mb-6">
          <div className="w-16 h-16 bg-blue-600 rounded-xl flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-2xl">H</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">공정 시작 설정</h2>
          <p className="text-sm text-gray-500">작업자명과 NC코드 파일을 설정해주세요</p>
        </div>

        <div className="space-y-4">
          {/* 작업자명 입력 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              작업자명 <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={operatorName}
              onChange={(e) => {
                console.log('작업자명 입력:', e.target.value);
                setOperatorName(e.target.value);
              }}
              placeholder="작업자명을 입력하세요"
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              autoFocus
            />
          </div>

          {/* NC코드 파일 선택 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              NC코드 파일 <span className="text-red-500">*</span>
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={gcodeFolderPath}
                onChange={(e) => setGcodeFolderPath(e.target.value)}
                placeholder="NC코드 파일명"
                className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
              />
              <button
                onClick={handleSelectFile}
                className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg transition-colors"
              >
                📄 파일 선택
              </button>
            </div>
          </div>

          {/* 미리보기 */}
          {operatorName && (
            <div className="bg-blue-50 p-3 rounded-lg">
              <p className="text-xs text-gray-600 mb-1">폴더명 미리보기:</p>
              <p className="text-sm font-mono text-blue-700">
                {(() => {
                  const now = new Date();
                  const year = now.getFullYear();
                  const month = String(now.getMonth() + 1).padStart(2, '0');
                  const day = String(now.getDate()).padStart(2, '0');
                  const hour = String(now.getHours()).padStart(2, '0');
                  const minute = String(now.getMinutes()).padStart(2, '0');
                  return `${year}${month}${day}_${hour}${minute}_${operatorName}`;
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

