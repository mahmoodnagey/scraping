import re
import csv

# Open the text file
with open('highland-community-college-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data
    pattern = re.compile(r'(^\^?[A-Z]+\d{3}|\^?[A-Z]+\s\d{3}|\^?[A-Z]+\s\d{3}[A-Z]?\s*-\s*\d{3}[A-Z]?)\s(.*?)\s+(\d)\s+(.*?)\s+(?=(?:^\^?[A-Z]+\d{3}|\^?[A-Z]+\s\d{3}|\^?[A-Z]+\s\d{3}[A-Z]?\s*-\s*\d{3}[A-Z]?|$))', re.DOTALL | re.MULTILINE)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)
    for match in matches:
        code = match[0].strip()
        title = match[1].strip()
        credit = match[2].strip()
        description = match[3].strip()

        # Create a dictionary for each course
        course_info = {
            'code': code,
            'title': title,
            'credit': credit,
            'description': description,
        }

        course_data.append(course_info)

# Write the extracted course data to a CSV file
with open('highland-community-college.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'title', 'credit', 'description'])

    # Write course data rows
    for course in course_data:
        csv_writer.writerow([course['code'], course['title'], course['credit'], course['description']])

print("CSV file 'highland-community-college.csv' has been created with the extracted course data.")