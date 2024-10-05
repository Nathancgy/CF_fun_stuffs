import csv
from datetime import datetime
import re

# Initialize variables
contests = []
current_contest = {}
previous_line = None

def parse_date(s):
    """Parse the date string and return a datetime object or None."""
    try:
        return datetime.strptime(s.strip(), '%b/%d/%Y')
    except ValueError:
        return None

def parse_participants(s):
    """Parse the participants line starting with 'x' followed by a number."""
    match = re.match(r'x(\d+)', s.strip())
    if match:
        return int(match.group(1))
    else:
        return None

# Read the input file and process each line
with open('input.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    line = lines[i].strip()
    if not line:
        i += 1
        continue  # Skip empty lines

    if line == 'Enter »':
        # Start of a new contest
        current_contest = {
            'Name': lines[i - 1].strip() if i > 0 else None,
            'Date': None,
            'Participants': None
        }
        i += 1
        # Process the lines within the contest block
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            # Try to parse date
            dt = parse_date(line)
            if dt:
                current_contest['Date'] = dt
                i += 1
                continue

            # Check for 'Final standings' (not needed for this logic, but we can note it)
            if line == 'Final standings':
                i += 1
                continue

            # Try to parse participants
            participants = parse_participants(line)
            if participants is not None:
                current_contest['Participants'] = participants
                # Now we have all the information, we can process the contest
                if current_contest['Name'] and current_contest['Date']:
                    # Check if contest is Division 2
                    name_lower = current_contest['Name'].lower()
                    is_div2 = False
                    if ('div. 2' in name_lower or
                        'div. 1 + div. 2' in name_lower or
                        'div. 1+2' in name_lower or
                        'global' in name_lower or
                        ('educational' in name_lower and 'unrated' not in name_lower)):
                        is_div2 = True
                    if is_div2:
                        month = current_contest['Date'].strftime('%B')
                        year = current_contest['Date'].strftime('%Y')
                        contests.append({
                            'Name': current_contest['Name'],
                            'Month': month,
                            'Year': year,
                            'Participants': current_contest['Participants']
                        })
                # Reset current_contest for the next contest
                current_contest = {}
                i += 1
                break  # Exit the inner loop to start processing the next contest
            else:
                i += 1
    else:
        i += 1  # Move to the next line if not 'Enter »'

# Write the extracted data to a CSV file
with open('parti.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Month', 'Year', 'Participants']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for contest in contests:
        writer.writerow(contest)
