import os
from fastapi_mail import (
    ConnectionConfig,
    FastMail,
    MessageSchema,
    MessageType
)
from pydantic import BaseModel

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
    author: str
    branch: str
    commit: str
    project: str
    status: str
    timestamp: str | None = None


async def send_notification(notification: Notification):
    message = MessageSchema(
        subject=prepare_subject(notification),
        recipients=[fast_mail.config.MAIL_FROM],
        body=prepare_body(notification),
        subtype=MessageType.html
    )
    await fast_mail.send_message(message)


def prepare_subject(notification: Notification):
    return f"[CI Notification] Build {notification.status} for commit {notification.commit} on branch {notification.branch}"


def prepare_body(notification: Notification):
    return f"""
    <html>
      <body>
        <p>Automated notification from Group 18 CI server.</p>

        <h3>Build Details:</h3>
        <ul>
          <li><strong>Project:</strong> {notification.project}</li>
          <li><strong>Branch:</strong> {notification.branch}</li>
          <li><strong>Commit:</strong> {notification.commit} </li>
          <li><strong>Author:</strong> {notification.author} </li>
          <li><strong>Build Status:</strong> {notification.status} </li>
          {f"<li><strong>Build Timestamp:</strong> {notification.timestamp} </li>" if notification.timestamp else ""} 
        </ul>        
      </body>
    </html>
    """
