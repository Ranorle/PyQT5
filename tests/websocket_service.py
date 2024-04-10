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
    # 打印客户端连接信息
    print(f"Client connected from {websocket.remote_address}")
    try:
        # 不断循环，接收客户端发送的消息并回传
        async for message in websocket:
            print(f"Received message: {message}")
            # 如果收到 "chuanganqishuju" 消息，则发送 JSON 回复
            if message == "chuanganqishuju":
                # 获取当前时间
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 获取温度、湿度和光照信息
                temperature, humidity, light = get_sensor_data()
                # 构建回复的 JSON 数据
                reply_data = {
                    "time": current_time,
                    "temperature": temperature,
                    "humidity": humidity,
                    "light": light
                }
                reply_json = json.dumps(reply_data)
                await websocket.send(reply_json)
            else:
                # 回传收到的消息
                await websocket.send(message)
    finally:
        print(f"Client {websocket.remote_address} disconnected")

# 启动 WebSocket 服务器
start_server = websockets.serve(handle_connection, "localhost", 8765)

# 运行事件循环，保持服务器运行
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
