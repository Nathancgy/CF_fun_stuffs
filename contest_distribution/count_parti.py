import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

# Step 1: Create a list of months from January 2012 to October 2024
def generate_month_list(start_year, start_month, end_year, end_month):
    month_list = []
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)
    while start_date <= end_date:
        month_str = start_date.strftime('%Y %b')
        month_list.append({'Month': month_str, 'Divisions': []})
        # Move to the next month
        next_month = start_date.month % 12 + 1
        next_year = start_date.year + (start_date.month // 12)
        start_date = datetime(next_year, next_month, 1)
    return month_list

# Generate the month list
months = generate_month_list(2012, 1, 2024, 10)
month_dict = {month['Month']: month for month in months}  # For quick access

# Step 2: Read the CSV file and process each contest
with open('output.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        contest_name = row['Name']
        month = row['Month']
        year = row['Year']
        month_year = f"{year} {month[:3]}"  # Format month as 'YYYY Mon'
        
        # Initialize divisions list
        divisions = []
        contest_name_lower = contest_name.lower()
        
        if 'div. 1 + div. 2' in contest_name_lower or 'global' in contest_name_lower:
            divisions.extend([1, 2])
        elif 'div. 1' in contest_name_lower:
            divisions.append(1)
        elif 'div. 2' in contest_name_lower:
            divisions.append(2)
        elif 'div. 3' in contest_name_lower:
            divisions.append(3)
        elif 'div. 4' in contest_name_lower:
            divisions.append(4)
        elif 'educational' in contest_name_lower and 'unrated' not in contest_name_lower:
            divisions.append(2)
        else:
            continue  # Unrated or doesn't specify divisions
        
        # Step 3: Append divisions to the corresponding month
        if month_year in month_dict:
            month_dict[month_year]['Divisions'].extend(divisions)

# Process the data to group by year and month
yearly_data = {}
for month_data in months:
    month_str = month_data['Month']
    month_datetime = datetime.strptime(month_str, '%Y %b')
    year = month_datetime.year
    month_num = month_datetime.month  # 1 to 12
    divisions = month_data['Divisions']
    counts = defaultdict(int)
    for div in divisions:
        counts[f'Div {div}'] += 1

    if year not in yearly_data:
        # Initialize data structure for the year
        yearly_data[year] = {
            'Div 1': [0]*12,
            'Div 2': [0]*12,
            'Div 3': [0]*12,
            'Div 4': [0]*12
        }
    # Update counts for the month (month_num - 1 because list index starts from 0)
    for div in ['Div 1', 'Div 2', 'Div 3', 'Div 4']:
        yearly_data[year][div][month_num - 1] = counts[div]

# Now, plot the data
# Set up the plot
fig, ax = plt.subplots(figsize=(15, 7))

# Define colors for divisions
div_colors = {
    'Div 1': '#4C72B0',
    'Div 2': '#55A868',
    'Div 3': '#C44E52',
    'Div 4': '#8172B2'
}

# Prepare data for plotting
positions = []
labels = []
bar_width = 0.6
year_positions = {}
current_pos = 0

for year in sorted(yearly_data.keys()):
    year_positions[year] = []
    for month in range(12):
        positions.append(current_pos)
        # Only label odd months
        if (month + 1) % 2 != 0:
            labels.append(str(month + 1))
        else:
            labels.append('')  # Leave even months unlabeled
        year_positions[year].append(current_pos)
        current_pos += 1  # Increment position
    current_pos += 2  # Add extra space between years

# Plot the stacked bars
div_bottoms = [0]*len(positions)
for div in ['Div 1']:
    div_values = []
    for year in sorted(yearly_data.keys()):
        div_values.extend(yearly_data[year][div])
    ax.bar(positions, div_values, bottom=div_bottoms, width=bar_width, label=div, color=div_colors[div])
    # Update bottoms for stacking
    div_bottoms = [sum(x) for x in zip(div_bottoms, div_values)]

# Customize x-axis labels
ax.set_xticks(positions)
ax.set_xticklabels(labels)

# Add year annotations
for year in sorted(yearly_data.keys()):
    positions_in_year = year_positions[year]
    if not positions_in_year:
        continue
    year_start = positions_in_year[0]
    year_end = positions_in_year[-1]
    year_mid = (year_start + year_end) / 2
    ax.text(year_mid, ax.get_ylim()[1], str(year), ha='center', va='bottom', fontsize=10)
    # Add a vertical line to separate years
    ax.axvline(x=year_end + 1, color='gray', linestyle='--', linewidth=0.5)

# Adjust the plot limits
max_value = max(div_bottoms)
ax.set_ylim(0, max_value + 1)  # Set the upper limit to just above the highest bar

# Add labels and title
ax.set_xlabel('Month')
ax.set_ylabel('Number of Rated Contests')
ax.set_title('Monthly Distribution of Codeforces Division 1 Contests (2012-2024)')

# Add legend
ax.legend()

# Tight layout for better spacing
plt.tight_layout()

# Show the plot
plt.show()
