# Continuous-Integration

# CI Compilation (Static Syntax Check)

## Webhook Implementation
- The CI server is implemented using FastAPI.
- A webhook triggers syntax checks whenever a push event occurs.

## How Compilation Works
1. When a push event occurs, a webhook triggers the CI server.
2. The CI server pulls the latest code from the repository.
3. It runs `flake8` to perform a static syntax check.
4. The output is displayed in the CI server logs.

## Running Locally
To test the CI locally:
```bash
uvicorn compilation:app --host 0.0.0.0 --port 8000

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
