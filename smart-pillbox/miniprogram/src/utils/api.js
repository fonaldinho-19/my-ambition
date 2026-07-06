// ============================================================
//  API 工具层 - 封装所有后端接口调用
// ============================================================

// ⚠️ 部署时改为你电脑的局域网 IP，例如 'http://192.168.1.100:5000'
const BASE_URL = 'http://localhost:5000'

const DEVICE_ID = 'pillbox_001'

export function request(url, params = {}) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      data: { device_id: DEVICE_ID, ...params },
      timeout: 5000,
      success: (res) => {
        if (res.statusCode === 200 && res.data.code === 200) {
          resolve(res.data.data)
        } else {
          reject(new Error(res.data?.message || '请求失败'))
        }
      },
      fail: (err) => {
        reject(new Error('网络错误，请检查后端是否启动'))
      }
    })
  })
}

// 获取最新数据
export function getLatestData() {
  return request('/api/latest')
}

// 获取历史数据
export function getHistory(hours = 24) {
  return request('/api/history', { hours })
}

// 获取吃药记录
export function getMedication(date) {
  return request('/api/medication', { date })
}
