import fitz  # PyMuPDF

def extract_text_from_pdf(input_pdf, output_text, start_page, end_page):
    pdf_document = fitz.open(input_pdf)
    
    with open(output_text, 'w', encoding='utf-8') as text_file:
        for page_num in range(start_page - 1, min(end_page, len(pdf_document))):
            page = pdf_document[page_num]
            page_text = page.get_text("text")
            text_file.write(page_text)
    
    pdf_document.close()

if __name__ == "__main__":
    input_pdf_file = "./oklahoma-christian-university.pdf"  # Replace with your input PDF file path
    output_text_file = "oklahoma-christian-university-source.txt"  # Replace with the desired output text file path
    start_page_number = 138 # Replace with the starting page number
    end_page_number = 180  # Replace with the ending page number
    
    extract_text_from_pdf(input_pdf_file, output_text_file, start_page_number, end_page_number)
    print(f"Text extracted from pages {start_page_number}-{end_page_number} and saved to '{output_text_file}'.")
