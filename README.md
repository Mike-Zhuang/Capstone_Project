<p align="center">
  <img src="Gemini_Generated_Image_9evjsh9evjsh9evj.png" alt="Underground Shelter AI" width="400"/>
</p>

<h1 align="center">🏚️ Underground Shelter AI System</h1>
<h3 align="center">地下避难所智能管理系统</h3>

<p align="center">
  <strong>A Cyber-Physical System integrating Unity 3D Visualization with Python AI Backend</strong><br/>
  <strong>融合 Unity 3D 可视化与 Python AI 后端的信息物理系统</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Unity-6000.3.1f1-black?logo=unity&logoColor=white" alt="Unity"/>
  <img src="https://img.shields.io/badge/Scikit--Learn-1.3+-orange?logo=scikit-learn&logoColor=white" alt="Scikit-learn"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License"/>
  <img src="https://img.shields.io/badge/Model_Accuracy-R²_0.9978-brightgreen" alt="Model Accuracy"/>
</p>

<p align="center">
  <a href="#-features--功能特性">Features</a> •
  <a href="#-architecture--系统架构">Architecture</a> •
  <a href="#-quick-start--快速开始">Quick Start</a> •
  <a href="#-usage--使用指南">Usage</a> •
  <a href="#-api-reference--接口文档">API</a> •
  <a href="#-license--许可证">License</a>
</p>

---

## 📋 Overview | 项目概述

**Underground Shelter AI System** is a real-time **Cyber-Physical System (CPS)** designed to simulate intelligent management of a post-apocalyptic underground shelter. The system combines:

- 🎮 **Unity 3D Frontend**: Real-time physics simulation, particle effects, and interactive UI
- 🧠 **Python AI Backend**: Machine Learning predictions and Decision Tree-based emergency response
- 🔗 **TCP/IP Communication**: Low-latency bidirectional data streaming with JSON serialization

**地下避难所 AI 系统** 是一个实时 **信息物理系统 (CPS)**，用于模拟末日场景下地下避难所的智能管理。系统整合了：

- 🎮 **Unity 3D 前端**：实时物理仿真、粒子特效与交互式界面
- 🧠 **Python AI 后端**：机器学习预测与基于决策树的应急响应
- 🔗 **TCP/IP 通信**：低延迟双向数据流与 JSON 序列化

---

## ✨ Features | 功能特性

### 🔬 Sensor Simulation | 传感器模拟
| Sensor | Threshold | Response |
|--------|-----------|----------|
| ☢️ Radiation | > 100 μSv/h | Deploy Lead Shield |
| ☠️ Toxic Gas | > 50 ppm | Seal Ventilation |
| 💨 Oxygen | < 19.5% | Activate Electrolysis |
| 🌫️ CO₂ | > 5000 ppm | Activate Carbon Filter |

### 🤖 AI Prediction Engine | AI 预测引擎
- **Algorithm**: Polynomial Linear Regression (degree=2)
- **Features**: `[day, population, emergency_level, activity_level]`
- **Performance**: R² = **0.9978** | RMSE = 10.29 L/day
- **Cross-Validation**: 5-fold CV R² = 0.9960 (±0.0035)

### 🎯 Decision Tree System | 决策树系统
```
Emergency Detected
    ├── radiation_high → activate_shield
    │       ├── shield_active → monitor_levels
    │       └── shield_failed → evacuate_to_inner_chamber
    ├── toxic_gas → seal_ventilation
    │       ├── seal_successful → activate_filters
    │       └── seal_failed → deploy_emergency_masks
    └── power_failure → switch_to_backup
            ├── backup_online → diagnose_main
            └── backup_failed → activate_manual_generators
```

### 🎬 Real-time Visualization | 实时可视化
- Lead shield deployment animation (铅护盾动画)
- Toxic gas particle effects (毒气粒子特效)
- Oxygen bubble generation (氧气气泡生成)
- Emergency alarm light flashing (警报灯闪烁)
- Live dashboard with AI predictions (AI 预测仪表盘)

