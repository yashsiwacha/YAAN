const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Get backend URL
  getBackendUrl: () => ipcRenderer.invoke('get-backend-url'),
  
  // Window controls
  minimizeToTray: () => ipcRenderer.invoke('minimize-to-tray'),
  
  // Notifications
  showNotification: (title, body) => ipcRenderer.invoke('show-notification', { title, body }),
  
  // Listen to events from main process
  onFocusInput: (callback) => {
    ipcRenderer.on('focus-input', callback);
  },
  
  onToggleVoice: (callback) => {
    ipcRenderer.on('toggle-voice', callback);
  },
  
  // Platform info
  platform: process.platform,
  
  // App version
  version: '2.0.0'
});

// Log that preload script loaded
console.log('✅ Preload script loaded');
