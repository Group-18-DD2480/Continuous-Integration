import pytest
from src.testing import run_tests

@pytest.mark.asyncio
async def test_run_tests():
    result = await run_tests("tests")
    assert isinstance(result, dict)
    assert "success" in result
    assert "output" in result

@pytest.mark.asyncio
async def test_run_tests_invalid_directory():
    result = await run_tests("nonexistent_directory")
    assert not result["success"]
    assert result["error"] is not None
