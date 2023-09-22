import re
import csv

# Open the text file
with open('sul-ross-state-university-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data
    pattern = re.compile(r'([A-Z]+ \d+)(?: \([A-Z]+ \d+\))?\s+(.*?)(\(\d-\d\))\.(\s*(?:\n\s*QEP MAPPED COURSE\.\s*)?[\s\S]*?)(?:\n\s*Equivalent courses:\s(.*?))?(?=\n[A-Z]+ \d+|\Z)')

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    for match in matches:
        code, title, credits, description, equivalent_courses = match
        credits = int(credits[1])  # Extract the second digit from credits
        description = description.strip()
        prerequisites_match = re.search(r'Prerequisite:\s(.+?)(?=\n|$)', description)
        prerequisites = prerequisites_match.group(1) if prerequisites_match else "None"
        
        equivalent_courses = equivalent_courses.strip() if equivalent_courses else "None"
        
        course_data.append({
            'code': code.strip(),
            'title': title.strip(),
            'credits': credits,
            'description': description + prerequisites + equivalent_courses,
        })

# Write the extracted course data to a CSV file
with open('sul-ross-state-university.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'title', 'credits', 'description'])

    # Write course data rows
    for course in course_data:
        csv_writer.writerow([course['code'], course['title'], course['credits'], course['description']])

print("CSV file 'sul-ross-state-university' has been created with the extracted course data.")
