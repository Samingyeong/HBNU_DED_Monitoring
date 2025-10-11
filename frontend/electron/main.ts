const { app, BrowserWindow, ipcMain, dialog } = require('electron')
const path = require('path')
const fs = require('fs')

const isDev = process.env.NODE_ENV === 'development'

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1800,
    height: 1000,
    minWidth: 1300,
    minHeight: 840,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
    icon: path.join(__dirname, '../public/icon.png'),
  })

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }
}

// 파일 읽기 API
ipcMain.handle('read-log-file', async (event: any, filePath: string) => {
  try {
    if (fs.existsSync(filePath)) {
      const content = fs.readFileSync(filePath, 'utf8')
      return { success: true, content }
    } else {
      return { success: false, error: 'File not found' }
    }
  } catch (error: any) {
    return { success: false, error: error.message }
  }
})

// 파일 존재 확인 API
ipcMain.handle('check-file-exists', async (event: any, filePath: string) => {
  try {
    return fs.existsSync(filePath)
  } catch (error: any) {
    return false
  }
})

// 폴더 선택 API
ipcMain.handle('select-folder', async () => {
  try {
    const result = await dialog.showOpenDialog({
      properties: ['openDirectory']
    })
    
    if (!result.canceled && result.filePaths.length > 0) {
      return result.filePaths[0]
    }
    return null
  } catch (error: any) {
    console.error('폴더 선택 오류:', error)
    return null
  }
})

// 파일 선택 API
ipcMain.handle('select-file', async () => {
  try {
    const result = await dialog.showOpenDialog({
      properties: ['openFile'],
      title: 'NC코드 파일 선택',
      filters: [
        { name: 'NC코드 파일', extensions: ['nc', 'txt', 'tap', 'cnc'] },
        { name: '모든 파일', extensions: ['*'] }
      ]
    })
    
    if (!result.canceled && result.filePaths.length > 0) {
      return result.filePaths[0]
    }
    return null
  } catch (error: any) {
    console.error('파일 선택 오류:', error)
    return null
  }
})

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
