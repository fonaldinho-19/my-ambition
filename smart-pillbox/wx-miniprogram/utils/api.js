// ============================================================
//  API helper - handles all backend requests
//  When testing on phone: change baseUrl in app.js to LAN IP
// ============================================================

const app = getApp()

function request(url, params) {
  params = params || {}
  var baseUrl = app.globalData.baseUrl
  var deviceId = app.globalData.deviceId
  return new Promise(function (resolve, reject) {
    wx.request({
      url: baseUrl + url,
      data: Object.assign({ device_id: deviceId }, params),
      timeout: 5000,
      success: function (res) {
        if (res.statusCode === 200 && res.data.code === 200) {
          resolve(res.data.data)
        } else {
          reject(new Error(res.data ? res.data.message : 'Request failed'))
        }
      },
      fail: function () {
        reject(new Error('Network error - is the backend running?'))
      }
    })
  })
}

function getLatestData() {
  return request('/api/latest')
}

function getHistory(hours) {
  return request('/api/history', { hours: hours || 24 })
}

function getMedication(date) {
  return request('/api/medication', { date: date || '' })
}

module.exports = { getLatestData: getLatestData, getHistory: getHistory, getMedication: getMedication }