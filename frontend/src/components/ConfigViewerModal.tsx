/**
 * Config 파일 뷰어 모달 - ini 설정 파일 내용 표시
 */
import React, { useState, useEffect } from 'react';
import { ApiService } from '../services/api';

interface ConfigViewerModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ConfigViewerModal({ isOpen, onClose }: ConfigViewerModalProps) {
  const [configFiles, setConfigFiles] = useState<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>('');
  const [fileContent, setFileContent] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  // 모달이 열릴 때 설정 파일 목록 로드
  useEffect(() => {
    if (isOpen) {
      loadConfigList();
    }
  }, [isOpen]);

  const loadConfigList = async () => {
    try {
      setLoading(true);
      setError('');
      const files = await ApiService.getConfigList();
      setConfigFiles(files);
      
      // 첫 번째 파일 자동 선택
      if (files.length > 0) {
        setSelectedFile(files[0]);
        loadConfigFile(files[0]);
      }
    } catch (err: any) {
      console.error('설정 파일 목록 로드 실패:', err);
      setError(`설정 파일 목록 로드 실패: ${err.message || '알 수 없는 오류'}`);
    } finally {
      setLoading(false);
    }
  };

  const loadConfigFile = async (fileName: string) => {
    try {
      setLoading(true);
      setError('');
      const data = await ApiService.getConfigFile(fileName);
      setFileContent(data.content);
    } catch (err: any) {
      console.error('설정 파일 로드 실패:', err);
      setError(`설정 파일 로드 실패: ${err.message || '알 수 없는 오류'}`);
      setFileContent('');
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (fileName: string) => {
    setSelectedFile(fileName);
    loadConfigFile(fileName);
  };

  if (!isOpen) return null;

  return (
    <div 
      className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-70 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <div 
        className="bg-white rounded-2xl p-6 w-[800px] max-w-[90vw] h-[600px] max-h-[80vh] shadow-2xl flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* 헤더 */}
        <div className="flex justify-between items-center mb-4 pb-4 border-b border-gray-200">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">설정 파일 보기</h2>
            <p className="text-sm text-gray-500 mt-1">시스템 설정 파일(config/*.ini) 내용을 확인합니다</p>
          </div>
          <button 
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl font-bold w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100"
          >
            ✕
          </button>
        </div>

        {/* 에러 메시지 */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* 본문 */}
        <div className="flex-1 flex gap-4 overflow-hidden">
          {/* 왼쪽: 파일 목록 */}
          <div className="w-48 flex flex-col">
            <h3 className="text-sm font-semibold text-gray-700 mb-2">설정 파일</h3>
            <div className="flex-1 overflow-y-auto border border-gray-200 rounded-lg">
              {loading && configFiles.length === 0 ? (
                <div className="p-4 text-center text-gray-500 text-sm">
                  로딩 중...
                </div>
              ) : configFiles.length === 0 ? (
                <div className="p-4 text-center text-gray-500 text-sm">
                  설정 파일이 없습니다
                </div>
              ) : (
                configFiles.map((file) => (
                  <button
                    key={file}
                    onClick={() => handleFileSelect(file)}
                    className={`w-full text-left px-4 py-2 text-sm transition-colors border-b border-gray-100 last:border-b-0 ${
                      selectedFile === file
                        ? 'bg-blue-50 text-blue-700 font-medium'
                        : 'hover:bg-gray-50 text-gray-700'
                    }`}
                  >
                    {file}
                  </button>
                ))
              )}
            </div>
          </div>

          {/* 오른쪽: 파일 내용 */}
          <div className="flex-1 flex flex-col">
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-sm font-semibold text-gray-700">
                {selectedFile || '파일을 선택하세요'}
              </h3>
              <button
                onClick={() => selectedFile && loadConfigFile(selectedFile)}
                disabled={!selectedFile || loading}
                className="text-xs px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                🔄 새로고침
              </button>
            </div>
            <div className="flex-1 overflow-y-auto border border-gray-200 rounded-lg bg-gray-50 p-4">
              {loading ? (
                <div className="flex items-center justify-center h-full">
                  <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
              ) : fileContent ? (
                <pre className="text-xs font-mono text-gray-800 whitespace-pre-wrap break-words">
                  {fileContent}
                </pre>
              ) : (
                <div className="flex items-center justify-center h-full text-gray-500 text-sm">
                  {selectedFile ? '파일 내용이 비어있습니다' : '왼쪽에서 파일을 선택하세요'}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* 푸터 */}
        <div className="mt-4 pt-4 border-t border-gray-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium transition-colors"
          >
            닫기
          </button>
        </div>
      </div>
    </div>
  );
}


