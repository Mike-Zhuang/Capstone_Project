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
            
        # 检查有毒气体
        if sensor_data["toxic_gas"] > self.TOXIC_GAS_THRESHOLD:
            alerts.append("⚠️ 检测到有毒气体！切换内循环模式")
            
        # 检查CO2浓度
        if sensor_data["co2"] > self.CO2_THRESHOLD:
            alerts.append("⚠️ CO2浓度过高！启动碳过滤")
            
        # 检查氧气浓度
        if sensor_data["oxygen"] < 19.5:
            alerts.append("⚠️ 氧气浓度偏低！启动电解制氧")
            
        return alerts