import asyncio
import websockets
import json
import datetime

# 模拟获取温度、湿度和光照信息的函数
def get_sensor_data():
    # 这里假设获取到了温度、湿度和光照信息，实际中需要根据您的传感器或设备来获取数据
    temperature = 25.5  # 摄氏度
    humidity = 50.0     # 百分比
    light = 500         # 光照强度，单位为 lux
    return temperature, humidity, light

# 客户端连接时触发的处理函数
async def handle_connection(websocket, path):
    duan = 1
    licheng = 0
    print(f"Client connected from {websocket.remote_address}")
    try:
        async def send_sensor_data():
            nonlocal duan, licheng
            while True:
                if licheng >= 30:
                    licheng = 0
                # 获取当前时间
                current_time = datetime.datetime.now().timestamp()
                # 获取温度、湿度和光照信息
                temperature, humidity, light = get_sensor_data()
                # 构建回复的 JSON 数据
                reply_data = {
                    "time": current_time,
                    "temperature": temperature,
                    "relative humidity": humidity,
                    "light intensity": light,
                    "duan": str(duan),
                    "licheng": str(licheng)
                }
                reply_json = json.dumps(reply_data)
                await websocket.send(reply_json)
                await websocket.recv()  # 等待客户端发送请求
                licheng += 1

        # 创建定时器任务，每隔10秒更新duan的值
        async def update_duan():
            nonlocal duan 
            while True:
                await asyncio.sleep(15)
                duan += 1
                if duan == 5:
                    duan = 1

        # 开始定时器任务
        send_sensor_data_task = asyncio.create_task(send_sensor_data())
        update_duan_task = asyncio.create_task(update_duan())

        # 等待定时器任务结束
        await asyncio.gather(send_sensor_data_task, update_duan_task)

    finally:
        print(f"Client {websocket.remote_address} disconnected")
# 启动 WebSocket 服务器
start_server = websockets.serve(handle_connection, "localhost", 8765)

# 运行事件循环，保持服务器运行
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
