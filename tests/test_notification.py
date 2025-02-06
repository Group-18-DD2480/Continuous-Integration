import pytest
from pydantic import ValidationError

from src.notification import fast_mail, prepare_subject, send_notification, Notification


# Ensure send_notification() sends the notification email successfully to the specified address.
@pytest.mark.asyncio
async def test_send_notification():
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as captured_messages:
        notification = Notification(**{
            "author": "Test-Author",
            "branch": "Test-Branch",
            "commit": "Test-Commit",
            "project": "Test-Project",
            "status": "Success",
        })
        await send_notification(notification)
        assert len(captured_messages) == 1
        captured_message = captured_messages[0]
        assert captured_message["To"] == fast_mail.config.MAIL_FROM
        assert captured_message["subject"] == prepare_subject(notification)


# Ensure send_notification() raises ValidationError given missing commit information.
@pytest.mark.asyncio
async def test_send_notification_missing_commit_data():
    fast_mail.config.SUPPRESS_SEND = 1
    with pytest.raises(ValidationError):
        notification = Notification(**{
            "author": "Test-Author",
            "branch": "Test-Branch"
        })
        await send_notification(notification)
