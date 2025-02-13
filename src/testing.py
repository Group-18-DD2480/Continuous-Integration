import os
import subprocess

async def run_tests(directory: str):
    """
    Runs pytest for the specified directory and returns the results.

    Args:
        directory (str): The path to the directory containing the tests.

    Returns:
        dict: A dictionary containing:
            - "success" (bool): Whether the tests passed or failed.
            - "output" (str): The standard output from pytest.
            - "error" (str or None): The error message if the tests failed, otherwise None.

    Raises:
        Exception: If an unexpected error occurs while running the tests.
    """
    try:
        result = subprocess.run(
            ["pytest", directory, "-v"],
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except Exception as e:
        return {
            "success": False,
            "output": None,
            "error": str(e)
        }
