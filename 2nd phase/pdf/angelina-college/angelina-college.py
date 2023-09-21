import re
import csv

# Open the text file
with open('angelina-college-source.txt', 'r', encoding='utf-8') as txt_file:
    txt_content = txt_file.read()

    # Create a regex pattern to match course data with the enhanced formats
    pattern = re.compile(r'([A-Z]+\s\d+)\s*[-–]\s*([^.,]+)[.,]\s*(\d+(?:-hour)?\s?credit)\s*(?:hours)?[.]\s*(.*?)(?=\s[A-Z]+\s\d+|$)', re.DOTALL)

    # Initialize a list to store extracted course data
    course_data = []

    # Find all matches in the text content
    matches = pattern.findall(txt_content)

    for match in matches:
        code, title, credits, description = match

        # Remove extra whitespace from the description
        description = description.strip()

        # Extract the numeric part of the credit hours and convert it to an integer
        credit_hours = int(re.search(r'\d+', credits).group())

        course_data.append({
            'code': code.strip(),
            'title': title.strip(),
            'credits': credit_hours,
            'description': description
        })

# Write the extracted course data to a CSV file
with open('angelina-college.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['code', 'title', 'credit', 'description'])

    # Write course data rows
    for course in course_data:
        csv_writer.writerow([course['code'], course['title'], course['credits'], course['description']])

print("CSV file 'angelina-college' has been created with the extracted course data.")
