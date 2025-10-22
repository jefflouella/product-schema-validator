const { app, BrowserWindow, dialog, ipcMain, shell } = require('electron');
const { autoUpdater } = require('electron-updater');
const path = require('path');
const { spawn } = require('child_process');
const findPort = require('./port-finder');

// Keep a global reference of the window object
let mainWindow;
let pythonProcess;
let serverPort;

// Enable live reload for Electron in development
if (process.env.NODE_ENV === 'development') {
  require('electron-reload')(__dirname, {
    electron: path.join(__dirname, '..', 'node_modules', '.bin', 'electron'),
    hardResetMethod: 'exit'
  });
}

// Configure auto-updater (disabled for now - configure when you have a GitHub repo)
// autoUpdater.setFeedURL({
//   provider: 'github',
//   owner: 'yourusername', // Replace with your GitHub username
//   repo: 'schema-validator'
// });

// Check for updates on startup (disabled for now)
// autoUpdater.checkForUpdatesAndNotify();

// Update available event
autoUpdater.on('update-available', (info) => {
  const options = {
    type: 'info',
    title: 'Update Available',
    message: `A new version (${info.version}) is available. Would you like to download it now?`,
    detail: `Current version: ${app.getVersion()}\nNew version: ${info.version}\n\nRelease notes:\n${info.releaseNotes || 'No release notes available.'}`,
    buttons: ['Update Now', 'Remind Me Later', 'Skip This Version'],
    defaultId: 0,
    cancelId: 1
  };

  dialog.showMessageBox(mainWindow, options).then((result) => {
    if (result.response === 0) {
      // Update Now
      autoUpdater.downloadUpdate();
    } else if (result.response === 2) {
      // Skip This Version
      // Store skipped version in user preferences
      app.setAppUserModelId(`com.mookee.schema-validator-${info.version}`);
    }
    // If "Remind Me Later", do nothing - will check again on next launch
  });
});

// Update downloaded event
autoUpdater.on('update-downloaded', (info) => {
  const options = {
    type: 'info',
    title: 'Update Ready',
    message: 'Update downloaded successfully. Restart the application to apply the update.',
    buttons: ['Restart Now', 'Restart Later'],
    defaultId: 0
  };

  dialog.showMessageBox(mainWindow, options).then((result) => {
    if (result.response === 0) {
      autoUpdater.quitAndInstall();
    }
  });
});

// Download progress event
autoUpdater.on('download-progress', (progressObj) => {
  // You could emit this to the renderer process to show progress
  console.log(`Download progress: ${progressObj.percent}%`);
});

