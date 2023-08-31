import re
import csv

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def extract_courses(text):
    # Split the text into blocks starting with the course code pattern
    course_blocks = re.split(r'(?=[A-Z]{2}\d{3,4})', text.strip())

    courses = []

    for block in course_blocks:
        if not block.strip():
            continue

        # Extract course number and course name together
        number_name_match = re.search(r'([A-Z]{2}\d{3,4}) ([^\n]+)', block)
        if number_name_match:
            number = number_name_match.group(1)
            name = number_name_match.group(2).strip()
        else:
            number, name = None, None

        # Extract credit hours
        hours_match = re.search(r'(\d+(\.\d)?) credit hours', block)
        hours = hours_match.group(1) if hours_match else None

        # Extract description, taking all content after credit hours detail until "Prerequisite:"
        desc_start_idx = hours_match.end() if hours_match else None
        description_end_idx = block.find("Prerequisite:") if "Prerequisite:" in block else len(block)
        description = block[desc_start_idx:description_end_idx].strip() if desc_start_idx is not None else None

        # Append to courses if we have all required details
        if number and name and hours and description:
            courses.append((number, name, hours, description))

    return courses

text = read_file('itt-technical-institute-source.txt')

courses = extract_courses(text)

# Export to CSV
with open('itt-technical-institute.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Course Number", "Course Name", "Credit Hours", "Description"])
    for course in courses:
        csvwriter.writerow(course)
