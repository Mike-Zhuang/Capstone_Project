import socket
import json
import time
from detect import AirQualityMonitor
from react import EmergencyDecisionTree
from predict import ResourcePredictor

# 初始化模块
monitor = AirQualityMonitor()
decision_system = EmergencyDecisionTree()
predictor = ResourcePredictor()

# 预先训练模型 (回答你的痛点2: 这里就是在训练一个线性回归模型，用来预测未来的水资源消耗)
print("正在训练 AI 资源消耗模型...")
X_train, y_water, y_food, y_oxygen = predictor.generate_training_data(num_people=50)
predictor.train_model(X_train, y_water)
print("✅ 模型就绪！")

def start_server():
    host = '127.0.0.1'
    port = 65500 # 保持和你Unity设置的一样
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"\n🎧 等待 Unity 连接中...")
        conn, addr = server_socket.accept()
        print(f"✅ Unity 已连接！进入【导演模式】")
        print("------------------------------------------------")
        print("请在终端输入指令控制场景：")
        print(" [n]  -> 恢复正常 (Normal)")
        print(" [r]  -> 触发辐射 (Radiation)")
        print(" [g]  -> 触发毒气 (Gas)")
        print(" [o]  -> 触发缺氧 (Low Oxygen)")
        print(" [q]  -> 退出程序")
        print("------------------------------------------------")

        # 默认状态
        current_data = {
            "radiation": 10, "toxic_gas": 0, "co2": 400, "oxygen": 21
        }

        while True:
            # 等待你的输入
            cmd = input("请输入指令 (n/r/g/o): ").strip().lower()
            
            if cmd == 'q':
                break
            
            # 根据指令修改数据
            if cmd == 'n':
                print(">>> 切换到：一切正常")
                current_data = {"radiation": 10, "toxic_gas": 0, "co2": 400, "oxygen": 21}
            elif cmd == 'r':
                print(">>> 切换到：☢️ 高辐射危机")
                current_data = {"radiation": 500, "toxic_gas": 0, "co2": 400, "oxygen": 21}
            elif cmd == 'g':
                print(">>> 切换到：☠️ 毒气泄漏")
                current_data = {"radiation": 10, "toxic_gas": 200, "co2": 400, "oxygen": 21}
            elif cmd == 'o':
                print(">>> 切换到：💨 严重缺氧")
                current_data = {"radiation": 10, "toxic_gas": 0, "co2": 400, "oxygen": 15}
            else:
                print("无效指令，保持原状")
                continue # 跳过发送，重新输入

            # 生成报告
            status_report = {
                "sensor": current_data,
                "alert_message": "SYSTEM NORMAL",
                "action_plan": "MONITORING",
                "prediction_water": 0.0
            }

            # 决策逻辑 (调用队友的 react.py)
            if current_data["radiation"] > 100:
                decision = decision_system.make_decision("radiation_high", "high")
                status_report["alert_message"] = "WARNING: HIGH RADIATION"
                status_report["action_plan"] = f"ACT: {decision['immediate_action']}"
            elif current_data["toxic_gas"] > 50:
                status_report["alert_message"] = "WARNING: TOXIC GAS"
                status_report["action_plan"] = "ACT: SEAL VENTS"
            elif current_data["oxygen"] < 19.5:
                status_report["alert_message"] = "WARNING: LOW OXYGEN"
                status_report["action_plan"] = "ACT: ELECTROLYSIS ON"

            # 预测逻辑 (调用队友的 predict.py)
            # 解释痛点2: 这里预测的是“明天”的水消耗，并在Unity屏幕上显示数字
            future = predictor.predict(100, 50, future_days=1)
            status_report["prediction_water"] = round(future[0], 1)

            # 发送数据
            json_str = json.dumps(status_report)
            conn.sendall((json_str + "\n").encode('utf-8'))
            print(f"数据已发送至 Unity")

    except Exception as e:
        print(f"错误: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()