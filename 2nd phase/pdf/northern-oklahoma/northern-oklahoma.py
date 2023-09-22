import re
import csv

# Open the text file
with open('northern-oklahoma-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data
    pattern = re.compile(r'([A-Z]{3,4} \d{4}) (.*?)\n(.*?)\n', re.DOTALL)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    for match in matches:
        code, title, description = match

        # Extract the last digit from the code as credits
        credits = int(code.strip()[-1])
        
        course_data.append({
            'code': code.strip(),
            'title': title.strip(),
            'credits': credits,
            'description': description.strip()
        })

# Write the extracted course data to a CSV file with the modified order
with open('northern-oklahoma.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'title', 'credit', 'description'])

    # Write course data rows
    for course in course_data:
        csv_writer.writerow([course['code'], course['title'], course['credits'], course['description']])

print("CSV file 'northern-oklahoma.csv' has been created with the extracted course data.")
