const { contextBridge, ipcRenderer } = require('electron');

// Electron API를 렌더러 프로세스에 노출
contextBridge.exposeInMainWorld('electronAPI', {
  readLogFile: (filePath: string) => ipcRenderer.invoke('read-log-file', filePath),
  checkFileExists: (filePath: string) => ipcRenderer.invoke('check-file-exists', filePath),
});
