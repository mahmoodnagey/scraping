import re
import csv

# Open the text file
with open('southwestern-university-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data
    pattern = re.compile(r'(\d{2}-\d{3}(?:, \d{3})*)\s+([A-Z\s]+)\.\s+(.*?)(?=\n\d{2}-\d{3}|$)', re.DOTALL)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    code, title, description = '', '', ''

    for match in matches:
        # If a new course code is found, add the previous course data
        if code:
            # Extract the last digit from the course code
            last_digit = int(re.search(r'(\d)$', code).group(1))
            course_data.append({
                'code': code.strip(),
                'name': title.strip(),
                'credits': last_digit,
                'description': description.strip() if description else None
            })

        # Update code, title, and description
        code, title, description = match

    # Add the last course data
    if code:
        # Extract the last digit from the course code
        last_digit = int(re.search(r'(\d)$', code).group(1))
        course_data.append({
            'code': code.strip(),
            'name': title.strip(),
            'credits': last_digit,
            'description': description.strip() if description else None
        })

# Write the extracted course data to a CSV file
with open('southwestern-university.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'name', 'credits', 'description'])

    # Write course data rows
    for course in course_data:
        csv_writer.writerow([course['code'], course['name'], course['credits'], course['description']])

print("CSV file 'southwestern-university' has been created with the extracted course data.")
