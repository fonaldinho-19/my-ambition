// pages/history/history.js
const api = require('../../utils/api.js')

Page({
  data: {
    selectedHours: 6,
    timeOptions: [
      { label: '1小时', value: 1 },
      { label: '6小时', value: 6 },
      { label: '24小时', value: 24 },
      { label: '3天', value: 72 }
    ],
    chartData: [],
    medRecords: [],
    minTemp: 20, maxTemp: 30,
    minHumi: 30, maxHumi: 70,
    minWeight: 100, maxWeight: 160
  },

  onLoad() {
    this.fetchAll()
  },

  async fetchAll() {
    await Promise.all([this.fetchHistory(), this.fetchMedication()])
  },

  async switchTime(e) {
    const hours = e.currentTarget.dataset.hours
    this.setData({ selectedHours: hours })
    await this.fetchAll()
  },

  async fetchHistory() {
    try {
      const rawData = await api.getHistory(this.data.selectedHours)

      // 采样（最多显示30个点）
      let chartData = rawData
      if (rawData.length > 30) {
        const step = Math.floor(rawData.length / 30)
        const sampled = []
        for (let i = 0; i < rawData.length; i += step) {
          sampled.push(rawData[i])
        }
        chartData = sampled.slice(0, 30)
      }

      chartData = chartData.map(d => ({
        ...d,
        time_label: d.timestamp ? d.timestamp.slice(11, 16) : '--' // HH:MM
      }))

      // 计算范围
      const temps = chartData.map(d => d.temperature || 0)
      const humis = chartData.map(d => d.humidity || 0)
      const weights = chartData.map(d => d.weight || 0)

      this.setData({
        chartData,
        minTemp: Math.min(...(temps.length ? temps : [20]), 20),
        maxTemp: Math.max(...(temps.length ? temps : [30]), 30),
        minHumi: Math.min(...(humis.length ? humis : [30]), 30),
        maxHumi: Math.max(...(humis.length ? humis : [70]), 70),
        minWeight: Math.min(...(weights.length ? weights : [100]), 100),
        maxWeight: Math.max(...(weights.length ? weights : [160]), 160)
      })
    } catch (err) {
      console.error('获取历史数据失败:', err.message)
    }
  },

  async fetchMedication() {
    try {
      const records = await api.getMedication('')
      this.setData({ medRecords: records || [] })
    } catch (err) {
      console.error('获取吃药记录失败:', err.message)
    }
  }
})