from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
import uvicorn
from compilation import handle_compilation
from testing import run_tests
from notification import Notification, send_notification
import os


app = FastAPI()
PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class GitHubWebhook(BaseModel):
    ref: str
    repository: dict[str, Any]
    commits: list[dict[str, Any]]
    head_commit: dict[str, Any]


@app.get("/")
def root():
    return {"message": "CI"}


@app.post("/webhook")
async def github_webhook(payload: GitHubWebhook):
    branch = payload.ref.split("/")[-1]
    repo_name = payload.repository["full_name"]
    commit_sha = payload.head_commit["id"]
    authors =[commit["author"]["name"] for commit in payload.commits
]
    # Run compilation process
    compilation_result = await handle_compilation(branch)
    
    # Run tests
    test_result = await run_tests(os.path.join(PROJECT_DIR,"tests"))

    await send_notification(Notification(authors=authors,branch=branch,commit=commit_sha,project=repo_name,status=test_result["success"],output=test_result["output"]))

    return {
        "status": "completed",
        "authors": authors,
        "branch": branch,
        "repository": repo_name,
        "commit": commit_sha,
        "compilation": compilation_result,
        "tests": test_result
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
