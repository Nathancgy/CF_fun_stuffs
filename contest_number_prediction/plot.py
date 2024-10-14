import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')
plt.figure(figsize=(12, 6))
plt.scatter(df['Days'], df['Round'], alpha=0.5)

plt.xlabel('Days')
plt.ylabel('Contest Round')
plt.title('Days vs Contest Round')
plt.xlim(0, max(df['Days']))
plt.ylim(0, max(df['Round']))
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()