import re
import csv

# Open the text file
with open('community-care-college-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data
    pattern = re.compile(r'(\w{2,6}\d+)\s+(.*?)\s+Lecture Hrs:\s+(\d+)\s+Lab Hrs:\s+(\d+)\s+Credit Hrs:\s+(\d+)(?:\s+(.*?)\s*(?=\w{2,4}\d+|$))?', re.DOTALL | re.MULTILINE)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    for match in matches:
        code, title, lecture_hrs, lab_hrs, credits, description = match

        course_data.append({
            'code': code.strip(),
            'title': title.strip(),
            'credits': int(credits),
            'description': description.strip() if description else '',
            'lecture_hrs': lecture_hrs.strip(),
            'lab_hrs': lab_hrs.strip()
        })

# Write the extracted course data to a CSV file
with open('community-care-college.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'title', 'credit', 'description'])

    # Write course data rows
    for course in course_data:
        csv_writer.writerow([course['code'], course['title'], course['credits'], course['description']])

print("CSV file 'community-care-college' has been created with the extracted course data.")
