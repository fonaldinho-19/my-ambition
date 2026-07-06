# 智能药盒 - API 接口规范

## 整体数据流

ESP8266(硬件) ──POST──→ 后端服务器(Flask) ──GET──→ 微信小程序
 192.168.x.x:8080       192.168.x.x:5000          手机端

---

## 一、ESP8266 → 后端（硬件同学负责）

### POST /api/sensor-data

ESP8266 每 5 秒向 Flask 后端发送一次传感器数据。

请求体 JSON：
`json
{
  "device_id": "pillbox_001",
  "temperature": 25.6,
  "humidity": 58.3,
  "weight": 152.7,
  "timestamp": "2026-07-06 10:30:05"
}
`

| 字段 | 类型 | 说明 |
|------|------|------|
| device_id | string | 设备编号，区分多个药盒 |
| temperature | float | 温度（℃），精确到 0.1 |
| humidity | float | 湿度（%RH），精确到 0.1 |
| weight | float | 当前重量（克），精确到 0.1 |
| timestamp | string | 采集时间，格式 YYYY-MM-DD HH:MM:SS |

返回：
`json
{ "code": 200, "message": "ok" }
`

---

## 二、后端 → 小程序（你和同学负责）

### 1. GET /api/latest?device_id=pillbox_001

获取最新一条传感器数据。

返回：
`json
{
  "code": 200,
  "data": {
    "temperature": 25.6,
    "humidity": 58.3,
    "weight": 152.7,
    "timestamp": "2026-07-06 10:30:05"
  }
}
`

---

### 2. GET /api/history?device_id=pillbox_001&hours=24

获取历史传感器数据（用于绘制曲线图）。

参数：
| 参数 | 默认值 | 说明 |
|------|--------|------|
| device_id | 必填 | 设备编号 |
| hours | 24 | 查最近多少小时 |

返回：
`json
{
  "code": 200,
  "data": [
    { "temperature": 25.6, "humidity": 58.3, "weight": 152.7, "timestamp": "2026-07-06 10:30:05" },
    { "temperature": 25.7, "humidity": 58.1, "weight": 152.5, "timestamp": "2026-07-06 10:30:10" }
  ]
}
`

---

### 3. GET /api/medication?device_id=pillbox_001&date=2026-07-06

获取吃药记录（后端根据重量突变自动判断）。

判断逻辑：
- 如果当前重量相比上一次下降超过 10g → 判定为"已取药"
- 每条记录包含取药时间和当时重量

返回：
`json
{
  "code": 200,
  "data": [
    { "time": "2026-07-06 08:05:00", "weight_before": 152.7, "weight_after": 140.2, "taken": true },
    { "time": "2026-07-06 12:05:00", "weight_before": 140.2, "weight_after": 140.1, "taken": false },
    { "time": "2026-07-06 18:05:00", "weight_before": 140.1, "weight_after": 128.5, "taken": true }
  ]
}
`

| 字段 | 说明 |
|------|------|
| time | 检测到重量变化的时间 |
| weight_before | 变化前的重量（g） |
| weight_after | 变化后的重量（g） |
| taken | true=已吃药，false=未检测到取药 |

---

## 三、给硬件同学的要求

ESP8266 上需要实现：
1. 连接同一局域网的 WiFi
2. 每 5 秒读取 DHT11/DHT22（温湿度）+ HX711（称重）
3. 向 http://<后端电脑IP>:5000/api/sensor-data 发送 POST 请求
4. 请求体按上面的 JSON 格式

硬件同学只需要关心 **POST /api/sensor-data** 这一个接口！
