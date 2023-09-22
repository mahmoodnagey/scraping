import re
import csv

# Open the text file
with open('concordia-univeristy-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data with the enhanced formats
    pattern = re.compile(r'(\b\w{2,4} (\d{1})(\d{2,3}(?:-\d{2,4})?)[A-Z]*\d*[A-Z]?)\s+(.*?)\n(.*?)\nPre-Requisites:\s*(.*?)(?:\nCo-requisites:\s*(.*?))?(?=\n|$)', re.DOTALL)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    for match in matches:
        code, credit_hours, course_number, title, description, prerequisites, corequisites = match

        # Remove extra whitespace from the description, prerequisites, and corequisites
        description = description.strip()
        prerequisites = prerequisites.strip()
        corequisites = corequisites.strip() if corequisites else "None"

        # Extract individual course codes from the Co-requisites field
        corequisites_codes = re.findall(r'\b\w{2,4} (\d{1})(\d{2,3}(?:-\d{2,4})?)[A-Z]*\d*[A-Z]?', corequisites)

        # Convert lists to strings and append them to the description
        prerequisites_str = 'Prerequisites: {}'.format(prerequisites)
        corequisites_str = 'Corequisites: {}'.format(', '.join(corequisites_codes))

        description += '\n\n' + prerequisites_str + '\n\n' + corequisites_str

        course_data.append({
            'code': code.strip(),
             'title': title.strip(),
            'credit_hours': credit_hours,
            'description': description
        })

    # Create a regex pattern to match the additional course format
    additional_pattern = re.compile(r'(\b\w{3,4} \d{4}[A-Z]?\s*/\s*\d{4}[A-Z]?)\s+(.*?)\n(.*?)\nPre-Requisites:\s*(.*?)(?=\n|$)', re.DOTALL)

    # Find all matches for the additional course format
    additional_matches = additional_pattern.findall(txt_content)

    for match in additional_matches:
        code, title, description, prerequisites = match

        # Remove extra whitespace from the description and prerequisites
        description = description.strip()
        prerequisites = prerequisites.strip()

        # Convert prerequisites to a string and append it to the description
        prerequisites_str = 'Prerequisites: {}'.format(prerequisites)

        description += '\n\n' + prerequisites_str

        course_data.append({
            'code': code.strip(),
            'title': title.strip(),
            'credit_hours': 3,
            'description': description
        })

# Write the extracted course data to a CSV file
with open('concordia-univeristy.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'title', 'credit_hours',  'description'])

    # Write course data rows
    for course in course_data:
        csv_writer.writerow([course['code'],  course['title'], course['credit_hours'], course['description']])

print("CSV file 'concordia-university.csv' has been created with the extracted course data.")
