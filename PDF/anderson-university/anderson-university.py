import re
import csv

# Open the text file
with open('anderson-university-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Initialize a list to store extracted course data
    course_data = []

    # Separate out course package identifiers
    sections = re.split(r'([A-Z]+ COURSES)', txt_content)
    current_prefix = None

    for i in range(len(sections)):
        # If the section is a course package identifier
        if 'COURSES' in sections[i]:
            current_prefix = sections[i].split(' ')[0] + " "
        else:
            # Use regex pattern to match course data
            pattern = re.compile(
                r'(\d{4})\s+([\s\S]+?)\s+(\d+(?:-\d+)?(?:\s*-\s*\d+)?)(?:\s*hrs?\.? \((\d+(?:,\s*\d+)?)\))?\s+([\s\S]+?)(?:(PREREQUISITE|COREQUISITE|EXPECTATION):\s+((?:[\w\s]+\s+(?:\d+|\d+\s*(?:or\s*\d+)?)\s*(?:,\s*[\w\s]+\s+(?:\d+|\d+\s*(?:or\s*\d+)?)\s*)*))[\s\S]*?)?(?=(?:\d{4})|$)')

            # Find all matches in the section content
            matches = pattern.findall(sections[i])
            for match in matches:
                code = current_prefix + match[0] if current_prefix else match[0]
                name = match[1].strip()
                credits = match[2]
                credit_hours = match[3] if match[3] else ""
                description = match[4].strip()
                prerequisite_type = match[5] if match[5] else ""
                prerequisite_str = match[6] if match[6] else ""

                # Include credit hours in the description
                if credit_hours:
                    description += f' ({credit_hours})'

                # Include prerequisite information in the description
                if prerequisite_type and prerequisite_str:
                    description += f' {prerequisite_type}: {prerequisite_str}'

                # Remove any trailing whitespace from description
                description = description.rstrip()

                # Append extracted data to the list
                course_data.append({'code': code, 'title': name, 'credit': credits, 'description': description})

# Write the extracted course data to a CSV file
with open('anderson-university.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=['code', 'title', 'credit', 'description'])

    # Write header row
    csv_writer.writeheader()

    # Write course data rows
    csv_writer.writerows(course_data)

print("CSV file 'anderson-university.csv' has been created with the extracted course data.")
