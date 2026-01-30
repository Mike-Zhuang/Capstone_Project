import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

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
    
    def plot_predictions(self, actual, predicted, resource_name="资源"):
        """绘制预测图表"""
        plt.figure(figsize=(10, 6))
        days = range(len(actual))
        
        plt.plot(days, actual, 'b-', label='实际消耗', linewidth=2)
        plt.plot(days, predicted, 'r--', label='预测消耗', linewidth=2)
        plt.fill_between(days, actual, predicted, alpha=0.2, color='gray')
        
        plt.xlabel('天数', fontsize=12)
        plt.ylabel(f'{resource_name}消耗量', fontsize=12)
        plt.title(f'{resource_name}消耗预测 vs 实际', fontsize=14)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 添加统计数据
        mae = np.mean(np.abs(np.array(actual) - np.array(predicted)))
        plt.text(0.02, 0.98, f'平均绝对误差: {mae:.2f}', 
                 transform=plt.gca().transAxes,
                 verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.show()

# 使用示例
predictor = ResourcePredictor()

# 生成数据
X, y_water, y_food, y_oxygen = predictor.generate_training_data(num_people=50, days=100)

# 训练水消耗模型
print("训练水消耗预测模型...")
score_water = predictor.train_model(X, y_water)
print(f"模型R²分数: {score_water:.4f}")

# 进行预测
future_predictions = predictor.predict(
    current_day=100, 
    num_people=50, 
    emergency_level=2, 
    activity_level=1.2,
    future_days=30
)

print(f"\n未来30天水消耗预测:")
for day, pred in enumerate(future_predictions, 1):
    print(f"第{day:2d}天: {pred:7.1f}升")

# 绘制对比图（使用最后30天数据作为验证）
actual_last_30 = y_water[-30:]
predicted_last_30 = predictor.predict(70, 50, 1, 1.0, 30)
predictor.plot_predictions(actual_last_30, predicted_last_30, "水")

