import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for the plot
plt.style.use('default')
sns.set_palette("deep")

# Read the CSV file into a DataFrame
df = pd.read_csv('partidiv1.csv')

# Convert 'Year' to string before concatenation
df['Date'] = pd.to_datetime(df['Year'].astype(str) + ' ' + df['Month'], format='%Y %B')

# Group by Year-Month and calculate the average number of participants
df['Year-Month'] = df['Date'].dt.to_period('M')
monthly_avg = df.groupby('Year-Month')['Participants'].mean().reset_index()
monthly_avg['Date'] = monthly_avg['Year-Month'].dt.to_timestamp()

# Plot the data
plt.figure(figsize=(16, 8))
sns.lineplot(x='Date', y='Participants', data=monthly_avg, linewidth=2, marker='o')

# Customize the plot
plt.title('Average Number of Participants for Division 1 only Contests Per Month', fontsize=18, fontweight='bold')
plt.xlabel('Date', fontsize=14)
plt.ylabel('Average Number of Participants', fontsize=14)
plt.tick_params(axis='both', which='major', labelsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Add annotations for the highest and lowest points
max_point = monthly_avg.loc[monthly_avg['Participants'].idxmax()]
min_point = monthly_avg.loc[monthly_avg['Participants'].idxmin()]

plt.annotate(f'Max: {max_point["Participants"]:.0f}', 
             xy=(max_point['Date'], max_point['Participants']),
             xytext=(10, 10), textcoords='offset points',
             ha='left', va='bottom',
             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

plt.annotate(f'Min: {min_point["Participants"]:.0f}', 
             xy=(min_point['Date'], min_point['Participants']),
             xytext=(10, -10), textcoords='offset points',
             ha='left', va='top',
             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

# Add grid and adjust layout
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Show the plot
plt.show()
