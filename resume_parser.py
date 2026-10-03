import pypdf
import docx
import io

def extract_text_from_pdf(file_bytes):
    """Extracts text from a PDF file."""
    text = ""
    try:
        pdf_reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")
    return text

def extract_text_from_docx(file_bytes):
    """Extracts text from a DOCX file."""
    text = ""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        raise ValueError(f"Failed to extract text from DOCX: {e}")
    return text

def parse_resume(file, filename: str) -> str:
    """
    Parses a resume file (PDF or DOCX) and returns the extracted text.
    """
    file_bytes = file.read()
    
    if filename.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith('.docx'):
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")
