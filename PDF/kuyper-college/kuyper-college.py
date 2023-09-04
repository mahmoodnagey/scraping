import re
import csv

# Open the text file
with open('kuyper-college-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data
    pattern = re.compile(
        r'([A-Z/]+\s\d{3}(?:\s+and\s+[A-Z/]+\s\d{3})?)\s(.+?)\n(\d+)\scredit(?:s)?(?:\s(each))?(?:\s(?:hour|hours))?[\s\n](.+?)(?=\n[A-Z/]+\s\d{3}|\Z)',
        re.DOTALL)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)
    for match in matches:
        code = match[0]
        title = match[1]
        credit = int(match[2])
        description = match[4].strip()

        # Remove "hours" or "hour" from the beginning of the description
        description = re.sub(r'^(?:hours|hour)\s', '', description, flags=re.IGNORECASE)

        # Append the extracted course data as a dictionary
        course_data.append({
            'code': code,
            'title': title,
            'credit': credit,
            'description': description
        })

# Write the extracted course data to a CSV file
with open('kuyper-college.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=['code', 'title', 'credit', 'description'])

    # Write header row
    csv_writer.writeheader()

    # Write course data rows
    csv_writer.writerows(course_data)

print("CSV file 'kuyper-college.csv' has been created with the extracted course data.")