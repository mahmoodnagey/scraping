import re
import csv

# Open the text file
with open('oklahoma-state-university-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data
    pattern = re.compile(r'(\w+\s+\d+(?:-\d+)?)\s+(.*?)\s+\|\s+(\d+(?:-\d+)?)\s*(?:Credit\s+Hour|Hours)?\s+(.*?)\s+(?:Prerequisites:\s+(.*?))?(?=(?:\w+\s+\d+(?:-\d+)?)|\Z)', re.DOTALL)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    for match in matches:
        code, title, credits, description, prerequisites = match

        # Extract prior learning assessment information if it exists
        pla_match = re.search(r'(\d+-\d+)\s*CREDIT\s*HOURS', code)
        pla_credits = pla_match.group(1) if pla_match else None

        # Remove prior learning assessment information from course code
        code = re.sub(r'\(\d+-\d+\s*CREDIT\s*HOURS\)', '', code).strip()

        # Concatenate description and prerequisites if both exist
        combined_description = description.strip()
        if prerequisites:
            combined_description += '\nPrerequisites: ' + prerequisites.strip()

        course_data.append({
            'code': code,
            'title': title.strip(),
            'credits': pla_credits if pla_credits else credits.strip(),
            'description': combined_description
        })

# Write the extracted course data to a CSV file
with open('oklahoma-state-university.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'title', 'credits', 'description'])

    # Write course data rows
    for course in course_data:
        csv_writer.writerow([course['code'], course['title'], course['credits'], course['description']])

print("CSV file 'oklahoma-state-university.csv' has been created with the extracted course data.")
