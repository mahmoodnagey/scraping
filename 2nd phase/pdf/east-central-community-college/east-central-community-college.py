import re
import csv

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Your sample text
sample_text = read_file('east-central-community-college-source.txt')

# Regular expression pattern to extract course details
pattern = r'([A-Z]+ \d{4}) — (.*?) — ([\s\S]*?)(?=(?:[A-Z]+ \d{4} —)|(?:$))'

# Function to extract credit information from the description
def extract_credit(description):
    # Patterns to match numeric credit values with various formats
    credit_patterns = [
        r'(\d+) (?:semester|hour)s? credit',  # Three semester hours credit
        r'(\d+) (?:semester|hour)s?',  # Three semester hours
        r'(\d+) credit',  # Three hours credit
        r'(\d+) semester hour credit',  # One semester hour credit
        r'(\d+) semester hour'  # One semester hour
    ]

    for pattern in credit_patterns:
        credit_match = re.search(pattern, description, re.IGNORECASE)
        if credit_match:
            credit = credit_match.group(1)
            return credit

    # Mapping of credit words to numbers
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
        'thirteen': '13',
        'fourteen': '14',
        'fifteen': '15'
    }

    # Split the description into words and look for credit words
    words = description.split()
    for word in words:
        word = word.lower()  # Convert to lowercase for matching
        if word in credit_mapping:
            credit = credit_mapping[word]
            return credit

    # If no credit pattern or word is found, return 'N/A'
    return 'N/A'




# Extract course details using regular expressions
matches = re.finditer(pattern, sample_text)

# Prepare CSV file
csv_filename = 'east-central-community-college.csv'
csv_header = ['code', 'title', 'credit', 'description']

with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_header)
    writer.writeheader()

    for match in matches:
        code = match.group(1)
        title = match.group(2).strip() if match.group(2) else ''
        description = match.group(3).strip() if match.group(3) else ''

        # Extract credit from the description
        credit = extract_credit(description)

        writer.writerow({'code': code,
                         'title': title,
                         'credit': credit,
                         'description': description})

print(f'Data has been extracted and saved to {csv_filename}.')
