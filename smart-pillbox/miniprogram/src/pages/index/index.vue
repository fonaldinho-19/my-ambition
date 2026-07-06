<template>
  <view class="container">
    <!-- 标题栏 -->
    <view class="header">
      <text class="title">💊 智能药盒</text>
      <text class="subtitle">设备: {{ deviceId }}</text>
    </view>

    <!-- 温湿度卡片 -->
    <view class="card-row">
      <view class="card card-temp">
        <view class="card-icon">🌡️</view>
        <text class="card-value">{{ data.temperature }}°</text>
        <text class="card-label">温度</text>
      </view>
      <view class="card card-humi">
        <view class="card-icon">💧</view>
        <text class="card-value">{{ data.humidity }}%</text>
        <text class="card-label">湿度</text>
      </view>
    </view>

    <!-- 重量卡片 -->
    <view class="card card-weight">
      <view class="card-icon">⚖️</view>
      <text class="card-value big">{{ data.weight }}</text>
      <text class="card-unit">克</text>
      <text class="card-label">当前重量</text>
    </view>

    <!-- 今日吃药状态 -->
    <view class="card card-med">
      <text class="section-title">📋 今日吃药记录</text>
      <view class="med-list">
        <view
          v-for="(item, index) in medication"
          :key="index"
          class="med-item"
          :class="{ taken: item.taken, missed: !item.taken }"
        >
          <text class="med-time">{{ item.time_label }}</text>
          <text class="med-status">
            {{ item.taken ? '✅ 已服药' : '❌ 未服药' }}
          </text>
        </view>
      </view>
      <view v-if="medication.length === 0" class="empty-tip">
        暂无记录，等待数据...
      </view>
    </view>

    <!-- 更新时间 -->
    <view class="update-time">
      <text>更新于 {{ data.timestamp || '--' }}</text>
      <text class="refresh-btn" @click="fetchData">🔄 刷新</text>
    </view>

    <!-- 底部导航 -->
    <view class="tab-bar">
      <view class="tab-item active">
        <text>🏠 首页</text>
      </view>
      <view class="tab-item" @click="goHistory">
        <text>📊 历史</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { getLatestData, getMedication } from '@/utils/api.js'

const deviceId = 'pillbox_001'

const data = reactive({
  temperature: '--',
  humidity: '--',
  weight: '--',
  timestamp: ''
})

const medication = ref([])

// 默认一天 4 次吃药的时段标签
const TIME_SLOTS = [
  { label: '早上 (8:00)', taken: null },
  { label: '中午 (12:00)', taken: null },
  { label: '晚上 (18:00)', taken: null },
  { label: '睡前 (22:00)', taken: null }
]

let timer = null

async function fetchData() {
  try {
    const result = await getLatestData()
    data.temperature = result.temperature
    data.humidity = result.humidity
    data.weight = result.weight
    data.timestamp = result.timestamp
  } catch (err) {
    console.error('获取数据失败:', err.message)
  }
}

async function fetchMedication() {
  try {
    const today = new Date().toISOString().slice(0, 10)
    const records = await getMedication(today)

    // 将真实记录映射到 4 个时段
    medication.value = TIME_SLOTS.map(slot => {
      const found = records.find(r => {
        const hour = new Date(r.time).getHours()
        const slotHour = parseInt(slot.label.match(/\d+/)?.[0] || 0)
        return Math.abs(hour - slotHour) <= 1 && r.taken
      })
      return {
        time_label: slot.label,
        taken: !!found
      }
    })
  } catch (err) {
    console.error('获取吃药记录失败:', err.message)
  }
}

function goHistory() {
  uni.navigateTo({ url: '/pages/history/history' })
}

onMounted(() => {
  fetchData()
  fetchMedication()
  // 每 10 秒自动刷新
  timer = setInterval(() => {
    fetchData()
    fetchMedication()
  }, 10000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.container {
  padding: 20rpx 30rpx;
  padding-bottom: 120rpx;
  min-height: 100vh;
}

.header {
  text-align: center;
  padding: 40rpx 0 30rpx;
}
.title {
  font-size: 44rpx;
  font-weight: bold;
  color: #2c3e50;
}
.subtitle {
  display: block;
  font-size: 24rpx;
  color: #999;
  margin-top: 10rpx;
}

/* 卡片通用 */
.card-row {
  display: flex;
  gap: 20rpx;
  margin-bottom: 20rpx;
}
.card {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
  text-align: center;
}
.card-row .card {
  flex: 1;
  margin-bottom: 0;
}
.card-icon { font-size: 48rpx; margin-bottom: 10rpx; }
.card-value {
  display: block;
  font-size: 56rpx;
  font-weight: bold;
  color: #2c3e50;
}
.card-value.big { font-size: 72rpx; }
.card-unit {
  font-size: 28rpx;
  color: #999;
  margin-left: 8rpx;
}
.card-label {
  display: block;
  font-size: 24rpx;
  color: #999;
  margin-top: 8rpx;
}

.card-temp { border-top: 6rpx solid #e74c3c; }
.card-humi { border-top: 6rpx solid #3498db; }
.card-weight { border-top: 6rpx solid #27ae60; }

/* 吃药记录 */
.section-title {
  display: block;
  font-size: 30rpx;
  font-weight: bold;
  text-align: left;
  margin-bottom: 20rpx;
}
.med-item {
  display: flex;
  justify-content: space-between;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}
.med-item:last-child { border-bottom: none; }
.med-time { font-size: 28rpx; color: #333; }
.med-status { font-size: 28rpx; }
.med-item.taken .med-status { color: #27ae60; }
.med-item.missed .med-status { color: #e74c3c; }

.empty-tip {
  text-align: center;
  color: #ccc;
  font-size: 26rpx;
  padding: 40rpx 0;
}

/* 更新时间 */
.update-time {
  text-align: center;
  font-size: 24rpx;
  color: #bbb;
  margin-top: 20rpx;
}
.refresh-btn {
  color: #3498db;
  margin-left: 20rpx;
}

/* 底部导航 */
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  background: #fff;
  border-top: 1rpx solid #eee;
  padding: 15rpx 0;
  padding-bottom: env(safe-area-inset-bottom);
}
.tab-item {
  flex: 1;
  text-align: center;
  font-size: 26rpx;
  color: #999;
}
.tab-item.active { color: #3498db; font-weight: bold; }
</style>
