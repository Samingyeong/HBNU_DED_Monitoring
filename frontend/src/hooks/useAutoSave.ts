import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

interface AutoSaveStatus {
  isAutoSaving: boolean;
  currentSession: string | null;
  lastEventTime: string | null;
  hasException: boolean;
  error: string | null;
}

interface TempStorageInfo {
  has_temp_data: boolean;
  session_id: string | null;
  data_count: number;
  start_time: string | null;
}

export const useAutoSave = () => {
  const [status, setStatus] = useState<AutoSaveStatus>({
    isAutoSaving: false,
    currentSession: null,
    lastEventTime: null,
    hasException: false,
    error: null
  });

  const [tempStorage, setTempStorage] = useState<TempStorageInfo>({
    has_temp_data: false,
    session_id: null,
    data_count: 0,
    start_time: null
  });

  // 백엔드에서 자동저장 상태 조회 (폴링)
  const fetchAutoSaveStatus = useCallback(async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/autosave/status`, {
        timeout: 3000
      });
      
      if (response.data?.success) {
        setStatus(prev => ({
          ...prev,
          isAutoSaving: response.data.is_auto_saving || false,
          currentSession: response.data.current_session || null,
          lastEventTime: response.data.timestamp,
          error: null
        }));
        
        if (response.data.temp_storage) {
          setTempStorage(response.data.temp_storage);
        }
      }
    } catch (error) {
      // 백엔드 연결 실패 시 조용히 실패
      console.debug('📋 자동저장 상태 조회 스킵 (백엔드 미연결)');
    }
  }, []);

  // WebSocket 메시지 처리 (자동저장 이벤트)
  const handleWebSocketMessage = useCallback((data: any) => {
    if (data.type === 'auto_save_event') {
      console.log('📋 자동저장 이벤트 수신:', data);
      
      if (data.event === 'start') {
        setStatus(prev => ({
          ...prev,
          isAutoSaving: true,
          currentSession: data.session_id,
          lastEventTime: data.timestamp,
          hasException: false,
          error: null
        }));
        console.log('🚀 자동저장 시작 (백엔드에서 감지):', data.session_id);
      } else if (data.event === 'stop') {
        setStatus(prev => ({
          ...prev,
          isAutoSaving: false,
          currentSession: null,
          lastEventTime: data.timestamp,
          hasException: false
        }));
        console.log('🛑 자동저장 중지 (백엔드에서 감지):', data.reason);
      }
    }
  }, []);

  // 폴링으로 상태 확인 (5초마다)
  useEffect(() => {
    // 초기 상태 조회
    fetchAutoSaveStatus();
    
    const interval = setInterval(() => {
      fetchAutoSaveStatus();
    }, 5000); // 5초마다 체크 (백엔드에서 2초마다 파일 감시하므로 충분)

    return () => clearInterval(interval);
  }, [fetchAutoSaveStatus]);

  // WebSocket 연결 및 메시지 수신
  useEffect(() => {
    let ws: WebSocket | null = null;
    let reconnectTimeout: NodeJS.Timeout | null = null;

    const connect = () => {
      try {
        ws = new WebSocket('ws://127.0.0.1:8000/ws');
        
        ws.onopen = () => {
          console.log('📋 자동저장 WebSocket 연결됨');
        };
        
        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
          } catch (e) {
            // JSON 파싱 실패 무시
          }
        };
        
        ws.onclose = () => {
          console.log('📋 자동저장 WebSocket 연결 해제');
          // 3초 후 재연결 시도
          reconnectTimeout = setTimeout(connect, 3000);
        };
        
        ws.onerror = () => {
          // 에러 시 조용히 처리 (onclose에서 재연결)
        };
      } catch (e) {
        // 연결 실패 시 3초 후 재시도
        reconnectTimeout = setTimeout(connect, 3000);
      }
    };

    connect();

    return () => {
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
      }
      if (ws) {
        ws.close();
      }
    };
  }, [handleWebSocketMessage]);

  // 수동으로 자동저장 상태 리셋
  const resetAutoSave = useCallback(() => {
    setStatus({
      isAutoSaving: false,
      currentSession: null,
      lastEventTime: null,
      hasException: false,
      error: null
    });
  }, []);

  // 수동으로 자동저장 시작 (백엔드 API 호출)
  const startAutoSaving = useCallback(async (sessionId: string) => {
    try {
      await axios.post(`${API_BASE_URL}/api/save/start`, {
        folder_name: sessionId,
        auto_save: true
      });
      console.log('✅ 자동저장 수동 시작:', sessionId);
      
      setStatus(prev => ({
        ...prev,
        isAutoSaving: true,
        currentSession: sessionId,
        lastEventTime: new Date().toISOString(),
        error: null
      }));
    } catch (error) {
      console.error('❌ 자동저장 수동 시작 실패:', error);
    }
  }, []);

  // 수동으로 자동저장 중지 (백엔드 API 호출)
  const stopAutoSaving = useCallback(async () => {
    try {
      await axios.post(`${API_BASE_URL}/api/save/temp-stop`);
      console.log('✅ 자동저장 수동 중지');
      
      setStatus(prev => ({
        ...prev,
        isAutoSaving: false,
        currentSession: null,
        lastEventTime: new Date().toISOString()
      }));
    } catch (error) {
      console.error('❌ 자동저장 수동 중지 실패:', error);
    }
  }, []);

  return {
    ...status,
    tempStorage,
    resetAutoSave,
    startAutoSaving,
    stopAutoSaving,
    refreshStatus: fetchAutoSaveStatus
  };
};
