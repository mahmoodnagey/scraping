import re
import csv

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

data = read_file('clarks-summit-university-source.txt')
# Split by newline to iterate over each line
lines = data.split("\n")
courses = []

course = {}
for line in lines:
    # Find code: patterns like AR200, AS101–102, SC218/SC218L, and SED323
    code_match = re.search(r'^[A-Z]+[\d–/]+[\dA-Z]*', line)

    if code_match:
        if course:
            courses.append(course)
        course = {'code': code_match.group(0)}

        # Find title
        title_match = re.search(r'^[A-Z]+[\d–/]+[\dA-Z]*\s+(.*?)(?=\s+\d\s*(credit|credits|credit/semester))', line)
        if title_match:
            title = title_match.group(1).strip()
            # Remove "—2 semesters" or similar from the title
            title = re.sub(r'—\d+\s*semesters$', '', title).strip()
            course['title'] = title

        # Find credit
        credit_match = re.search(r'(\d)(?=\s*(credit|credits|credit/semester))', line)
        if credit_match:
            course['credit'] = credit_match.group(0)

        course['description'] = ''
    else:
        course['description'] += ' ' + line.strip()

# Add the last course
if course:
    courses.append(course)

# Write to CSV
filename = "clarks-summit-university.csv"
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['code', 'title', 'credit', 'description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for course in courses:
        writer.writerow(course)

print(f"Data exported to {filename}")
