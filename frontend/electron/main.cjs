const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow = null;
let backendProcess = null;
const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;

function startBackend() {
  const backendPath = path.join(__dirname, '..', '..', 'backend');
  const pythonCmd = process.platform === 'win32' ? 'python.exe' : 'python3';
  
  console.log('[Electron] Starting FastAPI backend...');
  backendProcess = spawn(pythonCmd, ['-m', 'uvicorn', 'backend.main:app', '--host', '127.0.0.1', '--port', '8000'], {
    cwd: path.join(__dirname, '..', '..'),
    stdio: ['ignore', 'pipe', 'pipe'],
    env: { ...process.env, PYTHONPATH: path.join(__dirname, '..', '..') }
  });

  backendProcess.stdout.on('data', (data) => {
    console.log(`[Backend] ${data.toString().trim()}`);
  });

  backendProcess.stderr.on('data', (data) => {
    console.error(`[Backend ERROR] ${data.toString().trim()}`);
  });

  backendProcess.on('close', (code) => {
    console.log(`[Electron] Backend process exited with code ${code}`);
    backendProcess = null;
  });

  return new Promise(resolve => setTimeout(resolve, 3000));
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 1200,
    minHeight: 768,
    backgroundColor: '#0f172a',
    title: 'Grove — GeoPrithvi-Agri Canal Command Advisory System',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.cjs'),
    },
    autoHideMenuBar: true,
    show: false,
  });

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    if (isDev) {
      mainWindow.webContents.openDevTools();
    }
  });

  const loadApp = async () => {
    if (isDev) {
      // In dev mode, assume backend is running separately on port 8000
      // and Vite dev server is running on port 5173
      mainWindow.loadURL('http://127.0.0.1:5173');
    } else {
      // In production, start backend and load built frontend
      await startBackend();
      await new Promise(resolve => setTimeout(resolve, 2000));
      mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
    }
  };

  loadApp().catch(console.error);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
});

ipcMain.handle('app:get-version', () => app.getVersion());
ipcMain.handle('app:get-platform', () => process.platform);