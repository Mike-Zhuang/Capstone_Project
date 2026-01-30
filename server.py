import socket
import json
import time
import threading
from detect import AirQualityMonitor
from react import EmergencyDecisionTree
from predict import ResourcePredictor

# 1. 初始化各个模块
monitor = AirQualityMonitor()
decision_system = EmergencyDecisionTree()
predictor = ResourcePredictor()

# 预先训练预测模型 (直接用队友的逻辑)
print("正在初始化 AI 预测模型...")
X, y_water, y_food, y_oxygen = predictor.generate_training_data(num_people=50)
predictor.train_model(X, y_water)

def start_server():
    # 建立 TCP 服务器
    host = '127.0.0.1'
    port = 65432
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"服务器启动，监听 {host}:{port}...")
    print("等待 Unity 连接...")
    
    conn, addr = server_socket.accept()
    print(f"Unity 已连接: {addr}")

    try:
        while True:
            # --- A. 获取实时传感器数据 (来自 detect.py) ---
            sensor_data = monitor.simulate_sensor_data()
            
            # --- B. 检查异常并生成决策 (来自 react.py) ---
            # 我们把 sensor_data 转换成 react 需要的格式
            status_report = {
                "sensor": sensor_data,
                "alert_message": "SYSTEM NORMAL",
                "action_plan": "MONITORING",
                "prediction_water": 0
            }

            # 逻辑连接：如果辐射高 -> 查决策树
            if sensor_data["radiation"] > monitor.RADIATION_THRESHOLD:
                decision = decision_system.make_decision("radiation_high", "high")
                status_report["alert_message"] = "WARNING: HIGH RADIATION"
                status_report["action_plan"] = f"ACTION: {decision['immediate_action']} | RESOURCE: {decision['resources_needed']}"
            
            elif sensor_data["toxic_gas"] > monitor.TOXIC_GAS_THRESHOLD:
                decision = decision_system.make_decision("toxic_gas", "medium")
                status_report["alert_message"] = "WARNING: TOXIC GAS DETECTED"
                status_report["action_plan"] = f"ACTION: {decision['immediate_action']}"

            elif sensor_data["oxygen"] < 19.5:
                 status_report["alert_message"] = "WARNING: LOW OXYGEN"
                 status_report["action_plan"] = "ACTION: ELECTROLYSIS SYSTEM ACTIVE"

            # --- C. 获取预测数据 (来自 predict.py) ---
            # 简单起见，我们预测明天的水消耗
            # 参数: current_day=100, num_people=50
            future_pred = predictor.predict(100, 50, future_days=1) 
            status_report["prediction_water"] = round(future_pred[0], 1)

            # --- D. 打包发送给 Unity ---
            # json.dumps 把字典变成字符串, encode 转成字节
            json_str = json.dumps(status_report)
            # 发送数据长度 + 数据本身 (防止粘包，这里简单处理，直接发带换行符的)
            conn.sendall((json_str + "\n").encode('utf-8'))
            
            print(f"发送数据: {json_str}")
            time.sleep(1) # 每秒发送一次

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    start_server()