---

## 🏗️ Architecture | 系统架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        UNDERGROUND SHELTER AI SYSTEM                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────┐      TCP/IP       ┌──────────────────────┐│
│  │     UNITY 3D FRONTEND    │    Port 65500     │   PYTHON AI BACKEND  ││
│  │       (The Body)         │◄════════════════►│      (The Brain)     ││
│  ├──────────────────────────┤   JSON Protocol   ├──────────────────────┤│
│  │                          │                   │                      ││
│  │  ┌────────────────────┐  │   ─────────────►  │  ┌────────────────┐  ││
│  │  │  ShelterController │  │   User Commands   │  │    server.py   │  ││
│  │  │  - Button Events   │  │   (n/r/g/o/q)     │  │  - TCP Server  │  ││
│  │  │  - Animations      │  │                   │  │  - Main Loop   │  ││
│  │  └────────────────────┘  │                   │  └───────┬────────┘  ││
│  │           │              │                   │          │           ││
│  │           ▼              │                   │          ▼           ││
│  │  ┌────────────────────┐  │                   │  ┌────────────────┐  ││
│  │  │  PythonConnector   │  │   ◄─────────────  │  │   detect.py    │  ││
│  │  │  - TCP Client      │  │   Sensor Data +   │  │  - Thresholds  │  ││
│  │  │  - JSON Parser     │  │   AI Predictions  │  │  - Simulation  │  ││
│  │  └────────────────────┘  │                   │  └────────────────┘  ││
│  │           │              │                   │          │           ││
│  │           ▼              │                   │          ▼           ││
│  │  ┌────────────────────┐  │                   │  ┌────────────────┐  ││
│  │  │     GameData       │  │                   │  │    react.py    │  ││
│  │  │  - ServerData      │  │                   │  │  - Decision    │  ││
│  │  │  - SensorData      │  │                   │  │    Tree Logic  │  ││
│  │  └────────────────────┘  │                   │  └────────────────┘  ││
│  │                          │                   │          │           ││
│  │  ┌────────────────────┐  │                   │          ▼           ││
│  │  │   Visual Effects   │  │                   │  ┌────────────────┐  ││
│  │  │  - Particle System │  │                   │  │   predict.py   │  ││
│  │  │  - Lead Shield     │  │                   │  │  - ML Model    │  ││
│  │  │  - Alarm Lights    │  │                   │  │  - Polynomial  │  ││
│  │  └────────────────────┘  │                   │  │    Regression  │  ││
│  │                          │                   │  └────────────────┘  ││
│  └──────────────────────────┘                   └──────────────────────┘│
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start | 快速开始

### Prerequisites | 环境要求

| Requirement | Version | Description |
|-------------|---------|-------------|
| Python | 3.10+ | AI Backend Runtime |
| Unity | 6000.0+ (Unity 6) | 3D Visualization Engine |
| pip | Latest | Python Package Manager |

### Step 1: Clone Repository | 克隆仓库

```bash
git clone https://github.com/Mike-Zhuang/Capstone_Project.git
cd Capstone_Project
```

### Step 2: Setup Python Environment | 配置 Python 环境

```bash
# Create virtual environment | 创建虚拟环境
python -m venv venv

# Activate virtual environment | 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate

# Install dependencies | 安装依赖
pip install -r requirements.txt
```

### Step 3: Create `requirements.txt` (if not exists) | 创建依赖文件

```txt
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
```

Install with:
```bash
pip install numpy pandas scikit-learn matplotlib
```

### Step 4: Open Unity Project | 打开 Unity 项目

1. Launch **Unity Hub**
2. Click **"Add"** → Navigate to `Underground_Shelter/` folder
3. Open with **Unity 6 (6000.3.1f1 or compatible)**
4. Open scene: `Assets/Scenes/SampleScene.unity`

---

## 📖 Usage | 使用指南

### 🟢 Launch Sequence | 启动流程

