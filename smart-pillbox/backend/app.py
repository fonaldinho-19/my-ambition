from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import random
import threading
import time

app = Flask(__name__)

# ============================================================
#  内存数据存储（生产环境应换数据库，开发阶段用内存够了）
# ============================================================
sensor_records = []          # 所有传感器原始数据
medication_records = []      # 吃药记录

# ============================================================
#  模拟数据生成器（开发阶段自动生成假数据，方便调试）
# ============================================================
def generate_mock_data():
    '''在后台线程中每 5 秒生成一条模拟传感器数据'''
    base_temp = 25.0
    base_humidity = 55.0
    base_weight = 150.0

    while True:
        temp = round(base_temp + random.uniform(-1.5, 1.5), 1)
        humi = round(base_humidity + random.uniform(-5, 5), 1)

        # 模拟吃药行为：每 6 小时左右重量骤降约 10-20g
        hour = datetime.now().hour
        if hour in [8, 12, 18, 22] and datetime.now().minute < 2:
            base_weight -= random.uniform(10, 20)

        weight = round(base_weight + random.uniform(-1, 1), 1)
        record = {
            'temperature': max(0, temp),
            'humidity': max(0, min(100, humi)),
            'weight': max(0, weight),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # 检测吃药事件（重量骤降 > 10g）
        if sensor_records:
            last_weight = sensor_records[-1]['weight']
            if last_weight - weight > 10:
                medication_records.append({
                    'time': record['timestamp'],
                    'weight_before': last_weight,
                    'weight_after': weight,
                    'taken': True
                })

        sensor_records.append(record)
        # 只保留最近 7 天的数据
        if len(sensor_records) > 7 * 24 * 60 * 12:
            sensor_records.pop(0)

        time.sleep(5)

# ============================================================
#  API 路由
# ============================================================

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    '''接收 ESP8266 发来的传感器数据'''
    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '数据格式错误'}), 400

    required_fields = ['device_id', 'temperature', 'humidity', 'weight', 'timestamp']
    for field in required_fields:
        if field not in data:
            return jsonify({'code': 400, 'message': f'缺少字段: {field}'}), 400

    record = {
        'temperature': data['temperature'],
        'humidity': data['humidity'],
        'weight': data['weight'],
        'timestamp': data['timestamp']
    }

    # 检测吃药事件
    if sensor_records:
        last_weight = sensor_records[-1]['weight']
        if last_weight - data['weight'] > 10:
            medication_records.append({
                'time': data['timestamp'],
                'weight_before': last_weight,
                'weight_after': data['weight'],
                'taken': True
            })

    sensor_records.append(record)
    return jsonify({'code': 200, 'message': 'ok'})


@app.route('/api/latest', methods=['GET'])
def get_latest():
    '''获取最新一条数据'''
    device_id = request.args.get('device_id', 'pillbox_001')

    if not sensor_records:
        return jsonify({'code': 404, 'message': '暂无数据', 'data': None})

    return jsonify({
        'code': 200,
        'data': sensor_records[-1]
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    '''获取历史数据（支持按小时筛选）'''
    device_id = request.args.get('device_id', 'pillbox_001')
    hours = int(request.args.get('hours', 24))

    cutoff = datetime.now() - timedelta(hours=hours)
    filtered = [
        r for r in sensor_records
        if datetime.strptime(r['timestamp'], '%Y-%m-%d %H:%M:%S') >= cutoff
    ]

    return jsonify({
        'code': 200,
        'data': filtered
    })


@app.route('/api/medication', methods=['GET'])
def get_medication():
    '''获取吃药记录'''
    device_id = request.args.get('device_id', 'pillbox_001')
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    filtered = [
        r for r in medication_records
        if r['time'].startswith(date_str)
    ]

    return jsonify({
        'code': 200,
        'data': filtered
    })


# ============================================================
#  启动
# ============================================================
if __name__ == '__main__':
    # 启动模拟数据生成线程
    mock_thread = threading.Thread(target=generate_mock_data, daemon=True)
    mock_thread.start()
    print('=' * 50)
    print('  智能药盒 Mock 后端已启动')
    print('  接口文档: smart-pillbox/api-spec.md')
    print('  本机地址: http://localhost:5000')
    print('  局域网地址: http://<本机IP>:5000')
    print('=' * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
