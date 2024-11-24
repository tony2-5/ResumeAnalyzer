from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.task11_text_extraction import router  # 导入 router
import os

# 创建 FastAPI 应用并注册路由
app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_valid_resume_upload():
    # 使用相对路径找到 sample.pdf 文件
    file_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
    with open(file_path, "rb") as file:
        response = client.post("/store-resume", files={"resume_file": file})
        assert response.status_code == 200
        assert "extracted_text" in response.json()

def test_invalid_file_type():
    file_path = os.path.join(os.path.dirname(__file__), "sample.txt")
    with open(file_path, "rb") as file:
        response = client.post("/store-resume", files={"resume_file": file})
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid file type. Only PDF files are allowed."
