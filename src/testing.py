import subprocess

async def run_tests(directory: str):
    """
    Runs pytest for the specified directory and returns the results.
    """
    try:
        # Run pytest with output capture
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
