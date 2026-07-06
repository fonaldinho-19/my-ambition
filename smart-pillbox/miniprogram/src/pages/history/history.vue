<template>
  <view class="container">
    <view class="header">
      <text class="title">📊 历史数据</text>
    </view>

    <!-- 时间范围选择 -->
    <view class="time-tabs">
      <view
        v-for="h in timeOptions"
        :key="h.value"
        class="time-tab"
        :class="{ active: selectedHours === h.value }"
        @click="switchTime(h.value)"
      >
        {{ h.label }}
      </view>
    </view>

    <!-- 温度曲线（简易柱状图） -->
    <view class="card">
      <text class="chart-title">🌡️ 温度变化 (℃)</text>
      <view class="bar-chart">
        <view
          v-for="(item, index) in chartData"
          :key="index"
          class="bar-wrapper"
        >
          <view
            class="bar bar-temp"
            :style="{ height: ((item.temperature - minTemp) / (maxTemp - minTemp || 1) * 160) + 'rpx' }"
          ></view>
          <text class="bar-label">{{ item.time_label }}</text>
        </view>
      </view>
    </view>

    <!-- 湿度曲线 -->
    <view class="card">
      <text class="chart-title">💧 湿度变化 (%RH)</text>
      <view class="bar-chart">
        <view
          v-for="(item, index) in chartData"
          :key="index"
          class="bar-wrapper"
        >
          <view
            class="bar bar-humi"
            :style="{ height: ((item.humidity - minHumi) / (maxHumi - minHumi || 1) * 160) + 'rpx' }"
          ></view>
          <text class="bar-label">{{ item.time_label }}</text>
        </view>
      </view>
    </view>

    <!-- 重量曲线 -->
    <view class="card">
      <text class="chart-title">⚖️ 重量变化 (g)</text>
      <view class="bar-chart">
        <view
          v-for="(item, index) in chartData"
          :key="index"
          class="bar-wrapper"
        >
          <view
            class="bar bar-weight"
            :style="{ height: ((item.weight - minWeight) / (maxWeight - minWeight || 1) * 160) + 'rpx' }"
          ></view>
          <text class="bar-label">{{ item.time_label }}</text>
        </view>
      </view>
    </view>

    <!-- 吃药记录列表 -->
    <view class="card">
      <text class="chart-title">📋 近期吃药记录</text>
      <view v-if="medRecords.length > 0">
        <view
          v-for="(item, index) in medRecords"
          :key="index"
          class="med-item"
        >
          <text class="med-time">{{ item.time }}</text>
          <text class="med-change">
            {{ item.weight_before }}g → {{ item.weight_after }}g
            <text class="med-arrow">↓{{ (item.weight_before - item.weight_after).toFixed(1) }}g</text>
          </text>
          <text :class="item.taken ? 'tag-ok' : 'tag-no'">
            {{ item.taken ? '已服药' : '未服药' }}
          </text>
        </view>
      </view>
      <view v-else class="empty-tip">暂无吃药记录</view>
    </view>

    <!-- 底部导航 -->
    <view class="tab-bar">
      <view class="tab-item" @click="goIndex">
        <text>🏠 首页</text>
      </view>
      <view class="tab-item active">
        <text>📊 历史</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getHistory, getMedication } from '@/utils/api.js'

const selectedHours = ref(6)
const timeOptions = [
  { label: '1小时', value: 1 },
  { label: '6小时', value: 6 },
  { label: '24小时', value: 24 },
  { label: '3天', value: 72 }
]

const rawHistory = ref([])
const medRecords = ref([])

// 采样后用于图表的数据（最多显示30个点）
const chartData = computed(() => {
  const data = rawHistory.value
  if (data.length <= 30) {
    return data.map(d => ({
      ...d,
      time_label: d.timestamp.slice(11, 16)  // HH:MM
    }))
  }
  // 均匀采样
  const step = Math.floor(data.length / 30)
  const sampled = []
  for (let i = 0; i < data.length; i += step) {
    sampled.push({
      ...data[i],
      time_label: data[i].timestamp.slice(11, 16)
    })
  }
  return sampled.slice(0, 30)
})

const minTemp = computed(() => Math.min(...chartData.value.map(d => d.temperature), 20))
const maxTemp = computed(() => Math.max(...chartData.value.map(d => d.temperature), 30))
const minHumi = computed(() => Math.min(...chartData.value.map(d => d.humidity), 30))
const maxHumi = computed(() => Math.max(...chartData.value.map(d => d.humidity), 70))
const minWeight = computed(() => Math.min(...chartData.value.map(d => d.weight), 100))
const maxWeight = computed(() => Math.max(...chartData.value.map(d => d.weight), 160))

async function fetchHistory() {
  try {
    rawHistory.value = await getHistory(selectedHours.value)
  } catch (err) {
    console.error('获取历史数据失败:', err.message)
  }
}

async function fetchMedication() {
  try {
    medRecords.value = await getMedication('')
  } catch (err) {
    console.error('获取吃药记录失败:', err.message)
  }
}

async function switchTime(hours) {
  selectedHours.value = hours
  await fetchHistory()
  await fetchMedication()
}

function goIndex() {
  uni.navigateBack()
}

onMounted(() => {
  fetchHistory()
  fetchMedication()
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
  padding: 30rpx 0 20rpx;
}
.title {
  font-size: 40rpx;
  font-weight: bold;
  color: #2c3e50;
}

/* 时间选择 */
.time-tabs {
  display: flex;
  gap: 16rpx;
  margin-bottom: 20rpx;
}
.time-tab {
  flex: 1;
  text-align: center;
  padding: 16rpx 0;
  background: #fff;
  border-radius: 12rpx;
  font-size: 24rpx;
  color: #666;
  box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.04);
}
.time-tab.active {
  background: #3498db;
  color: #fff;
  font-weight: bold;
}

/* 图表卡片 */
.card {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
}
.chart-title {
  display: block;
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

/* 简易柱状图 */
.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 200rpx;
  border-bottom: 2rpx solid #eee;
}
.bar-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}
.bar {
  width: 16rpx;
  border-radius: 8rpx 8rpx 0 0;
  min-height: 4rpx;
  transition: height 0.3s ease;
}
.bar-temp { background: linear-gradient(to top, #e74c3c, #f39c12); }
.bar-humi { background: linear-gradient(to top, #2980b9, #3498db); }
.bar-weight { background: linear-gradient(to top, #27ae60, #2ecc71); }
.bar-label {
  font-size: 16rpx;
  color: #999;
  margin-top: 8rpx;
  transform: rotate(-30deg);
  white-space: nowrap;
}

/* 吃药记录 */
.med-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18rpx 0;
  border-bottom: 1rpx solid #f5f5f5;
}
.med-time { font-size: 26rpx; color: #333; }
.med-change { font-size: 24rpx; color: #666; }
.med-arrow { color: #e74c3c; font-weight: bold; }
.tag-ok {
  font-size: 22rpx;
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  background: #eafaf1;
  color: #27ae60;
}
.tag-no {
  font-size: 22rpx;
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  background: #fdedec;
  color: #e74c3c;
}

.empty-tip {
  text-align: center;
  color: #ccc;
  font-size: 26rpx;
  padding: 40rpx 0;
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
