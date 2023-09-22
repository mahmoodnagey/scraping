import re
import csv

# Open the text file
with open('northeastern-oklahoma-agricultural-and-mechanical-college-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data
    pattern = re.compile(r'(\w+\s+\d{4}-\d{4}|\w+\s+\d{4})\s+(.*?)\s+(?:Class|Lab|Cr\.) (\d+-\d+|\d+),?\s+(.*?)\n(?=\w+\s+\d{4}|\Z)', re.DOTALL)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    for match in matches:
        code, title, credits, description = match

        if '-' in credits:
            min_credits, max_credits = map(int, credits.split('-'))
        else:
            min_credits = max_credits = int(credits)

        # Combine min and max credits into a single string
        if min_credits == max_credits:
            credits_range = str(min_credits)
        else:
            credits_range = f"{min_credits}-{max_credits}"

        course_data.append({
            'code': code.strip(),
            'title': title.strip(),
            'credits_range': credits_range,
            'description': description.strip()
        })

# Write the extracted course data to a CSV file
with open('northeastern-oklahoma-agricultural-and-mechanical-college.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'title', 'credit', 'description'])

    # Write course data rows
    for course in course_data:
        csv_writer.writerow([course['code'], course['title'], course['credits_range'], course['description']])

print("CSV file 'Northeastern Oklahoma Agricultural and Mechanical College' has been created with the extracted course data.")
