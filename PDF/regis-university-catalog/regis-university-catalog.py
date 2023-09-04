import re
import csv

# Load the content of the uploaded file
with open("regis-university-catalog-source.txt", "r") as file:
    content_stepwise = file.read()

# Craft a regex pattern based on the provided examples and instructions
pattern_stepwise = re.compile(r'(?P<code>[A-Z]+\s+\d+[A-Z\-]*(?:/[A-Z]+\s+\d+[A-Z\-]*)?)\.\s+(?P<title>[A-Z\s]+)\((?P<credit>\d+(?:-\d+)?)\)\.\s+', re.DOTALL)

# Identify the start of each course block using the course code/title/credit pattern
course_starts = [match.start() for match in re.finditer(pattern_stepwise, content_stepwise)]

# Extract courses using the identified course starts
course_list_adjusted = []
for i in range(len(course_starts)):
    # Start of current course
    start = course_starts[i]
    # End of current course (start of next course or end of content)
    end = course_starts[i + 1] if i + 1 < len(course_starts) else len(content_stepwise)
    
    course_content = content_stepwise[start:end].strip()
    match = pattern_stepwise.match(course_content)
    
    if match:
        course_list_adjusted.append({
            "code": match.group("code"),
            "title": match.group("title"),
            "credit": match.group("credit"),
            "description": re.sub(r'\n+', ' ', course_content[match.end():]).strip()
        })

# Save the extracted data to a CSV file
csv_file_path_adjusted = "regis-university-catalog.csv"
with open(csv_file_path_adjusted, 'w', newline='') as csvfile:
    fieldnames = ['code', 'title', 'credit', 'description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for course in course_list_adjusted:
        writer.writerow(course)
