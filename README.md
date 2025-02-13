# Continuous-Integration

## API Documentation

You can view the API documentation hosted on GitHub Pages here:

[CI API Documentation](https://group-18-dd2480.github.io/Continuous-Integration/)

### Webhook Implementation
- The CI server is implemented using FastAPI.
- A webhook triggers syntax checks whenever a push event occurs.

### CI Compilation (Static Syntax Check)

1. When a push event occurs, a webhook triggers the CI server.
2. The CI server pulls the latest code from the repository.
3. It runs `flake8` to perform a static syntax check.
4. The output is displayed in the CI server logs.

#### Running Locally
To test the CI locally:
```bash
uvicorn compilation:app --host 0.0.0.0 --port 8000
```

### Notification
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


#### Tests
Notification system has been unit tested using the `pytest` package by mocking a sample mailbox, capturing the messages and verifying whether the notifications are successfully sent. Email dispatch is suppressed during unit tests, ensuring that no actual messages are sent. Furthermore, type error handling tests have been implemented, validating whether appropriate exceptions are raised if the notification is missing required information.

This CI server automates compilation, testing, and notifications for project changes.

### Workflow
1. A webhook triggers compilation (`/compile`).
2. On success, tests run (`/test`).
3. Results are emailed via `/notify`.

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
