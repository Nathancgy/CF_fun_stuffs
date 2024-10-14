import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from matplotlib.dates import DateFormatter, YearLocator, MonthLocator
from datetime import datetime, timedelta

df = pd.read_csv('data.csv')

start_date = datetime(2016, 1, 18)
df['Date'] = df['Days'].apply(lambda x: start_date + timedelta(days=x))
X = df['Round'].values.reshape(-1, 1)
y = df['Date']
model = LinearRegression()
model.fit(X, y.map(datetime.toordinal))

r_squared = r2_score(y.map(datetime.toordinal), model.predict(X))
mae = np.mean(np.abs(y.map(datetime.toordinal) - model.predict(X)))

def predict_date(round_number):
    predicted_ordinal = model.predict([[round_number]])[0]
    return datetime.fromordinal(int(predicted_ordinal))
plt.style.use('default')
sns.set_palette("deep")

# Create the figure and axis objects
fig, ax = plt.subplots(figsize=(14, 8))

# Plot the actual data points
sns.scatterplot(x='Date', y='Round', data=df, alpha=0.6, label='Actual Data', ax=ax)
X_plot = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_plot = [datetime.fromordinal(int(date)) for date in model.predict(X_plot)]
ax.plot(y_plot, X_plot, color='red', label='Linear Regression', linewidth=2)
future_rounds = [1000, 1100, 1200]
X_future = np.array([[df['Round'].min()], [max(df['Round'].max(), max(future_rounds))]])
y_future = [datetime.fromordinal(int(date)) for date in model.predict(X_future)]
ax.plot(y_future, X_future, color='red', linestyle='--', linewidth=2)
future_predictions = [predict_date(round_num) for round_num in future_rounds]
ax.scatter(future_predictions, future_rounds, color='green', s=100, label='Future Predictions', zorder=5)
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Contest Round', fontsize=12, fontweight='bold')
ax.set_title('Round vs Date', fontsize=16, fontweight='bold')
ax.set_ylim(df['Round'].min(), X_future[-1][0])
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
ax.xaxis.set_major_locator(YearLocator())
ax.xaxis.set_minor_locator(MonthLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y'))
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(fontsize=10, loc='lower right', bbox_to_anchor=(1, 0), ncol=1)
model_info = f"R² = {r_squared:.4f}\nMAE = {mae:.2f} days"
ax.text(0.05, 0.95, model_info, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

for round_num, pred_date in zip(future_rounds, future_predictions):
    ax.annotate(f'Round {round_num}: {pred_date.strftime("%Y-%m-%d")}', 
                xy=(pred_date, round_num), xytext=(10, 0),
                textcoords='offset points', ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

plt.tight_layout()
plt.show()

print("Model Coefficient (Slope):", model.coef_[0])
print("Model Intercept:", model.intercept_)
print(f"R-squared: {r_squared:.4f}")
print(f"Mean Absolute Error: {mae:.4f} days")

for round_num in future_rounds:
    predicted_date = predict_date(round_num)
    print(f"Predicted date for round {round_num}: {predicted_date.strftime('%Y-%m-%d')}")