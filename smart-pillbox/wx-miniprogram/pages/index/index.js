// pages/index/index.js
const api = require('../../utils/api.js')

// 默认一天 4 次吃药的时段
const TIME_SLOTS = [
  { label: '早上 (8:00)', taken: null },
  { label: '中午 (12:00)', taken: null },
  { label: '晚上 (18:00)', taken: null },
  { label: '睡前 (22:00)', taken: null }
]

Page({
  data: {
    temperature: '--',
    humidity: '--',
    weight: '--',
    timestamp: '',
    medication: []
  },

  onLoad() {
    this.fetchAll()
  },

  onShow() {
    this.fetchAll()
  },

  onPullDownRefresh() {
    this.fetchAll().then(() => wx.stopPullDownRefresh())
  },

  async fetchAll() {
    await Promise.all([this.fetchData(), this.fetchMedication()])
  },

  async fetchData() {
    try {
      const data = await api.getLatestData()
      this.setData({
        temperature: data.temperature,
        humidity: data.humidity,
        weight: data.weight,
        timestamp: data.timestamp
      })
    } catch (err) {
      console.error('获取数据失败:', err.message)
    }
  },

  async fetchMedication() {
    try {
      const today = new Date().toISOString().slice(0, 10)
      const records = await api.getMedication(today)

      const medication = TIME_SLOTS.map(slot => {
        var found = null
        if (records && records.length > 0) {
          found = records.find(function (r) {
            if (!r || !r.time) return false
            var hour = new Date(r.time.replace(/-/g, '/')).getHours()
            var match = slot.label.match(/\d+/)
            var slotHour = match ? parseInt(match[0]) : 0
            return Math.abs(hour - slotHour) <= 1 && r.taken
          })
        }
        return {
          time_label: slot.label,
          taken: !!found
        }
      })
      this.setData({ medication: medication })
    } catch (err) {
      console.error('获取吃药记录失败:', err.message)
    }
  }
})