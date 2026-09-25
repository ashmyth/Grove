const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getVersion: () => ipcRenderer.invoke('app:get-version'),
  getPlatform: () => ipcRenderer.invoke('app:get-platform'),
  onBackendStatus: (callback) => ipcRenderer.on('backend:status', (_event, status) => callback(status)),
});

window.addEventListener('DOMContentLoaded', () => {
  console.log('Grove Desktop Electron Runtime Ready');
  console.log('Platform:', process.platform);
  console.log('Electron version:', process.versions.electron);
});