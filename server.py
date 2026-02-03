import socket
import json
import time
import threading  # Key import: multi-threading
from detect import AirQualityMonitor
from react import EmergencyDecisionTree
from predict import ResourcePredictor

# --- Global variables (for inter-thread communication) ---
current_command = 'n'  # Default: Normal
running = True

# Initialize modules
monitor = AirQualityMonitor()
decision_system = EmergencyDecisionTree()
predictor = ResourcePredictor()

# Pre-train the model (training a linear regression model to predict future water consumption)
print("\n" + "="*50)
print("🚀 UNDERGROUND SHELTER AI SYSTEM")
print("="*50)
X_train, y_water, y_food, y_oxygen = predictor.generate_training_data(num_people=50)
try:
    score = predictor.train_model(X_train, y_water)
    print(f"\n   🎯 Model Training Score (R²): {score:.4f}")
    if score >= 0.9:
        print("   ✓ Excellent model fit!")
    elif score >= 0.7:
        print("   ✓ Good model fit")
    else:
        print("   ⚠️ Warning: Low model fit, predictions may be unstable")
except Exception as e:
    print(f"   ❌ Model training failed: {e}")
    print("   Predictions will not work properly!")
print("\n" + "="*50)
print("✅ AI MODEL READY FOR DEPLOYMENT")
print("="*50)

# --- Keyboard listener thread function ---
def input_listener():
    """Background thread to handle keyboard input without blocking main loop"""
    global current_command, running
    print("   [Keyboard Listener Started] Type n, r, g, o, or q and press Enter...")
    while running:
        try:
            # This input() blocks, but only blocks the sub-thread, not the main thread!
            cmd = input().strip().lower()
            if cmd in ['n', 'r', 'g', 'o', 'q']:
                current_command = cmd
                if cmd == 'n':
                    print(">>> ✅ Command received: Normal Mode")
                elif cmd == 'r':
                    print(">>> ☢️ Command received: Radiation Crisis!")
                elif cmd == 'g':
                    print(">>> ☠️ Command received: Toxic Gas Leak!")
                elif cmd == 'o':
                    print(">>> 💨 Command received: Oxygen Shortage!")
                elif cmd == 'q':
                    print(">>> Shutting down...")
                    running = False
            else:
                print("   [Invalid Command] Use: n, r, g, o, or q")
        except EOFError:
            break

def start_server():
    global current_command, running
    
    host = '127.0.0.1'
    port = 65500  # Keep the same as your Unity settings
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"\n🎧 Waiting for Unity connection...")
        conn, addr = server_socket.accept()
        print(f"✅ Unity connected from {addr}! Entering [Director Mode]")
        
        # --- Start background thread for keyboard input ---
        t = threading.Thread(target=input_listener)
        t.daemon = True  # Daemon thread: exits when main program exits
        t.start()
        
        print("------------------------------------------------")
        print("🎬 LIVE DATA STREAM ACTIVE (auto-refresh every second)")
        print("   Commands: [n] Normal | [r] Radiation | [g] Gas | [o] Oxygen | [q] Quit")
        print("------------------------------------------------")

        # State variables
        current_data = {"radiation": 10, "toxic_gas": 0, "co2": 400, "oxygen": 21}
        current_emergency_level = 1

        while running:
            # --- A. Update state based on global command (set by keyboard thread) ---
            if current_command == 'n':
                current_data = {"radiation": 10, "toxic_gas": 0, "co2": 400, "oxygen": 21}
                current_emergency_level = 1  # Normal
            elif current_command == 'r':
                current_data = {"radiation": 500, "toxic_gas": 0, "co2": 400, "oxygen": 21}
                current_emergency_level = 3  # Critical!
            elif current_command == 'g':
                current_data = {"radiation": 10, "toxic_gas": 200, "co2": 400, "oxygen": 21}
                current_emergency_level = 2  # Warning
            elif current_command == 'o':
                current_data = {"radiation": 10, "toxic_gas": 0, "co2": 400, "oxygen": 15}
                current_emergency_level = 2  # Warning
            elif current_command == 'q':
                break

            # --- B. Prepare data packet ---
            status_report = {
                "sensor": current_data,
                "alert_message": "SYSTEM NORMAL",
                "action_plan": "MONITORING",
                "prediction_water": 0.0
            }

            # --- C. Execute React decision logic ---
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

            # --- D. Execute AI Prediction (KEY FIX!) ---
            try:
                # current_emergency_level is now dynamic!
                future = predictor.predict(
                    current_day=100,
                    num_people=50,
                    emergency_level=current_emergency_level,
                    future_days=1
                )
                pred_val = round(future[0], 1)
                status_report["prediction_water"] = pred_val
                
            except Exception as e:
                print(f"   [AI Error] Prediction failed: {e}")
                status_report["prediction_water"] = -1.0

            # --- E. Send data to Unity ---
            try:
                json_str = json.dumps(status_report)
                conn.sendall((json_str + "\n").encode('utf-8'))
                # Optional: uncomment to see live updates
                # print(f"   [LIVE] Level: {current_emergency_level} | Water: {pred_val} L/day")
            except BrokenPipeError:
                print("   Unity disconnected!")
                break
            
            # Auto-refresh rate: 1 second (no need to press Enter!)
            time.sleep(1.0)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()
        print("Server closed.")

if __name__ == "__main__":
    start_server()