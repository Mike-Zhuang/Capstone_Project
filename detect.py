import time
import random

class AirQualityMonitor:
    def __init__(self):
        # Sensor thresholds
        self.RADIATION_THRESHOLD = 100  # uSv/h
        self.TOXIC_GAS_THRESHOLD = 50   # ppm
        self.CO2_THRESHOLD = 5000       # ppm
        
        # System status
        self.air_mode = "normal"  # normal / internal_circulation / emergency
        self.filter_status = "active"
        
    def simulate_sensor_data(self):
        """Simulate sensor data"""
        return {
            "radiation": random.uniform(10, 150),
            "toxic_gas": random.uniform(10, 80),
            "co2": random.uniform(3000, 7000),
            "oxygen": random.uniform(18, 23)
        }
    
    def check_air_quality(self, sensor_data):
        """Check air quality and trigger corresponding responses"""
        alerts = []
        
        # Check radiation
        if sensor_data["radiation"] > self.RADIATION_THRESHOLD:
            alerts.append("⚠️ High radiation alert! Activating lead shielding")
            
        # Check toxic gas
        if sensor_data["toxic_gas"] > self.TOXIC_GAS_THRESHOLD:
            alerts.append("⚠️ Toxic gas detected! Switching to internal circulation mode")
            
        # Check CO2 concentration
        if sensor_data["co2"] > self.CO2_THRESHOLD:
            alerts.append("⚠️ CO2 level too high! Activating carbon filter")
            
        # Check oxygen concentration
        if sensor_data["oxygen"] < 19.5:
            alerts.append("⚠️ Oxygen level low! Activating electrolysis oxygen generator")
            
        return alerts