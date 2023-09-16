import re
import csv

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

text = read_file('wharton-county-junior-college-source.txt')

# Regular expression pattern to capture code, credit, title, and description
pattern = re.compile(r'(?P<code>[A-Z]+\s+\d+)\s+(\d+:\d+:\d+)\n(?P<title>[^\n]+)\n(.*?)(?=(?:[A-Z]+\s+\d+|$))', re.DOTALL)

matches = list(pattern.finditer(text))

# Prepare data for CSV
csv_data = []
for match in matches:
    code = match.group('code')
    credit = match.group(2).split(':')[0]
    title = match.group('title')
    description = match.group(4).strip()
    csv_data.append([code, title, credit, description])

# Write to CSV
with open('wharton-county-junior-college.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['code', 'title', 'credit', 'description'])  # headers
    writer.writerows(csv_data)

print("Data exported to wharton-county-junior-college.csv")
