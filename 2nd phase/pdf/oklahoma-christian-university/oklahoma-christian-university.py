import re
import csv

# Open the text file
with open('oklahoma-christian-university-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data
    pattern = re.compile(r'((?:\d{4}(?:-\d{4})?|\d{4})(?:[,-]\s*(?:\d{4}(?:-\d{4})?|\d{4}))*)\s+(.*?)\s*\n(.*?)\n(?=\d{4}(?:-\d{4})?|\Z)', re.DOTALL)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    for match in matches:
        codes_str, title, description = match
        # Extract and format the unique credits from the course codes
        codes = [code.strip() for code in re.split(r'[,-]', codes_str)]
        unique_credits = set()
        for code in codes:
            if '-' not in code:
                unique_credits.add(code[-1])
            else:
                range_parts = code.split('-')
                unique_credits.add(f"{range_parts[0][-1]}-{range_parts[1][-1]}")
        credits = ', '.join(sorted(unique_credits))
        course_data.append({
            'code': codes_str.strip(),
            'title': title.strip(),
            'credits': credits,
            'description': description.strip()
        })

# Write the extracted course data to a CSV file
with open('oklahoma-christian-university.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'title', 'credits', 'description'])

    # Write course data rows
    for course in course_data:
        csv_writer.writerow([course['code'], course['title'], course['credits'], course['description']])

print("CSV file 'oklahoma-christian-university' has been created with the extracted course data.")
