from fastapi.testclient import TestClient
import pytest
from backend.database import engine, metadata
from backend.main import app 
import io
from backend.routers.task11_text_extraction import extractTextFromPdf

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def clearDatabase():
    # Clear the database before each test
    metadata.drop_all(bind=engine) 
    metadata.create_all(bind=engine) 

def testValidResumeUpload():
    with open("./sample.pdf", "rb") as file:
        response = client.post(
            "/api/resume-upload",
            files={"resumeFile": file},
            headers={"sessionToken": "test-token"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Resume uploaded successfully."

def testInvalidResumeFileType():
    with open("./sample.txt", "rb") as file:
        response = client.post(
            "/api/resume-upload",
            files={"resumeFile": file},
            headers={"sessionToken": "test-token"}
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid file type. Only PDF files are allowed."

def testExtractTextFromPdf():
    with open("functionalsample.pdf", "rb") as pdf_file:
        pdf_bytes = io.BytesIO(pdf_file.read())

    expected_text = "Functional Resume Sample    John W. Smith   2002 Front Range Way Fort Collins, CO 80525   jwsmith@colostate.edu    Career Summary    Four years experience in early childhood development with a diverse background in the care of  special needs children and adults.      Adult Care Experience    • Determined work placement for 150 special needs adult clients.   • Maintained client databases and records.   • Coordinated client contact with local health care professionals on a monthly basis.      • Managed 25 volunteer workers.        Childcare Experience    • Coordinated service assignments for 20 part-time counselors and 100 client families.  • Oversaw daily activity and outing planning for 100 clients.   • Assisted families of special needs clients with researching financial assistance and  healthcare.  • Assisted teachers with managing daily classroom activities.     • Oversaw daily and special student activities.        Employment History     1999-2002 Counseling Supervisor, The Wesley Center, Little Rock, Arkansas.     1997-1999 Client Specialist, Rainbow Special Care Center, Little Rock, Arkansas   1996-1997 Teacher’s Assistant, Cowell Elem entary, Conway, Arkansas        Education    University of Arkansas at Little Rock, Little Rock, AR     • BS in Early Childhood Development (1999)  • BA in Elementary Education (1998)  • GPA (4.0 Scale):  Early Childhood Development – 3.8, Elementary Education – 3.5,  Overall 3.4.   • Dean’s List, Chancellor’s List"

    extracted_text = extractTextFromPdf(pdf_bytes)

    assert extracted_text == expected_text.strip()

def testExtractTextFromPdf2():
    with open("sample.pdf", "rb") as pdf_file:
        pdf_bytes = io.BytesIO(pdf_file.read())

    expected_text = "This is a sample PDF file."

    extracted_text = extractTextFromPdf(pdf_bytes)

    assert extracted_text == expected_text.strip()