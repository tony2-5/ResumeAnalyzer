from fastapi.testclient import TestClient
from backend.main import app 

client = TestClient(app)

def testValidResumeUpload():
    with open("./sample.pdf", "rb") as file:
        response = client.post("/store-resume", files={"resume_file": file})
        assert response.status_code == 200
        assert "extracted_text" in response.json()

def testInvalidFileType():
    with open("./sample.txt", "rb") as file:
        print(file)
        response = client.post("/store-resume", files={"resume_file": file})
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid file type. Only PDF files are allowed."
