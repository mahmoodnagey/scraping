import re
import csv

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

text = read_file('bacone-college-source.txt')

# Regular expression pattern to capture code, title, credit, and description
pattern = re.compile(r'(?P<code>[A-Z]+\s?(?:\d{4}|\d{4}/\s?\d{4}))\s+'
                     r'(?P<title>[^\n]+)\s+'
                     r'(?P<credit>\d) Hours\s+'
                     r'(?P<description>[\s\S]+?)(?=[A-Z]+\s?(?:\d{4}|\d{4}/\s?\d{4})|$)', re.M)

matches = list(pattern.finditer(text))

# Prepare data for CSV
csv_data = []
for match in matches:
    code = match.group('code')
    title = match.group('title')
    credit = match.group('credit')
    description = match.group('description').strip()
    csv_data.append([code, title, credit, description])

# Write to CSV
with open('bacone-college.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['code', 'title', 'credit', 'description'])  # headers
    writer.writerows(csv_data)

print("Data exported to courses.csv")
