---
name: github-api-repository-explorer
description: Authenticate with the GitHub REST API using a GitHub Personal Access Token (PAT) and establish access to a remote GitHub repository. Use this skill whenever a task requires authenticated access to a GitHub repository.
---

# GitHub API Repository Explorer

This skill establishes an authenticated connection to a remote GitHub repository using the GitHub REST API. Before performing any repository operations, verify that the user has a valid GitHub Personal Access Token (PAT) and that the repository is accessible.

## Bundled Resources

- `scripts/github_client.py` — GitHub API client handling authentication and requests.
- `scripts/connect.py` — CLI entry point that verifies the PAT and confirms repository access.

Always use these scripts rather than crafting raw HTTP requests manually.

## Workflow

### 1. Collect the required information

- Ask the user for a GitHub repository identifier (`owner/repository`) if not already provided.
- Confirm that a `.env` file exists in the project root with a `GITHUB_TOKEN` set.
  If missing, explain that a PAT can be created at:
  `GitHub → Settings → Developer settings → Personal access tokens`
  and should be placed in `.env` as `GITHUB_TOKEN=<token>` — never pasted into the chat.

### 2. Authenticate and connect to the repository

Run the connection script:

    python scripts/connect.py --repo <owner>/<repository>

The script reads `GITHUB_TOKEN` from a `.env` file in the project root, authenticates
with the GitHub REST API, and verifies access to the specified repository.

Never ask the token from the user directly into the conversation, log it, or display it — 
the script reads it from `.env` on its own.

Interpret the script's output:
- Output starting with `✅` — authentication and repository access succeeded. Proceed with subsequent operations.
- Output starting with `❌ Помилка підключення` — the PAT is missing, invalid, expired, or the repository is inaccessible. Show the message to the user and ask them to check their `.env` / PAT before continuing.
- Any other error — surface the message and stop the workflow.

Do not continue until the script reports success.

### 3. Completion

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