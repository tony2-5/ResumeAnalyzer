from pypdf import PdfReader
import io

def extractTextFromPdf(file: io.BytesIO) -> str:
    '''
     Extract text from pdf
    '''
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.replace("\n", " ").strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")
