from fastapi import FastAPI, HTTPException, Request
import subprocess
import git
import os
import asyncio  # Added for async execution of blocking calls

app = FastAPI()

# Automatically detect the absolute path of the project directory
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

@app.post("/webhook")
async def webhook_handler(request: Request):
    """
    Webhook listener for CI compilation.
    Triggers static syntax checking for Python when a push event occurs.
    """
    try:
        payload = await request.json()
        branch_name = payload.get("ref", "").replace("refs/heads/", "")

        if not branch_name:
            raise HTTPException(status_code=400, detail="Invalid payload: No branch found")

        # Log which branch triggered the CI
        print(f"Received webhook event for branch: {branch_name}")

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
        raise HTTPException(status_code=500, detail=str(e))

def run_syntax_check(directory):
    """
    Runs a Python syntax check (static analysis) using flake8.
    """
    try:
        result = subprocess.run(["flake8", directory], capture_output=True, text=True)
        return result.stdout or "No syntax errors found."
    except Exception as e:
        return str(e)
