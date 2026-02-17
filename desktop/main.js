const { app, BrowserWindow, ipcMain, Tray, Menu, globalShortcut } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const axios = require('axios');

let mainWindow;
let tray;
let pythonProcess;
const BACKEND_PORT = 8000;
const BACKEND_URL = `http://localhost:${BACKEND_PORT}`;

// Check if backend is already running
async function isBackendRunning() {
  try {
    await axios.get(`${BACKEND_URL}/api/health`, { timeout: 2000 });
    return true;
  } catch {
    return false;
  }
}

// Start Python backend
async function startBackend() {
  const backendRunning = await isBackendRunning();
  
  if (backendRunning) {
    console.log('Backend already running');
    return;
  }

  console.log('Starting Python backend...');
  
  // Path to backend - adjust based on your structure
  const backendPath = path.join(__dirname, '..', 'backend');
  const pythonScript = path.join(backendPath, 'main.py');
  
  console.log(`Backend path: ${backendPath}`);
  console.log(`Python script: ${pythonScript}`);
  
  // Use python with properly quoted path (no shell to avoid argument issues)
  pythonProcess = spawn('python', [pythonScript], {
    cwd: backendPath,
    shell: false
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`);
  });

  // Wait for backend to be ready
  for (let i = 0; i < 30; i++) {
    await new Promise(resolve => setTimeout(resolve, 1000));
    if (await isBackendRunning()) {
      console.log('✅ Backend ready!');
      return;
    }
  }
  
  console.error('❌ Backend failed to start');
}

// Create main window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    icon: path.join(__dirname, 'assets', 'icon.png'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    titleBarStyle: 'default',
    autoHideMenuBar: true,
    backgroundColor: '#1a1a1a',
    show: false // Don't show until ready
  });

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Load the web UI from backend
  mainWindow.loadURL(`${BACKEND_URL}/`).catch(err => {
    console.error('Failed to load backend URL:', err);
    // Load a simple error page
    mainWindow.loadURL(`data:text/html,<html><body style="background:#1a1a1a;color:#fff;font-family:system-ui;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;"><div style="text-align:center;"><h1>⚠️ Backend Connection Failed</h1><p>Could not connect to YAAN backend on port ${BACKEND_PORT}</p><p>Please check if Python backend is running.</p><button onclick="location.reload()" style="padding:10px 20px;margin-top:20px;font-size:16px;cursor:pointer;">Retry</button></div></body></html>`);
  });

  // Open DevTools in development
  if (process.argv.includes('--dev')) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('close', (event) => {
    if (!app.isQuitting) {
      event.preventDefault();
      mainWindow.hide();
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Create system tray
function createTray() {
  const iconPath = path.join(__dirname, 'assets', 'tray-icon.png');
  
  // Check if icon exists, skip tray if not
  if (!require('fs').existsSync(iconPath)) {
    console.log('⚠️  Tray icon not found, skipping system tray');
    return;
  }
  
  tray = new Tray(iconPath);

  const contextMenu = Menu.buildFromTemplate([
    {
      label: 'Show YAAN',
      click: () => {
        if (mainWindow) {
          mainWindow.show();
          mainWindow.focus();
        }
      }
    },
    {
      label: 'Quick Chat',
      accelerator: 'CmdOrCtrl+Shift+Y',
      click: () => {
        if (mainWindow) {
          mainWindow.show();
          mainWindow.focus();
          mainWindow.webContents.send('focus-input');
        }
      }
    },
    { type: 'separator' },
    {
      label: 'Quit',
      click: () => {
        app.isQuitting = true;
        app.quit();
      }
    }
  ]);

  tray.setToolTip('YAAN - AI Assistant');
  tray.setContextMenu(contextMenu);

  tray.on('click', () => {
    if (mainWindow) {
      if (mainWindow.isVisible()) {
        mainWindow.hide();
      } else {
        mainWindow.show();
        mainWindow.focus();
      }
    }
  });
}

// Register global shortcuts
function registerShortcuts() {
  // Quick access shortcut
  globalShortcut.register('CmdOrCtrl+Shift+Y', () => {
    if (mainWindow) {
      if (mainWindow.isVisible()) {
        mainWindow.hide();
      } else {
        mainWindow.show();
        mainWindow.focus();
      }
    }
  });

  // Voice mode shortcut
  globalShortcut.register('CmdOrCtrl+Shift+V', () => {
    if (mainWindow) {
      mainWindow.show();
      mainWindow.focus();
      mainWindow.webContents.send('toggle-voice');
    }
  });
}

// App lifecycle
app.whenReady().then(async () => {
  await startBackend();
  createWindow();
  createTray();
  registerShortcuts();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  // Keep app running in tray on Windows/Linux
  if (process.platform !== 'darwin') {
    // Don't quit, just hide
  }
});

app.on('will-quit', () => {
  // Unregister all shortcuts
  globalShortcut.unregisterAll();
  
  // Kill Python backend
  if (pythonProcess) {
    pythonProcess.kill();
  }
});

app.on('before-quit', () => {
  app.isQuitting = true;
});

// IPC handlers
ipcMain.handle('get-backend-url', () => {
  return BACKEND_URL;
});

ipcMain.handle('minimize-to-tray', () => {
  if (mainWindow) {
    mainWindow.hide();
  }
});

ipcMain.handle('show-notification', (event, { title, body }) => {
  const { Notification } = require('electron');
  new Notification({ title, body }).show();
});
