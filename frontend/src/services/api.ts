/**
 * API 서비스 - 백엔드와의 통신을 담당
 */
import axios, { AxiosInstance, AxiosResponse } from 'axios';

// API 기본 설정 (테스트 백엔드 사용)
const API_BASE_URL = 'http://127.0.0.1:8001';

// Axios 인스턴스 생성
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🌐 API 요청: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API 요청 오류:', error);
    return Promise.reject(error);
  }
);

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`✅ API 응답: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API 응답 오류:', error);
    return Promise.reject(error);
  }
);

// 타입 정의
export interface SensorData {
  timestamp: string;
  camera_data?: {
    image?: string;
    melt_pool_area?: number;
  };
  laser_data?: {
    outpower?: number;
    setpower?: number;
  };
  pyrometer_data?: {
    mpt?: number;
    '1ct'?: number;
    '2ct'?: number;
  };
  cnc_data?: {
    curpos_x?: number;
    curpos_y?: number;
    curpos_z?: number;
    curpos_a?: number;
    curpos_c?: number;
  };
  hik_camera_data?: {
    combined_image?: string;
  };
}

export interface SystemStatus {
  system_status: string;
  sensors: {
    camera: boolean;
    laser: boolean;
    pyrometer: boolean;
    cnc: boolean;
    hik_camera_1: boolean;
    hik_camera_2: boolean;
  };
  timestamp: string;
}

export interface SaveRequest {
  folder_name: string;
}

export interface SaveResponse {
  message: string;
  save_path: string;
  timestamp: string;
}

export interface SaveStatus {
  is_saving: boolean;
  save_path?: string;
  timestamp: string;
}

// API 서비스 클래스
export class ApiService {
  /**
   * 시스템 상태 조회
   */
  static async getSystemStatus(): Promise<SystemStatus> {
    const response = await apiClient.get('/api/status');
    return response.data;
  }

  /**
   * 최신 센서 데이터 조회
   */
  static async getLatestData(): Promise<SensorData> {
    const response = await apiClient.get('/api/data/latest');
    return response.data;
  }

  /**
   * 히스토리 데이터 조회
   */
  static async getDataHistory(limit: number = 100): Promise<SensorData[]> {
    const response = await apiClient.get(`/api/data/history?limit=${limit}`);
    return response.data;
  }

  /**
   * 데이터 저장 시작
   */
  static async startSaving(request: SaveRequest): Promise<SaveResponse> {
    const response = await apiClient.post('/api/save/start', request);
    return response.data;
  }

  /**
   * 데이터 저장 중지
   */
  static async stopSaving(): Promise<SaveResponse> {
    const response = await apiClient.post('/api/save/stop');
    return response.data;
  }

  /**
   * 저장 상태 조회
   */
  static async getSaveStatus(): Promise<SaveStatus> {
    const response = await apiClient.get('/api/save/status');
    return response.data;
  }

  /**
   * 이미지 조회
   */
  static async getImage(imageType: string): Promise<string> {
    const response = await apiClient.get(`/api/images/${imageType}`, {
      responseType: 'blob'
    });
    
    // Blob을 URL로 변환
    const blob = new Blob([response.data], { type: 'image/png' });
    return URL.createObjectURL(blob);
  }

  /**
   * 서버 연결 테스트
   */
  static async testConnection(): Promise<boolean> {
    try {
      const response = await apiClient.get('/');
      return response.status === 200;
    } catch (error) {
      console.error('서버 연결 테스트 실패:', error);
      return false;
    }
  }
}

// WebSocket 연결 관리
export class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectInterval = 3000;
  private listeners: Map<string, Function[]> = new Map();

  constructor() {
    this.listeners.set('sensor_data', []);
    this.listeners.set('status_update', []);
    this.listeners.set('save_status', []);
    this.listeners.set('connection', []);
    this.listeners.set('error', []);
  }

  /**
   * WebSocket 연결
   */
  connect(): void {
    try {
      this.ws = new WebSocket('ws://127.0.0.1:8001/ws');
      
      this.ws.onopen = () => {
        console.log('🔗 WebSocket 연결됨');
        this.reconnectAttempts = 0;
        this.emit('connection', { connected: true });
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.handleMessage(data);
        } catch (error) {
          console.error('❌ WebSocket 메시지 파싱 오류:', error);
        }
      };

      this.ws.onclose = () => {
        console.log('🔌 WebSocket 연결 해제됨');
        this.emit('connection', { connected: false });
        this.handleReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('❌ WebSocket 오류:', error);
        this.emit('error', error);
      };

    } catch (error) {
      console.error('❌ WebSocket 연결 실패:', error);
      this.handleReconnect();
    }
  }

  /**
   * WebSocket 연결 해제
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * 메시지 처리
   */
  private handleMessage(data: any): void {
    const { type } = data;
    
    switch (type) {
      case 'sensor_data':
        this.emit('sensor_data', data.data);
        break;
      case 'status_update':
        this.emit('status_update', data.data);
        break;
      case 'save_status':
        this.emit('save_status', data.data);
        break;
      case 'connection':
        this.emit('connection', data);
        break;
      case 'error':
        this.emit('error', data.message);
        break;
      case 'ping':
        // 핑 응답은 무시
        break;
      default:
        console.log('알 수 없는 WebSocket 메시지 타입:', type);
    }
  }

  /**
   * 재연결 처리
   */
  private handleReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`🔄 WebSocket 재연결 시도 ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
      
      setTimeout(() => {
        this.connect();
      }, this.reconnectInterval);
    } else {
      console.error('❌ WebSocket 최대 재연결 시도 횟수 초과');
    }
  }

  /**
   * 이벤트 리스너 등록
   */
  on(event: string, callback: Function): void {
    if (this.listeners.has(event)) {
      this.listeners.get(event)!.push(callback);
    }
  }

  /**
   * 이벤트 리스너 제거
   */
  off(event: string, callback: Function): void {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event)!;
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  /**
   * 이벤트 발생
   */
  private emit(event: string, data: any): void {
    if (this.listeners.has(event)) {
      this.listeners.get(event)!.forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`❌ 이벤트 콜백 오류 (${event}):`, error);
        }
      });
    }
  }

  /**
   * 연결 상태 확인
   */
  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }
}

// 전역 WebSocket 서비스 인스턴스
export const wsService = new WebSocketService();
