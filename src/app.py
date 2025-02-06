from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

app = FastAPI()


class GitHubWebhook(BaseModel):
    ref: str
    repository: Dict[str, Any]
    commits: list[Dict[str, Any]]
    head_commit: Dict[str, Any]


@app.get("/")
def root():
    return {"message": "CI"}


@app.post("/webhook")
async def github_webhook(payload: GitHubWebhook):
    branch = payload.ref.split("/")[-1]
    repo_name = payload.repository["full_name"]
    commit_sha = payload.head_commit["id"]

    # TODO: add CI logic
    return {
        "status": "received",
        "branch": branch,
        "repository": repo_name,
        "commit": commit_sha,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