#### Terminal 1: Start Python AI Server | 启动 Python AI 服务器

```bash
cd Capstone_Project
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
python server.py
```

**Expected Output | 预期输出:**
```
==================================================
🚀 UNDERGROUND SHELTER AI SYSTEM
==================================================

📊 GENERATING TRAINING DATA
==================================================
   Population: 50 people
   Simulation Period: 100 days
--------------------------------------------------
   Generating |████████████████████████████████████████| 100.0% Complete

   📈 Data Statistics:
      • Total samples: 100
      • Features: 4 (day, population, emergency, activity)
      • Water consumption: 359.7 ± 221.1 L/day

🤖 TRAINING PREDICTION MODEL
==================================================
   Model: Polynomial Linear Regression (degree=2)
   [1/4] Transforming features to polynomial...
   [2/4] Fitting linear regression model...
   [3/4] Calculating performance metrics...
   [4/4] Generating visualizations...

   🎯 Model Training Score (R²): 0.9978
   ✓ Excellent model fit!

==================================================
✅ AI MODEL READY FOR DEPLOYMENT
==================================================

🎧 Waiting for Unity connection...
```

#### Unity: Enter Play Mode | 进入播放模式

1. Press **▶️ Play** button in Unity Editor
2. Wait for connection confirmation in Python terminal:
```
✅ Unity connected from ('127.0.0.1', XXXXX)! Entering [Director Mode]
```

### 🎮 Control Commands | 控制命令

| Command | Mode | Effect (Unity) | Effect (Python) |
|---------|------|----------------|-----------------|
| `n` | Normal | Shield up, lights cyan | Level 1, low consumption |
| `r` | ☢️ Radiation | Shield down, alarm red | Level 3, high consumption |
| `g` | ☠️ Toxic Gas | Fan stops, gas particles | Level 2, seal vents |
| `o` | 💨 Low Oxygen | Bubbles active | Level 2, electrolysis on |
| `q` | Quit | - | Server shutdown |

**Control Methods | 控制方式:**
- **Terminal**: Type `n`, `r`, `g`, `o`, or `q` and press Enter
- **Unity UI**: Click the on-screen buttons (Radiation / Gas / Oxygen / Reset)

### 📊 Output Data Format | 输出数据格式

The Python server sends JSON packets to Unity every second:

```json
{
  "sensor": {
    "radiation": 500.0,
    "toxic_gas": 0.0,
    "co2": 400.0,
    "oxygen": 21.0
  },
  "alert_message": "WARNING: HIGH RADIATION",
  "action_plan": "ACT: activate_shield",
  "prediction_water": 750.5
}
```

| Field | Type | Description |
|-------|------|-------------|
| `sensor` | Object | Current simulated sensor readings |
| `alert_message` | String | Human-readable alert status |
| `action_plan` | String | Recommended immediate action |
| `prediction_water` | Float | AI-predicted water usage (L/day) |

---

## 📁 Project Structure | 项目结构

```
Capstone_Project/
│
├── 🐍 Python Backend
│   ├── server.py          # TCP server & main control loop | 主服务器与控制循环
│   ├── detect.py          # Sensor simulation & thresholds | 传感器模拟与阈值检测
│   ├── react.py           # Decision tree logic | 决策树逻辑
│   ├── predict.py         # ML model (Polynomial Regression) | 机器学习模型
│   └── requirements.txt   # Python dependencies | Python 依赖
│
├── 🎮 Unity Frontend (Underground_Shelter/)
│   ├── Assets/
│   │   ├── PythonConnector.cs   # TCP client & JSON parser | TCP 客户端
│   │   ├── ShelterController.cs # Animation & UI logic | 动画与界面逻辑
│   │   ├── GameData.cs          # Data structures | 数据结构定义
│   │   └── Scenes/              # Unity scenes | Unity 场景
│   ├── ProjectSettings/         # Unity project config | 项目配置
│   └── Packages/                # Unity packages | Unity 包
│
├── 📊 Output
│   └── training_output/
│       ├── training_summary.txt      # Model metrics | 模型指标
│       └── training_visualization.png # Learning curves | 学习曲线
│
└── 📄 Documentation
    └── README.md                # This file | 本文件
```

