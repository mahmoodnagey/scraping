import re
import csv

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

text_src = read_file('houston-christian-university-source.txt')  # Replace 'sample.txt' with your file path
def separate_prerequisites(text):
    lines = text.split('\n')
    new_lines = []

    for line in lines:
        if 'Prerequisite(s):' in line:
            # Split the line at "Prerequisite(s):" and add a new line
            parts = line.split('Prerequisite(s):', 1)
            new_lines.append(parts[0].strip())
            new_lines.append('Prerequisite(s):' + parts[1].strip())
        else:
            new_lines.append(line.strip())

    # Join the modified lines back into a single string
    modified_text = '\n'.join(new_lines)
    return modified_text

text = separate_prerequisites(text_src)

# Regular expression pattern to capture code, title, prerequisites, and description
pattern = re.compile(r'(?P<code>[A-Z]+\s?(?:\d{4}|\d{4}/\s?\d{4}))\s+(?P<title>[^\n]+)\nPrerequisite\(s\):(?P<prerequisites>[^\n]+)\n(?P<description>[\s\S]+?)(?=\n[A-Z]+\s?(?:\d{4}|\d{4}/\s?\d{4})|$)', re.M)

matches = list(pattern.finditer(text))

# Prepare data for CSV
csv_data = []
for match in matches:
    code = match.group('code')
    title = match.group('title').strip()
    prerequisites = match.group('prerequisites').strip()
    credit = 'N/A'
    description = match.group('description').strip()
    csv_data.append([code, title, credit, description])

# Write to CSV
with open('houston-christian-university.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['code', 'title', 'credit', 'description'])  # headers
    writer.writerows(csv_data)

print("Data exported to courses.csv")
