import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import sys
import time
import os

class ResourcePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.poly = PolynomialFeatures(degree=2)
        self.training_history = {}
        
    def _print_progress_bar(self, iteration, total, prefix='', suffix='', length=40, fill='█'):
        """Print a progress bar to the terminal"""
        percent = f"{100 * (iteration / float(total)):.1f}"
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '░' * (length - filled_length)
        sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
        sys.stdout.flush()
        if iteration == total:
            print()
    
    def generate_training_data(self, num_people, days=100, verbose=True):
        """Generate simulated training data with progress visualization"""
        np.random.seed(42)
        
        X = []
        y_water = []
        y_food = []
        y_oxygen = []
        
        if verbose:
            print("\n" + "="*50)
            print("📊 GENERATING TRAINING DATA")
            print("="*50)
            print(f"   Population: {num_people} people")
            print(f"   Simulation Period: {days} days")
            print("-"*50)
        
        for day in range(days):
            # Features: day count, population, emergency level (1-3), activity level (0.5-1.5)
            emergency_level = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
            activity_level = np.random.uniform(0.5, 1.5)
            
            features = [day, num_people, emergency_level, activity_level]
            X.append(features)
            
            # Calculate consumption (with random noise)
            water = num_people * 5 * emergency_level * activity_level + np.random.normal(0, 10)
            food = num_people * 2000 * emergency_level * activity_level + np.random.normal(0, 500)
            oxygen = num_people * 550 * emergency_level * activity_level + np.random.normal(0, 50)
            
            y_water.append(water)
            y_food.append(food)
            y_oxygen.append(oxygen)
            
            if verbose:
                self._print_progress_bar(day + 1, days, prefix='   Generating', suffix='Complete')
                time.sleep(0.01)  # Small delay for visual effect
        
        # Store statistics
        self.training_history['data_stats'] = {
            'samples': days,
            'features': 4,
            'water_mean': np.mean(y_water),
            'water_std': np.std(y_water),
            'food_mean': np.mean(y_food),
            'oxygen_mean': np.mean(y_oxygen)
        }
        
        if verbose:
            print("\n   📈 Data Statistics:")
            print(f"      • Total samples: {days}")
            print(f"      • Features: 4 (day, population, emergency, activity)")
            print(f"      • Water consumption: {np.mean(y_water):.1f} ± {np.std(y_water):.1f} L/day")
            print(f"      • Food consumption: {np.mean(y_food):.0f} ± {np.std(y_food):.0f} kcal/day")
            print(f"      • Oxygen consumption: {np.mean(y_oxygen):.0f} ± {np.std(y_oxygen):.0f} L/day")
        
        return np.array(X), np.array(y_water), np.array(y_food), np.array(y_oxygen)
    
    def train_model(self, X, y, verbose=True, save_plots=True):
        """Train prediction model with visualization"""
        if verbose:
            print("\n" + "="*50)
            print("🤖 TRAINING PREDICTION MODEL")
            print("="*50)
            print("   Model: Polynomial Linear Regression (degree=2)")
            print("-"*50)
        
        # Step 1: Feature transformation
        if verbose:
            print("   [1/4] Transforming features to polynomial...")
            self._print_progress_bar(1, 4, prefix='   Progress', suffix='')
            time.sleep(0.3)
        X_poly = self.poly.fit_transform(X)
        
        # Step 2: Model fitting
        if verbose:
            print("   [2/4] Fitting linear regression model...")
            self._print_progress_bar(2, 4, prefix='   Progress', suffix='')
            time.sleep(0.3)
        self.model.fit(X_poly, y)
        
        # Step 3: Calculate metrics
        if verbose:
            print("   [3/4] Calculating performance metrics...")
            self._print_progress_bar(3, 4, prefix='   Progress', suffix='')
            time.sleep(0.3)
        
        r2_score = self.model.score(X_poly, y)
        y_pred = self.model.predict(X_poly)
        mse = np.mean((y - y_pred) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y - y_pred))
        
        # Cross-validation
        cv_scores = cross_val_score(LinearRegression(), X_poly, y, cv=5, scoring='r2')
        
        # Store training history
        self.training_history['metrics'] = {
            'r2_score': r2_score,
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
        self.training_history['predictions'] = y_pred
        self.training_history['actual'] = y
        
        # Step 4: Generate visualizations
        if verbose:
            print("   [4/4] Generating visualizations...")
            self._print_progress_bar(4, 4, prefix='   Progress', suffix='')
            time.sleep(0.2)
        
        if save_plots:
            self._generate_training_plots(X, y, y_pred)
        
        if verbose:
            print("\n   📊 Model Performance Metrics:")
            print(f"      • R² Score: {r2_score:.4f} {'✓ Excellent' if r2_score > 0.9 else '✓ Good' if r2_score > 0.7 else '⚠ Needs improvement'}")
            print(f"      • RMSE: {rmse:.2f} L/day")
            print(f"      • MAE: {mae:.2f} L/day")
            print(f"      • Cross-validation R²: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
            print("\n   📁 Visualization saved to: ./training_output/")
        
        return r2_score
    
    def _generate_training_plots(self, X, y, y_pred):
        """Generate and save training visualization plots"""
        from sklearn.model_selection import learning_curve
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), 'training_output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid') if 'seaborn-v0_8-darkgrid' in plt.style.available else None
        
        # Create figure with 6 subplots (3x2)
        fig, axes = plt.subplots(3, 2, figsize=(14, 15))
        fig.suptitle('AI Resource Consumption Model - Training Report', fontsize=16, fontweight='bold', y=0.98)
        
        # Plot 1: Actual vs Predicted
        ax1 = axes[0, 0]
        ax1.scatter(y, y_pred, alpha=0.6, edgecolors='black', linewidth=0.5, c='#3498db')
        ax1.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2, label='Perfect Prediction')
        ax1.set_xlabel('Actual Water Consumption (L/day)')
        ax1.set_ylabel('Predicted Water Consumption (L/day)')
        ax1.set_title('1. Actual vs Predicted Values')
        ax1.legend()
        r2 = self.training_history['metrics']['r2_score']
        ax1.annotate(f'R² = {r2:.4f}', xy=(0.05, 0.95), xycoords='axes fraction', 
                    fontsize=10, fontweight='bold', va='top',
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        
        # Plot 2: Learning Curve (Loss Curve equivalent for Linear Regression)
        ax2 = axes[0, 1]
        X_poly = self.poly.transform(X)
        train_sizes = np.linspace(0.1, 1.0, 10)
        train_sizes_abs, train_scores, val_scores = learning_curve(
            LinearRegression(), X_poly, y, 
            train_sizes=train_sizes, cv=5, scoring='neg_mean_squared_error'
        )
        train_mse = -train_scores.mean(axis=1)
        val_mse = -val_scores.mean(axis=1)
        ax2.plot(train_sizes_abs, train_mse, 'o-', color='#3498db', label='Training Loss', linewidth=2)
        ax2.plot(train_sizes_abs, val_mse, 'o-', color='#e74c3c', label='Validation Loss', linewidth=2)
        ax2.fill_between(train_sizes_abs, train_mse - (-train_scores).std(axis=1), 
                        train_mse + (-train_scores).std(axis=1), alpha=0.2, color='#3498db')
        ax2.fill_between(train_sizes_abs, val_mse - (-val_scores).std(axis=1), 
                        val_mse + (-val_scores).std(axis=1), alpha=0.2, color='#e74c3c')
        ax2.set_xlabel('Training Set Size')
        ax2.set_ylabel('Mean Squared Error (Loss)')
        ax2.set_title('2. Learning Curve (MSE Loss)')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Residuals distribution
        ax3 = axes[1, 0]
        residuals = y - y_pred
        ax3.hist(residuals, bins=20, color='#2ecc71', edgecolor='black', alpha=0.7)
        ax3.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Zero Error')
        ax3.set_xlabel('Residual (Actual - Predicted)')
        ax3.set_ylabel('Frequency')
        ax3.set_title('3. Residuals Distribution')
        ax3.annotate(f'Mean: {np.mean(residuals):.2f}\nStd: {np.std(residuals):.2f}', 
                    xy=(0.95, 0.95), xycoords='axes fraction', ha='right', va='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax3.legend()
        
        # Plot 4: Consumption by Emergency Level
        ax4 = axes[1, 1]
        emergency_levels = X[:, 2]
        for level in [1, 2, 3]:
            mask = emergency_levels == level
            if np.any(mask):
                level_labels = ['Normal', 'Warning', 'Critical']
                colors = ['#2ecc71', '#f39c12', '#e74c3c']
                ax4.scatter(y[mask], y_pred[mask], alpha=0.7, label=f'Level {level}: {level_labels[level-1]}',
                          color=colors[level-1], edgecolors='black', linewidth=0.3, s=60)
        ax4.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=1.5, alpha=0.5)
        ax4.set_xlabel('Actual Consumption (L/day)')
        ax4.set_ylabel('Predicted Consumption (L/day)')
        ax4.set_title('4. Prediction Accuracy by Emergency Level')
        ax4.legend()
        
        # Plot 5: Consumption over time
        ax5 = axes[2, 0]
        days = X[:, 0]
        ax5.plot(days, y, 'b-', alpha=0.7, label='Actual', linewidth=1.5)
        ax5.plot(days, y_pred, 'r--', alpha=0.7, label='Predicted', linewidth=1.5)
        ax5.fill_between(days, y, y_pred, alpha=0.3, color='gray', label='Error Region')
        ax5.set_xlabel('Day')
        ax5.set_ylabel('Water Consumption (L/day)')
        ax5.set_title('5. Water Consumption Over Time')
        ax5.legend()
        
        # Plot 6: Cross-Validation Scores
        ax6 = axes[2, 1]
        cv_scores = cross_val_score(LinearRegression(), X_poly, y, cv=5, scoring='r2')
        bars = ax6.bar(range(1, 6), cv_scores, color=['#3498db', '#2ecc71', '#9b59b6', '#f39c12', '#e74c3c'],
                      edgecolor='black', alpha=0.8)
        ax6.axhline(y=cv_scores.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {cv_scores.mean():.4f}')
        ax6.fill_between([0.5, 5.5], cv_scores.mean() - cv_scores.std(), cv_scores.mean() + cv_scores.std(),
                        alpha=0.2, color='red', label=f'±1 Std: {cv_scores.std():.4f}')
        ax6.set_xlabel('Fold Number')
        ax6.set_ylabel('R² Score')
        ax6.set_title('6. 5-Fold Cross-Validation Results')
        ax6.set_xticks(range(1, 6))
        ax6.set_ylim([min(0.8, cv_scores.min() - 0.05), 1.0])
        ax6.legend(loc='lower right')
        for i, v in enumerate(cv_scores):
            ax6.text(i + 1, v + 0.005, f'{v:.3f}', ha='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'training_report.png'), dpi=150, bbox_inches='tight')
        plt.close()
        
        # Generate a summary text file
        self._generate_summary_report(output_dir)
    
    def _generate_summary_report(self, output_dir):
        """Generate a text summary of the training"""
        report_path = os.path.join(output_dir, 'training_summary.txt')
        with open(report_path, 'w') as f:
            f.write("="*60 + "\n")
            f.write("    AI RESOURCE CONSUMPTION MODEL - TRAINING SUMMARY\n")
            f.write("="*60 + "\n\n")
            
            f.write("DATA STATISTICS:\n")
            f.write("-"*40 + "\n")
            stats = self.training_history.get('data_stats', {})
            f.write(f"  Total Samples: {stats.get('samples', 'N/A')}\n")
            f.write(f"  Features: {stats.get('features', 'N/A')}\n")
            f.write(f"  Water Mean: {stats.get('water_mean', 0):.2f} L/day\n")
            f.write(f"  Water Std: {stats.get('water_std', 0):.2f} L/day\n\n")
            
            f.write("MODEL PERFORMANCE:\n")
            f.write("-"*40 + "\n")
            metrics = self.training_history.get('metrics', {})
            f.write(f"  R² Score: {metrics.get('r2_score', 0):.4f}\n")
            f.write(f"  RMSE: {metrics.get('rmse', 0):.2f} L/day\n")
            f.write(f"  MAE: {metrics.get('mae', 0):.2f} L/day\n")
            f.write(f"  Cross-validation R²: {metrics.get('cv_mean', 0):.4f} (±{metrics.get('cv_std', 0):.4f})\n\n")
            
            f.write("MODEL CONFIGURATION:\n")
            f.write("-"*40 + "\n")
            f.write("  Algorithm: Polynomial Linear Regression\n")
            f.write("  Polynomial Degree: 2\n")
            f.write("  Features: [day, population, emergency_level, activity_level]\n\n")
            
            f.write("="*60 + "\n")
            f.write("  Generated by Underground Shelter AI System\n")
            f.write("="*60 + "\n")
    
    def predict(self, current_day, num_people, emergency_level=1, activity_level=1.0, future_days=30):
        """Predict future consumption"""
        predictions = []
        
        for i in range(future_days):
            features = [[current_day + i, num_people, emergency_level, activity_level]]
            features_poly = self.poly.transform(features)
            prediction = self.model.predict(features_poly)[0]
            predictions.append(max(0, prediction))  # Ensure non-negative
        
        return predictions