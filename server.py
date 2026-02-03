import socket
import json
import time
from detect import AirQualityMonitor
from react import EmergencyDecisionTree
from predict import ResourcePredictor

# Initialize modules
monitor = AirQualityMonitor()
decision_system = EmergencyDecisionTree()
predictor = ResourcePredictor()

# Pre-train the model (training a linear regression model to predict future water consumption)
print("\n" + "="*50)
print("🚀 UNDERGROUND SHELTER AI SYSTEM")
print("="*50)
X_train, y_water, y_food, y_oxygen = predictor.generate_training_data(num_people=50)
predictor.train_model(X_train, y_water)
print("\n" + "="*50)
print("✅ AI MODEL READY FOR DEPLOYMENT")
print("="*50)

def start_server():
    host = '127.0.0.1'
    port = 65500 # Keep the same as your Unity settings
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"\n🎧 Waiting for Unity connection...")
        conn, addr = server_socket.accept()
        print(f"✅ Unity connected! Entering [Director Mode]")
        print("------------------------------------------------")
        print("Enter commands in terminal to control the scene:")
        print(" [n]  -> Normal (All systems normal)")
        print(" [r]  -> Radiation (High radiation crisis)")
        print(" [g]  -> Gas (Toxic gas leak)")
        print(" [o]  -> Oxygen (Low oxygen emergency)")
        print(" [q]  -> Quit program")
        print("------------------------------------------------")

        # Default state
        current_data = {
            "radiation": 10, "toxic_gas": 0, "co2": 400, "oxygen": 21
        }

        while True:
            # Wait for user input
            cmd = input("Enter command (n/r/g/o): ").strip().lower()
            
            if cmd == 'q':
                break
            
            # Modify data based on command
            if cmd == 'n':
                print(">>> Switching to: All Systems Normal")
                current_data = {"radiation": 10, "toxic_gas": 0, "co2": 400, "oxygen": 21}
            elif cmd == 'r':
                print(">>> Switching to: ☢️ High Radiation Crisis")
                current_data = {"radiation": 500, "toxic_gas": 0, "co2": 400, "oxygen": 21}
            elif cmd == 'g':
                print(">>> Switching to: ☠️ Toxic Gas Leak")
                current_data = {"radiation": 10, "toxic_gas": 200, "co2": 400, "oxygen": 21}
            elif cmd == 'o':
                print(">>> Switching to: 💨 Severe Oxygen Shortage")
                current_data = {"radiation": 10, "toxic_gas": 0, "co2": 400, "oxygen": 15}
            else:
                print("Invalid command, state unchanged")
                continue # Skip sending, re-enter

            # Generate report
            status_report = {
                "sensor": current_data,
                "alert_message": "SYSTEM NORMAL",
                "action_plan": "MONITORING",
                "prediction_water": 0.0
            }

            # Decision logic (calling react.py)
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

            # Prediction logic (calling predict.py)
            # Predicting tomorrow's water consumption and displaying on Unity screen
            future = predictor.predict(100, 50, future_days=1)
            status_report["prediction_water"] = round(future[0], 1)

            # Send data
            json_str = json.dumps(status_report)
            conn.sendall((json_str + "\n").encode('utf-8'))
            print(f"Data sent to Unity")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()