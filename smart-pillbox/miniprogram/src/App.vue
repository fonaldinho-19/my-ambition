<script setup>
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'

onLaunch(() => {
  console.log('智能药盒小程序启动')
})

onShow(() => {
  console.log('小程序显示')
})

onHide(() => {
  console.log('小程序隐藏')
})
</script>

<style>
/* 全局样式 */
page {
  background-color: #f5f6fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
</style>
