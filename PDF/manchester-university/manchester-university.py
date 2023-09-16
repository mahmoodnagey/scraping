import re
import csv

# Open the text file
with open('manchester-university-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data with codes like "3XX"
    pattern = re.compile(
        r'((?:\d+\s?or\s\d+|[A-Z]?\d{3}[A-Z]?|[A-Z]+\s\d+|(?:\d+|[\dX]{3})[A-Z]?))\s+(.*?)\s-\s((?:\d*(?:\.\d+)?(?:\s?or\s\d*(?:\.\d+)?)?|\d+\s?to\s\d*(?:\.\d+)?)?(?:\s?-\s?(?:\d*(?:\.\d+)?|\d+\s?or\s\d*(?:\.\d+)?|\d+\s?to\s\d*(?:\.\d+)?))?)\s+(?:hour|hours?)\s+(.*?)\n(?=(?:\d+\s?or\s\d+|[A-Z]?\d{3}[A-Z]?|[A-Z]+\s\d+|(?:\d+|[\dX]{3})[A-Z]?))'
        r'|'
        r'([A-Z]+(?:\s[A-Z]+)?\s\d+[A-Z]?)\s+(.*?)\s+-\s(\d+)\s+hour(?:s)?\s+(.+?)(?=(?:[A-Z]+\s\d+[A-Z]?|$))',
        re.DOTALL | re.IGNORECASE)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    for match in matches:
        if match[0]:  # matches from the first part of the pattern
            codes = match[0]
            name = match[1].strip()
            credits = match[2]
            description = match[3].strip()
        else:  # matches from the second part of the pattern
            codes = match[4]
            name = match[5].strip()
            credits = match[6]
            description = match[7].strip()

        course = {
            'Code': codes,
            'Title': name,
            'Credits': credits,
            'Description': description,
        }

        course_data.append(course)

# Write the extracted course data to a CSV file
with open('manchester-university.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'title', 'credit', 'description'])

    # Write course data rows
    for course in course_data:
        csv_writer.writerow(course.values())

print("CSV file 'manchester-university' has been created with the extracted course data.")