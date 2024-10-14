import csv
from datetime import datetime

# Initialize variables
contests = []
current_contest_name = None
current_date = None
previous_line = None

def parse_date(s):
    """Parse the date string and return a datetime object or None."""
    try:
        return datetime.strptime(s, '%b/%d/%Y')
    except ValueError:
        return None

# Read the input file and process each line
with open('input.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        if line == 'Enter »':
            current_contest_name = previous_line  # The contest name is the previous line
        else:
            dt = parse_date(line)
            if dt:
                current_date = dt  # Found the date line
        if line == 'Final standings':
            if current_contest_name and current_date:
                month = current_date.strftime('%B')
                year = current_date.strftime('%Y')
                date = current_date.strftime('%d')  # Only the day number
                contests.append({'Name': current_contest_name, 'Month': month, 'Year': year, 'Date': date})
            # Reset for the next contest
            current_contest_name = None
            current_date = None
        previous_line = line  # Keep track of the previous line

# Write the extracted data to a CSV file
with open('666.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Month', 'Year', 'Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for contest in contests:
        writer.writerow(contest)
