from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a given PDF file.
    """
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
    return text