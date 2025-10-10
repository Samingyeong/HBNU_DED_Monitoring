import { useState, useEffect, useCallback } from 'react';

// 개발 환경에서 Electron API mock
if (process.env.NODE_ENV === 'development' && !window.electronAPI) {
  window.electronAPI = {
    readLogFile: async (filePath: string) => {
      try {
        // 개발 환경에서는 fetch를 사용하여 파일 읽기 시뮬레이션
        const response = await fetch(`file://${filePath}`);
        if (response.ok) {
          const content = await response.text();
          return { success: true, content };
        } else {
          return { success: false, error: 'File not found' };
        }
      } catch (error: any) {
        return { success: false, error: error.message };
      }
    },
    checkFileExists: async (filePath: string) => {
      try {
        const response = await fetch(`file://${filePath}`, { method: 'HEAD' });
        return response.ok;
      } catch {
        return false;
      }
    }
  };
}

interface AutoSaveStatus {
  isAutoSaving: boolean;
  currentSession: string | null;
  lastTraceTime: string | null;
  hasException: boolean;
  error: string | null;
}

interface TraceLogEntry {
  timestamp: string;
  message: string;
}

export const useAutoSave = () => {
  const [status, setStatus] = useState<AutoSaveStatus>({
    isAutoSaving: false,
    currentSession: null,
    lastTraceTime: null,
    hasException: false,
    error: null
  });

  // 파일 경로 설정 (C드라이브 기본, D드라이브 폴백)
  const getLogPaths = useCallback(() => {
    const basePaths = [
      'C:\\DED\\Log',
      'D:\\DED\\Log'
    ];
    
    return basePaths.map(base => ({
      trace: `${base}\\Trace\\Trace_${new Date().toISOString().slice(0, 10).replace(/-/g, '-')}.txt`,
      exception: `${base}\\Exception\\Exception_${new Date().toISOString().slice(0, 10).replace(/-/g, '-')}.txt`
    }));
  }, []);

  // Trace 파일에서 시작/종료 로그 감지
  const checkTraceFile = useCallback(async () => {
    try {
      const logPaths = getLogPaths();
      
      for (const paths of logPaths) {
        try {
          // Electron IPC를 통해 파일 읽기
          const result = await window.electronAPI?.readLogFile(paths.trace);
          
          if (result?.success && result.content) {
            const lines = result.content.split('\n').filter(line => line.trim());
            
            if (lines.length === 0) continue;
            
            const lastLine = lines[lines.length - 1];
            const [timestamp, ...messageParts] = lastLine.split(',');
            const message = messageParts.join(',').trim();
            
            // 시작 로그 감지 (NC_CS5Axis,StartNormal)
            if (message.includes('NC_CS5Axis,StartNormal') && message.includes('step,10')) {
              const sessionId = `session_${timestamp.replace(/[:.]/g, '-')}`;
              
              setStatus(prev => ({
                ...prev,
                isAutoSaving: true,
                currentSession: sessionId,
                lastTraceTime: timestamp,
                hasException: false,
                error: null
              }));
              
              console.log('🚀 자동저장 시작:', sessionId);
              // 백엔드에 자동저장 시작 요청
              startAutoSaving(sessionId);
              return;
            }
            
            // 종료 로그 감지 (NC_CS5AXIS,IsRunning,False)
            if (message.includes('NC_CS5AXIS,IsRunning,False')) {
              setStatus(prev => ({
                ...prev,
                isAutoSaving: false,
                currentSession: null,
                lastTraceTime: timestamp,
                hasException: false
              }));
              
              console.log('🛑 자동저장 중지: NC 작업 완료');
              // 백엔드에 자동저장 중지 요청
              stopAutoSaving();
              return;
            }
            
            // UnInit 로그 감지 (시스템 종료)
            if (message.includes('UnInit Completed')) {
              setStatus(prev => ({
                ...prev,
                isAutoSaving: false,
                currentSession: null,
                lastTraceTime: timestamp,
                hasException: false
              }));
              
              console.log('🛑 자동저장 중지: 시스템 종료');
              // 백엔드에 자동저장 중지 요청
              stopAutoSaving();
              return;
            }
          }
        } catch (error) {
          // 파일이 없거나 읽을 수 없는 경우 다음 경로 시도
          continue;
        }
      }
    } catch (error) {
      console.error('Trace 파일 확인 중 오류:', error);
      setStatus(prev => ({
        ...prev,
        error: `Trace 파일 읽기 실패: ${error}`
      }));
    }
  }, [getLogPaths]);

  // Exception 파일에서 중단 감지
  const checkExceptionFile = useCallback(async () => {
    try {
      const logPaths = getLogPaths();
      
      for (const paths of logPaths) {
        try {
          // Electron IPC를 통해 파일 읽기
          const result = await window.electronAPI?.readLogFile(paths.exception);
          
          if (result?.success && result.content) {
            const lines = result.content.split('\n').filter(line => line.trim());
            
            if (lines.length > 0) {
              const lastLine = lines[lines.length - 1];
              const [timestamp, ...messageParts] = lastLine.split(',');
              const message = messageParts.join(',').trim();
              
              // Exception 발생 시 자동저장 중지
              if (message.includes('SocketServer') || message.includes('Exception')) {
                setStatus(prev => ({
                  ...prev,
                  isAutoSaving: false,
                  currentSession: null,
                  hasException: true,
                  error: `Exception 발생: ${message}`
                }));
                
                console.log('⚠️ 자동저장 중지: Exception 발생');
                // 백엔드에 자동저장 중지 요청
                stopAutoSaving();
                return;
              }
            }
          }
        } catch (error) {
          continue;
        }
      }
    } catch (error) {
      console.error('Exception 파일 확인 중 오류:', error);
    }
  }, [getLogPaths]);

  // 파일 모니터링 시작
  useEffect(() => {
    const interval = setInterval(() => {
      checkTraceFile();
      checkExceptionFile();
    }, 2000); // 2초마다 체크

    return () => clearInterval(interval);
  }, [checkTraceFile, checkExceptionFile]);

  // 자동저장 시작 시 백엔드에 임시 저장 요청
  const startAutoSaving = useCallback(async (sessionId: string) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/save/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          folder_name: sessionId,
          auto_save: true
        })
      });
      
      if (response.ok) {
        console.log('✅ 자동저장 임시 저장 시작됨:', sessionId);
      } else {
        console.error('❌ 자동저장 임시 저장 시작 실패');
      }
    } catch (error) {
      console.error('❌ 자동저장 백엔드 통신 오류:', error);
    }
  }, []);

  // 자동저장 중지 시 백엔드에 임시 저장 중지 요청
  const stopAutoSaving = useCallback(async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/save/temp-stop', {
        method: 'POST'
      });
      
      if (response.ok) {
        console.log('✅ 자동저장 임시 저장 중지됨');
      } else {
        console.error('❌ 자동저장 임시 저장 중지 실패');
      }
    } catch (error) {
      console.error('❌ 자동저장 백엔드 통신 오류:', error);
    }
  }, []);

  // 수동으로 자동저장 상태 리셋
  const resetAutoSave = useCallback(() => {
    setStatus({
      isAutoSaving: false,
      currentSession: null,
      lastTraceTime: null,
      hasException: false,
      error: null
    });
  }, []);

  return {
    ...status,
    resetAutoSave,
    startAutoSaving,
    stopAutoSaving
  };
};