// Error event
autoUpdater.on('error', (error) => {
  console.error('Auto-updater error:', error);
  dialog.showErrorBox('Update Error', `An error occurred while checking for updates: ${error.message}`);
});

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, '..', 'build-resources', 'icon.png'),
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
    show: false // Don't show until ready
  });

  // Load the app
  const startUrl = `http://127.0.0.1:${serverPort}`;
  console.log(`Loading app from: ${startUrl}`);
  
  mainWindow.loadURL(startUrl).catch((error) => {
    console.error('Failed to load URL:', error);
    dialog.showErrorBox('Load Error', `Failed to load the application: ${error.message}`);
  });

  // Show window when ready to prevent visual flash
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // Open DevTools in development
    if (process.env.NODE_ENV === 'development') {
      mainWindow.webContents.openDevTools();
    }
  });

  // Handle page load errors
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription, validatedURL) => {
    console.error('Page load failed:', errorCode, errorDescription, validatedURL);
    dialog.showErrorBox('Page Load Error', `Failed to load page: ${errorDescription}\nURL: ${validatedURL}`);
  });

  // Handle navigation errors
  mainWindow.webContents.on('did-navigate', (event, url) => {
    console.log('Navigated to:', url);
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

function startPythonServer() {
  return new Promise((resolve, reject) => {
    // Find an available port starting from 8000
    findPort(8000).then(port => {
      serverPort = port;
      console.log(`Found available port: ${port}`);
      
      // Determine if we're in development or production
      const isDev = process.env.NODE_ENV === 'development';
      
      let pythonCommand;
      let args;
      
      if (isDev) {
        // Development: run Python from virtual environment
        const venvPython = path.join(__dirname, '..', 'venv', 'bin', 'python');
        pythonCommand = venvPython;
        args = ['-m', 'schema_validator', '--port', port.toString()];
      } else {
        // Production: run bundled Python executable
        // Map platform names to build directory names
        const platformMap = {
          'darwin': 'mac',
          'win32': 'win', 
          'linux': 'linux'
        };
        const buildDir = platformMap[process.platform] || process.platform;
        const pythonExecutable = path.join(__dirname, '..', 'python-dist', buildDir, 'schema-validator');
        pythonCommand = pythonExecutable;
        args = ['--port', port.toString()];
      }

      console.log(`Starting Python server on port ${port}...`);
      console.log(`Command: ${pythonCommand} ${args.join(' ')}`);

      // Spawn Python process
      pythonProcess = spawn(pythonCommand, args, {
        stdio: ['pipe', 'pipe', 'pipe'],
        env: {
          ...process.env,
          PORT: port.toString()
        }
      });

      // Handle Python process output
      pythonProcess.stdout.on('data', (data) => {
        console.log(`Python stdout: ${data}`);
      });

      pythonProcess.stderr.on('data', (data) => {
        console.error(`Python stderr: ${data}`);
      });

      pythonProcess.on('error', (error) => {
        console.error('Failed to start Python process:', error);
        reject(error);
      });

      pythonProcess.on('exit', (code) => {
        console.log(`Python process exited with code ${code}`);
        if (code !== 0 && code !== null) {
          reject(new Error(`Python process exited with code ${code}`));
        }
      });

      // Wait for the server to start and verify it's running
      setTimeout(async () => {
        try {
          // Test if the server is actually running
          const http = require('http');
          const testRequest = http.get(`http://127.0.0.1:${port}`, (res) => {
            console.log(`Server is responding on port ${port}`);
            resolve(port);
          });
          
          testRequest.on('error', (err) => {
            console.error(`Server test failed: ${err.message}`);
            reject(new Error(`Server not responding on port ${port}: ${err.message}`));
          });
          
          testRequest.setTimeout(5000, () => {
            testRequest.destroy();
            reject(new Error(`Server connection timeout on port ${port}`));
          });
        } catch (error) {
          console.error('Server verification failed:', error);
          reject(error);
        }
      }, 3000);
    }).catch(error => {
      console.error('Port finding failed:', error);
      reject(new Error(`Failed to find available port: ${error.message}`));
    });
  });
}

function stopPythonServer() {
  if (pythonProcess) {
    console.log('Stopping Python server...');
    pythonProcess.kill('SIGTERM');
    
    // Force kill if it doesn't stop gracefully
    setTimeout(() => {
      if (pythonProcess && !pythonProcess.killed) {
        pythonProcess.kill('SIGKILL');
      }
    }, 5000);
    
    pythonProcess = null;
  }
}

// App event handlers
app.whenReady().then(async () => {
  try {
    await startPythonServer();
    createWindow();
  } catch (error) {
    console.error('Failed to start application:', error);
    dialog.showErrorBox('Startup Error', `Failed to start the application: ${error.message}`);
    app.quit();
  }
});

app.on('window-all-closed', () => {
  stopPythonServer();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

app.on('before-quit', () => {
  stopPythonServer();
});

// Handle app protocol for deep linking (optional)
app.setAsDefaultProtocolClient('schema-validator');

// IPC handlers
ipcMain.handle('get-app-version', () => {
  return app.getVersion();
});

ipcMain.handle('check-for-updates', () => {
  autoUpdater.checkForUpdatesAndNotify();
});

ipcMain.handle('restart-app', () => {
  autoUpdater.quitAndInstall();
});
