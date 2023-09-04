import re
import csv

# Open the text file
with open('./taylor-university-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data
    pattern = re.compile(r'([A-Z]+\s(?:\d+|xxx))\s+(\d+-\d+|\d+)\s+hour[s]?\s+(.*?)(?=\n[A-Z]+\s(?:\d+|xxx)|$)',
                         re.DOTALL)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    for match in matches:
        code, credit_hours, description = match
        code = code.strip()
        credit_hours = credit_hours.strip()

        # Extract course name from the description
        description_lines = description.split('\n')
        course_name = description_lines[0].strip()

        # Remove the course name from the description
        description = '\n'.join(description_lines[1:]).strip()

        course_info = {
            'code': code,
            'credit': credit_hours,
            'title': course_name,
            'description': description,
        }

        course_data.append(course_info)

# Write the extracted course data to a CSV file
with open('taylor-university.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'title', 'credit', 'description'])

    # Write course data rows
    for course in course_data:
        # Display the name first, followed by credit hours
        course_row = [course['title'], f"{course['credit']} - {course['code']}", course['description']]
        csv_writer.writerow([course['code'], course['title'], course['credit'], course['description']])

print("CSV file 'taylor-university' has been created with the extracted course data.")