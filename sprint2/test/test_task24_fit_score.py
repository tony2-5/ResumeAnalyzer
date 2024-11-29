from fastapi.testclient import TestClient
from API.main import app  # 确保导入完整的 FastAPI 应用

client = TestClient(app)  # 使用完整的 FastAPI 应用

def test_fit_score_success():
    payload = {
        "resume_text": "Experienced software engineer with Python and Java skills...",
        "job_description": "Looking for a software engineer with experience in Python, AWS, and REST APIs."
    }
    response = client.post("/api/fit-score", json=payload)
    assert response.status_code == 200
    assert "fit_score" in response.json()
    assert "feedback" in response.json()

def test_fit_score_invalid_payload():
    """
    Test that the API returns an error when required fields are missing.
    """
    # 缺少 job_description 字段
    payload = {"resume_text": "Some text without job description."}
    response = client.post("/api/fit-score", json=payload)
    
    # 断言状态码为 422
    assert response.status_code == 422
    
    # 检查返回的 JSON 是否包含 "job_description" 缺失的信息
    error_detail = response.json()["detail"]
    assert any(error["loc"] == ["body", "job_description"] for error in error_detail)
