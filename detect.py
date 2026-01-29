import time
import random

class AirQualityMonitor:
    def __init__(self):
        # 传感器阈值
        self.RADIATION_THRESHOLD = 100  # uSv/h
        self.TOXIC_GAS_THRESHOLD = 50   # ppm
        self.CO2_THRESHOLD = 5000       # ppm
        
        # 系统状态
        self.air_mode = "normal"  # normal / internal_circulation / emergency
        self.filter_status = "active"
        
    def simulate_sensor_data(self):
        """模拟传感器数据"""
        return {
            "radiation": random.uniform(10, 150),
            "toxic_gas": random.uniform(10, 80),
            "co2": random.uniform(3000, 7000),
            "oxygen": random.uniform(18, 23)
        }
    
    def check_air_quality(self, sensor_data):
        """检查空气质量并触发相应响应"""
        alerts = []
        
        # 检查辐射
        if sensor_data["radiation"] > self.RADIATION_THRESHOLD:
            alerts.append("⚠️ 高辐射警报！启动铅屏蔽层")
            self.activate_radiation_shield()
            
        # 检查有毒气体
        if sensor_data["toxic_gas"] > self.TOXIC_GAS_THRESHOLD:
            alerts.append("⚠️ 检测到有毒气体！切换内循环模式")
            self.switch_to_internal_circulation()
            
        # 检查CO2浓度
        if sensor_data["co2"] > self.CO2_THRESHOLD:
            alerts.append("⚠️ CO2浓度过高！启动碳过滤")
            self.activate_co2_scrubber()
            
        # 检查氧气浓度
        if sensor_data["oxygen"] < 19.5:
            alerts.append("⚠️ 氧气浓度偏低！启动电解制氧")
            self.activate_oxygen_generator()
            
        return alerts
    
    def activate_radiation_shield(self):
        """激活辐射屏蔽"""
        self.air_mode = "emergency"
        print("🛡️ 铅屏蔽层已启动，辐射防护激活")
        
    def switch_to_internal_circulation(self):
        """切换到内循环模式"""
        self.air_mode = "internal_circulation"
        print("♻️ 切换到内循环空气模式")
        
    def activate_co2_scrubber(self):
        """激活二氧化碳吸附系统"""
        print("🌫️ CO2吸附系统启动中...")
        
    def activate_oxygen_generator(self):
        """激活制氧系统"""
        print("💨 电解水制氧系统启动")

# 测试代码
monitor = AirQualityMonitor()

print("=== 避难所空气质量监控系统 ===")
print("系统启动...")

for i in range(10):
    print(f"\n--- 第{i+1}次检测 ---")
    data = monitor.simulate_sensor_data()
    print(f"传感器读数: {data}")
    
    alerts = monitor.check_air_quality(data)
    if alerts:
        for alert in alerts:
            print(alert)
    else:
        print("✅ 空气质量正常")
    
    time.sleep(1)