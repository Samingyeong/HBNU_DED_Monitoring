import { useState, useEffect, useCallback } from 'react';
import { ApiService, wsService, SensorData, SystemStatus, SaveStatus } from '../services/api';

interface UseSensorDataResult {
  isConnected: boolean;
  latestData: SensorData | null;
  historyData: SensorData[];
  systemStatus: SystemStatus | null;
  saveStatus: SaveStatus | null;
  error: string | null;
  startSaving: (folderName: string) => Promise<void>;
  stopSaving: () => Promise<void>;
}

export const useSensorData = (): UseSensorDataResult => {
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [latestData, setLatestData] = useState<SensorData | null>(null);
  const [historyData, setHistoryData] = useState<SensorData[]>([]);
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [saveStatus, setSaveStatus] = useState<SaveStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  // API를 통해 초기 데이터 및 상태를 가져오는 함수
  const fetchInitialData = useCallback(async () => {
    try {
      const [status, latest, saveStat] = await Promise.all([
        ApiService.getSystemStatus(),
        ApiService.getLatestData(),
        ApiService.getSaveStatus(),
      ]);
      setSystemStatus(status);
      setLatestData(latest);
      setSaveStatus(saveStat);
      setIsConnected(true);
      setError(null);
    } catch (err: any) {
      console.error("초기 데이터 로드 실패:", err);
      setError(`데이터 로드 실패: ${err.message || '알 수 없는 오류'}`);
      setIsConnected(false);
    }
  }, []);

  // WebSocket 메시지 핸들러
  const handleWebSocketMessage = useCallback((data: SensorData) => {
    setLatestData(data);
    setHistoryData(prev => {
      const newHistory = [...prev, data];
      // 최대 500개의 데이터만 유지
      if (newHistory.length > 500) {
        return newHistory.slice(newHistory.length - 500);
      }
      return newHistory;
    });
  }, []);

  const handleStatusUpdate = useCallback((status: SystemStatus) => {
    setSystemStatus(status);
  }, []);

  const handleSaveStatusUpdate = useCallback((status: SaveStatus) => {
    setSaveStatus(status);
  }, []);

  const handleConnectionStatus = useCallback((status: { connected: boolean }) => {
    setIsConnected(status.connected);
    if (!status.connected) {
      setError("백엔드 서버와 연결이 끊어졌습니다.");
    } else {
      setError(null);
      fetchInitialData(); // 재연결 시 데이터 다시 로드
    }
  }, [fetchInitialData]);

  const handleWebSocketError = useCallback((err: any) => {
    console.error("WebSocket 오류:", err);
    setError(`WebSocket 오류: ${err.message || '알 수 없는 오류'}`);
  }, []);

  useEffect(() => {
    // 초기 데이터 로드
    fetchInitialData();

    // 전역 WebSocket 인스턴스 사용 (이벤트 리스너만 등록)
    wsService.on('sensor_data', handleWebSocketMessage);
    wsService.on('status_update', handleStatusUpdate);
    wsService.on('save_status', handleSaveStatusUpdate);
    wsService.on('connection', handleConnectionStatus);
    wsService.on('error', handleWebSocketError);

    // 이미 연결되어 있지 않다면 연결
    if (!wsService.isConnected()) {
      wsService.connect();
    }

    return () => {
      // 컴포넌트 언마운트 시 리스너만 제거 (연결은 유지)
      wsService.off('sensor_data', handleWebSocketMessage);
      wsService.off('status_update', handleStatusUpdate);
      wsService.off('save_status', handleSaveStatusUpdate);
      wsService.off('connection', handleConnectionStatus);
      wsService.off('error', handleWebSocketError);
      // 주의: wsService.disconnect()를 호출하지 않음 (전역 인스턴스이므로)
    };
  }, [fetchInitialData, handleWebSocketMessage, handleStatusUpdate, handleSaveStatusUpdate, handleConnectionStatus, handleWebSocketError]);

  const startSaving = useCallback(async (folderName: string) => {
    try {
      const response = await ApiService.startSaving({ folder_name: folderName });
      setSaveStatus({ is_saving: true, save_path: response.save_path, timestamp: response.timestamp });
      setError(null);
    } catch (err: any) {
      console.error("저장 시작 실패:", err);
      setError(`저장 시작 실패: ${err.message || '알 수 없는 오류'}`);
    }
  }, []);

  const stopSaving = useCallback(async () => {
    try {
      await ApiService.stopSaving();
      setSaveStatus({ is_saving: false, save_path: undefined, timestamp: new Date().toISOString() });
      setError(null);
    } catch (err: any) {
      console.error("저장 중지 실패:", err);
      setError(`저장 중지 실패: ${err.message || '알 수 없는 오류'}`);
    }
  }, []);

  return {
    isConnected,
    latestData,
    historyData,
    systemStatus,
    saveStatus,
    error,
    startSaving,
    stopSaving,
  };
};
