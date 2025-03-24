def process_pdf(file_path):
    """
    Esta función recibe la ruta de un PDF y devuelve el texto extraído.
    Se puede implementar con PyPDF2 u otra librería.
    """
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error procesando PDF: {e}")
        return ""
