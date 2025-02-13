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
python src/app.py
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

## Dependencies

- **Python** 3.13
- **FastAPI**: Modern web framework for building APIs with Python
- **Uvicorn**: ASGI server implementation, used to run the FastAPI application
- **python-dotenv**: Loads environment variables from .env files
- **Pydantic**: Data validation using Python type annotations
- **GitPython**: Git repository interaction from Python
- **fastapi-mail**: Email handling and sending functionality for FastAPI
- **flake8**: Static code analysis and style checker
- **pytest**: Testing framework
- **pytest-asyncio**: Pytest plugin for testing async code
- **httpx**: HTTP client used by FastAPI's TestClient
- **fastapi.testclient**: Testing client for FastAPI applications

## Statement of Contributions

#### [@AlessandroColi](https://github.com/AlessandroColi) - Alessandro Coli

- [doc] Create GitHub issues for the project.
- [doc] Documentation API and contributions in `README.md`.
- [doc] Add html file for API documentation
- [doc] Add github page for API documentation


#### [@eliasfloreteng](https://github.com/eliasfloreteng) - Elias Floreteng

- [doc] Create GitHub issues for the project.
- [feat] Add GitHub webhook endpoint.
- [feat] Add `testing.py.
- [refactor] Remove duplicate FastAPI server


#### [@laykos0](https://github.com/laykos0) - Jakub Rybak

- [doc] Create `README.md` with contribution style and license sections
- [feat] add Skeleton Code for FastAPI.
- [feat] Add `notification.py`.
- [feat] Add tests for `notification.py`.
- [doc] Add documentation of `notification.py`.


#### [@RuriThomas](https://github.com/RuriThomas) - Ruri Osmon
- [feat] create public url with ngrok 
- [feat] add public webhook to repo

#### [@YusufDemir1210](https://github.com/YusufDemir1210) - Yusuf Demir
- [feat] Add `compilation.py`.
- [feat] Add tests for `compilation.py`.
- [doc] Add documentation of `compilation.py`.

### Way of working & Essence checklist

Our team's way of working is now at the "In Place" state according to the Essence framework. We have established clear principles for collaboration including standardized commit message and PR formats, code review processes, and GitHub Actions for running the tests on each commit. Our practices and tools are actively being used for real work, with regular inspections through pull requests and code reviews. The team has adapted practices to fit our context, such as using GitHub issues, PRs and maintaining clear documentation. These practices have now been used by all group members to perform their work. We are continuously improving our way of working and discussing it during meetings. Communication and collaboration are done through WhatsApp, Discord and issue comments.