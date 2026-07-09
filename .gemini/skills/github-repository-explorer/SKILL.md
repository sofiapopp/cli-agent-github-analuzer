---
name: github-api-repository-explorer
description: Authenticate with the GitHub REST API using a GitHub Personal Access Token (PAT) and establish access to a remote GitHub repository. Use this skill whenever a task requires authenticated access to a GitHub repository.
---

# GitHub API Repository Explorer

This skill establishes an authenticated connection to a remote GitHub repository using the GitHub REST API. Before performing any repository operations, verify that the user has a valid GitHub Personal Access Token (PAT) and that the repository is accessible.

## Workflow

### 1. Collect the required information

Before making any GitHub API request:

- Ask the user for a GitHub repository URL or an `owner/repository` identifier if it has not already been provided.
- Check whether a GitHub Personal Access Token (PAT) has already been provided.
- If no PAT is available, ask the user to generate one.

Explain that a PAT can be created in:

`GitHub → Settings → Developer settings → Personal access tokens`

Recommend creating a token with the minimum permissions required to read repository contents.

### 2. Authenticate with the GitHub REST API

Use the provided PAT to authenticate every GitHub API request.

Include the following HTTP headers:

```
Authorization: Bearer <PAT>
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
```

Never display, log, or permanently store the Personal Access Token.

### 3. Validate the Personal Access Token

Before accessing the repository, verify that the PAT is valid.

Send an authenticated request to:

```
GET https://api.github.com/user
```

Interpret the response as follows:

- HTTP 200 — authentication succeeded.
- HTTP 401 — the PAT is invalid or expired. Ask the user to provide a valid token before continuing.
- HTTP 403 — access is forbidden or the GitHub API rate limit has been reached. Explain the reason and stop the workflow.

Do not continue unless authentication succeeds.

### 4. Connect to the repository

Extract the repository owner and repository name from the user input.

Verify that the repository is accessible by sending an authenticated request to:

```
GET https://api.github.com/repos/{owner}/{repository}
```

Interpret the response as follows:

- HTTP 200 — the repository exists and is accessible.
- HTTP 404 — the repository does not exist or the authenticated user does not have permission to access it.
- HTTP 403 — access is forbidden or rate limits have been exceeded.

Continue only after successfully verifying repository access.

### 5. Completion

When authentication and repository access have both been verified:

- Inform the user that the connection to the repository has been established successfully.
- Confirm that the repository is ready for subsequent GitHub API operations.

## Error Handling

Handle the following situations gracefully:

- Missing Personal Access Token.
- Invalid or expired Personal Access Token.
- Authentication failure.
- Repository not found.
- Insufficient repository permissions.
- GitHub API rate limiting.
- Network or API connectivity errors.

Always explain the reason for the failure and clearly describe the next action required from the user.

## Expected Behaviour

The AI agent must perform all repository access through authenticated GitHub REST API requests.

Do not inspect the local file system or rely on a locally cloned repository unless the user explicitly requests local repository analysis.