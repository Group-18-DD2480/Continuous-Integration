import git
import os
import subprocess
import asyncio

# Automatically detect the absolute path of the project directory
PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

async def handle_compilation(branch_name: str):
    """
    Handles the compilation process for a given branch.
    """
    try:
        # Log which branch triggered the CI
        print(f"Processing compilation for branch: {branch_name}")

        # Pull the latest changes for the triggered branch asynchronously
        repo = git.Repo(PROJECT_DIR)
        await asyncio.to_thread(repo.git.checkout, branch_name)
        await asyncio.to_thread(repo.git.pull)

        # Perform syntax check
        result = run_syntax_check(PROJECT_DIR)

        return {
            "message": f"Compilation (syntax check) completed for branch: {branch_name}",
            "output": result
        }

    except Exception as e:
        raise Exception(f"Compilation error: {str(e)}")

def run_syntax_check(directory):
    """
    Runs a Python syntax check (static analysis) using flake8.
    """
    try:
        result = subprocess.run(["flake8", directory], capture_output=True, text=True)
        return result.stdout or "No syntax errors found."
    except Exception as e:
        return str(e)
