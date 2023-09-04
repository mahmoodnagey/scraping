import re
import csv

# Open the text file
with open('san-diego-christian-college-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data
    pattern = re.compile(
        r'([A-Z]+\s\d+(?:[A-Z])?(?:\s[A-Z]+)?(?:\s\&\s[A-Z]+)?(?:/\d+(?:[A-Z])?)?(?:/[A-Z])?)(?:\s*\.{2,}\s*)([^\(]+)\s+\((\d+(?:-\d+)?)\)\s*([\s\S]+?(?=(?:[A-Z]+\s\d+(?:[A-Z])?(?:\s[A-Z]+)?(?:\s\&\s[A-Z]+)?(?:/\d+(?:[A-Z])?)?(?:/[A-Z])?)\s*\.{2,}|\Z))')

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    for match in matches:
        code = match[0].strip()
        title = match[1].strip()
        credit = match[2].strip()
        description = match[3].strip()

        course_info = {
            'code': code,
            'title': title,
            'credit': credit,
            'description': description
        }

        course_data.append(course_info)

# Write the extracted course data to a CSV file
with open('san-diego-christian-college.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'title', 'credit', 'description'])

    # Write course data rows
    for course in course_data:
        csv_writer.writerow([course['code'], course['title'], course['credit'], course['description']])

print("CSV file 'san-diego-christian-college.csv' has been created with the extracted course data.")