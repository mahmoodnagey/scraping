import re
import csv

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Your sample text
sample_text = read_file('copiah-lincoln-community-college-source.txt')

# Regular expression pattern to extract course details
pattern = r'([A-Z]+ \d{4})\s+(.*?)\n(.*?)Credit, (\w+) semester hour(s)?\.|$'

# Credit value mapping from text to digits
credit_mapping = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'ten': '10',
    'eleven': '11',
    'twelve': '12',
    'thirteen': '13'
}

# Function to replace text credit values with digits
def replace_credit_text(text):
    for key, value in credit_mapping.items():
        text = text.replace(key, value)
    return text

# Extract course details using regular expressions
matches = re.finditer(pattern, sample_text, re.DOTALL)

# Prepare CSV file
csv_filename = 'copiah-lincoln-community-college.csv'
csv_header = ['code', 'title', 'credit', 'description']

with open(csv_filename, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_header)
    writer.writeheader()

    current_match = None
    pending_credit = None
    pending_description = ''

    for match in matches:
        if current_match is not None:
            code = current_match.group(1)
            title = current_match.group(2).strip() if current_match.group(2) else ''
            description = current_match.group(3).strip() if current_match.group(3) else ''
            credit = replace_credit_text(current_match.group(4).lower()) if current_match.group(4) else 'N/A'

            # Check if the current course information starts with a valid course code pattern
            # If not, consider it as a continuation of the previous course
            if re.match(r'[A-Z]+ \d{4}', title):
                # Write the previous course details
                writer.writerow({'code': code,
                                 'title': title,
                                 'credit': credit,
                                 'description': pending_description})

                # Store the current course details as pending
                pending_description = description
                code = current_match.group(1)
                title = current_match.group(2).strip() if current_match.group(2) else ''
                description = ''
                credit = 'N/A'

            # If "Credit" information is not on the same line as the description, use the pending_credit
            if not credit and pending_credit:
                credit = pending_credit
                pending_credit = None

            writer.writerow({'code': code,
                             'title': title,
                             'credit': credit,
                             'description': description})

        current_match = match

        # Check if "Credit" is not on the same line as description and store it as pending_credit
        if not match.group(4):
            pending_credit = replace_credit_text(match.group(3).lower())

print(f'Data has been extracted and saved to {csv_filename}.')
