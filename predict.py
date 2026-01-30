import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# 注意：我去掉了 matplotlib 的引用，因为服务器端我们不需要画图，只需要数字
# 如果你需要画图，在 Unity 墙上的屏幕直接贴图片即可

class ResourcePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.poly = PolynomialFeatures(degree=2)
        
    def generate_training_data(self, num_people, days=100):
        """生成模拟训练数据"""
        np.random.seed(42)
        
        X = []
        y_water = []
        y_food = []
        y_oxygen = []
        
        for day in range(days):
            # 特征：天数、人数、紧急程度(1-3)、活动水平(0.5-1.5)
            emergency_level = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
            activity_level = np.random.uniform(0.5, 1.5)
            
            features = [day, num_people, emergency_level, activity_level]
            X.append(features)
            
            # 计算消耗（加入随机噪声）
            water = num_people * 5 * emergency_level * activity_level + np.random.normal(0, 10)
            food = num_people * 2000 * emergency_level * activity_level + np.random.normal(0, 500)
            oxygen = num_people * 550 * emergency_level * activity_level + np.random.normal(0, 50)
            
            y_water.append(water)
            y_food.append(food)
            y_oxygen.append(oxygen)
        
        return np.array(X), np.array(y_water), np.array(y_food), np.array(y_oxygen)
    
    def train_model(self, X, y):
        """训练预测模型"""
        X_poly = self.poly.fit_transform(X)
        self.model.fit(X_poly, y)
        return self.model.score(X_poly, y)  # 返回R²分数
    
    def predict(self, current_day, num_people, emergency_level=1, activity_level=1.0, future_days=30):
        """预测未来消耗"""
        predictions = []
        
        for i in range(future_days):
            features = [[current_day + i, num_people, emergency_level, activity_level]]
            features_poly = self.poly.transform(features)
            prediction = self.model.predict(features_poly)[0]
            predictions.append(max(0, prediction))  # 确保非负
        
        return predictions