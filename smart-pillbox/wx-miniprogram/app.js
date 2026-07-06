// app.js - Mini Program entry
App({
  globalData: {
    // Change to your LAN IP when deploying, e.g. 'http://192.168.1.100:5000'
    baseUrl: 'http://localhost:5000',
    deviceId: 'pillbox_001'
  },

  onLaunch() {
    console.log('Smart Pillbox started')
  }
})