---

## 🔌 API Reference | 接口文档

### Python Modules | Python 模块

#### `detect.py` - AirQualityMonitor
```python
monitor = AirQualityMonitor()
data = monitor.simulate_sensor_data()  # Returns dict with radiation, toxic_gas, co2, oxygen
alerts = monitor.check_air_quality(data)  # Returns list of alert strings
```

#### `react.py` - EmergencyDecisionTree
```python
decision_system = EmergencyDecisionTree()
response = decision_system.make_decision(
    emergency_type="radiation_high",  # radiation_high | toxic_gas | power_failure
    severity="high"                   # low | medium | high
)
# Returns: { emergency, severity, immediate_action, sub_actions, priority, resources_needed }
```

#### `predict.py` - ResourcePredictor
```python
predictor = ResourcePredictor()

# Generate training data
X, y_water, y_food, y_oxygen = predictor.generate_training_data(num_people=50, days=100)

# Train model
r2_score = predictor.train_model(X, y_water)

# Predict future consumption
predictions = predictor.predict(
    current_day=100,
    num_people=50,
    emergency_level=3,    # 1=Normal, 2=Warning, 3=Critical
    activity_level=1.0,
    future_days=7
)
```

### Unity Classes | Unity 类

#### `PythonConnector.cs`
```csharp
// Access latest data from Python
ServerData data = connector.latestData;
float waterUsage = data.prediction_water;
string alert = data.alert_message;

// Send command to Python
connector.SendCommand("r");  // Trigger radiation mode
```

#### `ShelterController.cs`
```csharp
// Button event handlers (auto-bound in Start())
void TriggerRadiation();  // Sets mode to "r", lowers shield
void TriggerGas();        // Sets mode to "g", shows gas particles
void TriggerOxygen();     // Sets mode to "o", activates bubbles
void ResetSystem();       // Sets mode to "n", returns to normal
```

---

## 📈 Performance Metrics | 性能指标

### AI Model Performance | AI 模型性能

| Metric | Value | Interpretation |
|--------|-------|----------------|
| R² Score | 0.9978 | 99.78% variance explained ✅ |
| RMSE | 10.29 L/day | Average prediction error |
| MAE | 7.99 L/day | Mean absolute error |
| CV R² | 0.9960 ± 0.0035 | Robust cross-validation |

### System Performance | 系统性能

| Metric | Value |
|--------|-------|
| Communication Latency | < 10ms |
| Data Refresh Rate | 1 Hz (1 second) |
| Unity Frame Rate | 60+ FPS |
| TCP Port | 65500 |

---

## 🛠️ Troubleshooting | 故障排除

| Issue | Solution |
|-------|----------|
| `Connection refused` | Ensure `python server.py` is running BEFORE Unity Play |
| `Port already in use` | Kill existing Python process: `lsof -i :65500` then `kill -9 PID` |
| Unity not receiving data | Check Console for `✅ Successfully connected` message |
| Model training failed | Ensure scikit-learn is installed: `pip install scikit-learn` |
| Matplotlib crash (macOS) | Already fixed with `matplotlib.use('Agg')` in code |

---

## 🤝 Contributing | 贡献指南

1. Fork the repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📜 License | 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目基于 MIT 许可证开源 - 详见 [LICENSE](LICENSE) 文件。

---

## 👨‍💻 Author | 作者

**Chengbo Zhuang (庄程博)**

- 🎓 Tongji University, Shanghai, China
- 📧 Contact via GitHub Issues

---

<p align="center">
  <strong>🏚️ Survive. Adapt. Predict. 🧠</strong><br/>
  <em>Built with ❤️ for STEM Capstone Project 2026</em>
</p>
