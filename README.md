# Continuous-Integration

## Notification
Notification system for the CI server has been implemented using `fastapi_mail` Python package, enabling automated email notifications containing build details. The `Notification` BaseModel defines information included in each notification. 
```python
class Notification(BaseModel):
    author: str
    branch: str
    commit: str
    project: str
    status: str
    timestamp: str | None = None
```
Notifications are sent using a `FastMail` instance configured with environment variables specified as in `.env.example`. On `send_notification()` method call, subject and content of the emails are generated dynamically and sent asynchronously to the specified recipient. For demonstration purposes, the recipient has been configured as the sender email.
```python
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
```


### Tests
Notification system has been unit tested using the `pytest` package by mocking a sample mailbox, capturing the messages and verifying whether the notifications are successfully sent. Email dispatch is suppressed during unit tests, ensuring that no actual messages are sent. Furthermore, type error handling tests have been implemented, validating whether appropriate exceptions are raised if the notification is missing required information.

## Contribution Style

Contributions to the repository should follow the structure outlined below.

### **Prefixes**

Use one of the following prefixes to categorize the changes:

- `feat` – Adding a new feature
- `fix` – Fixing a bug
- `doc` – Writing documentation
- `refactor` – Improving existing code

### **Commit Messages**  

Commit messages should follow the format:  

```  
[prefix] Commit message (#PR)  
```  

Relevant issue numbers should be included in the squashed commit description.  

### **Pull Requests**

Pull request titles should follow the prefix structure:

```
[prefix] PR title
```

All relevant issues should be linked in the description of the PR.

### **Merge Strategy**

Use **Squash and Merge** policy and ensure the final commit message follows the correct format before merging.

### Code Review

Reviever of the Pull Request is responsible for the merger.

## License

This project is licensed under MIT License. See `LICENSE` for details.
