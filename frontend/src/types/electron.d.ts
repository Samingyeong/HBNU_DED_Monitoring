// Electron API 타입 정의
declare global {
  interface Window {
    electronAPI?: {
      readLogFile: (filePath: string) => Promise<{
        success: boolean;
        content?: string;
        error?: string;
      }>;
      checkFileExists: (filePath: string) => Promise<boolean>;
    };
  }
}

export {};
