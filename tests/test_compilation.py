from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest
from src.app import app
from src.compilation import handle_compilation, run_syntax_check

client = TestClient(app)

@pytest.mark.asyncio
async def test_handle_compilation_valid_branch():
    with patch("src.compilation.git.Repo") as mock_repo:
        mock_repo.return_value.git.checkout = MagicMock()
        mock_repo.return_value.git.pull = MagicMock()
        
        result = await handle_compilation("test-branch")
        assert result["message"].startswith("Compilation (syntax check) completed")

def test_run_syntax_check_valid():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "No syntax errors found."
        result = run_syntax_check("test_directory")
        assert result == "No syntax errors found."

def test_run_syntax_check_invalid():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "test.py:1:1: E999 SyntaxError: invalid syntax"
        result = run_syntax_check("test_directory")
        assert "E999 SyntaxError" in result

def test_webhook_endpoint():
    with patch("src.app.handle_compilation") as mock_handle:
        mock_handle.return_value = {
            "message": "Compilation completed",
            "output": "No syntax errors found."
        }
        
        response = client.post("/webhook", json={
            "ref": "refs/heads/test-branch",
            "repository": {"full_name": "test/repo"},
            "commits": [],
            "head_commit": {"id": "123abc"}
        })
        
        assert response.status_code == 200
        assert response.json()["branch"] == "test-branch"
        assert response.json()["status"] == "completed"

def test_webhook_invalid_payload():
    response = client.post("/webhook", json={})
    assert response.status_code == 422  # FastAPI validation error
