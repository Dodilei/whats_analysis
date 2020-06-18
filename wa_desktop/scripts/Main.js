const { app, BrowserWindow } = require('electron');

function createWindow() {

    let win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        },
        frame: false,
        titleBarStyle: 'customButtonsOnHover'
    })

    win.loadURL('http://localhost:3000');
}

app.whenReady().then(createWindow)