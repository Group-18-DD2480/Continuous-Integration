from fastapi import Request
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.compilation import app, run_syntax_check, webhook_handler
import asyncio

client = TestClient(app)

async def test_webhook_invalid_payload():
    request = Request(scope={"type": "http"}, receive=lambda: None)
    request._json = {}  # Mocking request.json()
    response = await webhook_handler(request)
    assert response.status_code == 400
    assert "Invalid payload" in response.detail

async def test_webhook_valid_branch():
    with patch("src.compilation.git.Repo") as mock_repo:
        mock_repo.return_value.git.checkout = MagicMock()
        mock_repo.return_value.git.pull = MagicMock()
        
        request = Request(scope={"type": "http"}, receive=lambda: None)
        request._json = {"ref": "refs/heads/test-branch"}  # Mocking request.json()
        response = await webhook_handler(request)
        assert response["message"].startswith("Compilation (syntax check) completed")

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
