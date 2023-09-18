import re
import csv


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


text = read_file('wsu-tech-college-source.txt')

# Split the text into individual courses
courses = re.split(r'\n(?=[A-Z]{3} \d{3})', text.strip())

# Initialize a list to store course data
course_data = []

# Iterate through each course and extract data
for course in courses:
    lines = course.strip().split('\n')

    # Check if there are at least 4 lines in the 'lines' list before extracting data
    if len(lines) >= 4:
        code, title = lines[0].split(maxsplit=1)

        # Concatenate the first 3 digits of the title with the code
        code = f"{code} {title[:3]}"
        title = title[4:]  # Remove the first 4 characters

        description = lines[3].strip()

        # Use try-except to handle the case where 'Total Credits' is not found
        try:
            credit = int(re.search(r'Total Credits\s+(\d+)', course).group(1))
        except AttributeError:
            credit = None  # Set credit to None if 'Total Credits' is not found

        course_data.append([code, title, credit, description])

# Define the CSV filename
csv_filename = 'wsu-tech-college.csv'

# Write the extracted data to a CSV file
with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header row
    csv_writer.writerow(['code', 'title', 'credit', 'description'])
    # Write course data
    csv_writer.writerows(course_data)

print(f'Data has been extracted and saved to {csv_filename}')
