def process_pdf(file_path):
    """
    Process the PDF file to extract text and prepare data for RAG methodology.
    
    Args:
        file_path (str): The path to the PDF file to be processed.
    
    Returns:
        str: Extracted text from the PDF.
    """
    from PyPDF2 import PdfReader

    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error processing PDF: {e}")
    
    return text.strip()  # Return the extracted text without leading/trailing whitespace.