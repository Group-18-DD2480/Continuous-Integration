import os
from dotenv import load_dotenv
from fastapi_mail import (
    ConnectionConfig,
    FastMail,
    MessageSchema,
    MessageType
)
from pydantic import BaseModel

load_dotenv()
fast_mail = FastMail(
    ConnectionConfig(
        MAIL_FROM=os.getenv("MAIL_FROM"),
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_PORT=os.getenv("MAIL_PORT"),
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
    )
)

class Notification(BaseModel):
    """
    Represents a notification containing details about a CI/CD build event.

    Attributes:
        authors (list[str]): List of the authors of the commit.
        branch (str): The branch where the commit was made.
        commit (str): The commit hash.
        project (str): The project name.
        status (str): The build status (e.g., success, failure).
        timestamp (str | None): The timestamp of the build, if available.
    """
    authors: list[str] 
    branch: str
    commit: str
    project: str
    status: bool
    output: str | None = None
    timestamp: str | None = None

async def send_notification(notification: Notification):
    """
    Sends an email notification with CI/CD build details.

    Args:
        notification (Notification): The notification details to be sent.

    Returns:
        None
    """
    message = MessageSchema(
        subject=prepare_subject(notification),
        recipients=[fast_mail.config.MAIL_FROM],
        body=prepare_body(notification),
        subtype=MessageType.html
    )
    await fast_mail.send_message(message)

def prepare_subject(notification: Notification) -> str:
    """
    Prepares the email subject line based on the notification details.

    Args:
        notification (Notification): The notification containing build details.

    Returns:
        str: The formatted subject line.
    """
    return f"[CI Notification] Build {notification.status} for commit {notification.commit} on branch {notification.branch}"

def prepare_body(notification: Notification) -> str:
    """
    Prepares the email body in HTML format based on the notification details.

    Args:
        notification (Notification): The notification containing build details.

    Returns:
        str: The formatted HTML email body.
    """
    return f"""
    <html>
      <body>
        <p>Automated notification from Group 18 CI server.</p>

        <h3>Build Details:</h3>
        <ul>
          <li><strong>Project:</strong> {notification.project}</li>
          <li><strong>Branch:</strong> {notification.branch}</li>
          <li><strong>Commit:</strong> {notification.commit} </li>
          <li><strong>Authors:</strong> {", ".join(notification.author) } </li>
          <li><strong>Build Status:</strong> {notification.status} </li>
          {f"<li><strong>Build Output:</strong> {notification.output} </li>"}
          {f"<li><strong>Build Timestamp:</strong> {notification.timestamp} </li>" if notification.timestamp else ""} 
        </ul>        
      </body>
    </html>
    """
