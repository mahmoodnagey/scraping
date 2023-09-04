import re
import csv

# Open the text file
with open('houghton-university-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match each course individually
    pattern = re.compile(
        r'(\w+(?: \w+)? (?:\d+(?:, ?\d+)*(?:- \w+(?: \w+)?)?)+) ([^\n]+)\n((?:\d+(?:, ?\d+)*(?:- \w+(?: \w+)?)?)+-[^\n]+)\n((?:(?!\w+(?: \w+)? (?:\d+(?:, ?\d+)*(?:- \w+(?: \w+)?)?)+).+?(?=\w+(?: \w+)? (?:\d+(?:, ?\d+)*(?:- \w+(?: \w+)?)?)+)|\Z))',
        re.DOTALL)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    for match in matches:
        code = match[0]
        name = match[1]
        credit_hours = match[2]
        description = match[3].strip()  # Remove leading/trailing whitespace

        # Append the extracted data as a dictionary
        course_data.append({
            'code': code,
            'title': name,
            'credit': credit_hours,
            'description': description
        })

# Adjust the credit hours to only numeric part
for course in course_data:
    course['credit'] = course['credit'].split('-')[0].strip()

# Rename the output CSV file
output_file_name = 'houghton-university.csv'

# Write the extracted course data to the renamed CSV file
with open(output_file_name, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=['code', 'title', 'credit', 'description'])

    # Write header row
    csv_writer.writeheader()

    # Write course data rows
    csv_writer.writerows(course_data)

print(f"CSV file '{output_file_name}' has been created with the extracted course data.")