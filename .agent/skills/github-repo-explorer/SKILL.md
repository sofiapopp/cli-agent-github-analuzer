---
name: github-repo-explorer
description: GitHub repository access and content retrieval via PowerShell. Use this skill whenever the user needs to access or explore a remote GitHub repository, browse its directory structure, list files, retrieve file contents, or inspect repository metadata. Trigger on requests like "show the repository structure", "list all files in this repo", "read a file from GitHub", "browse a repository", "explore a GitHub project", "get the contents of a file", or any task requiring programmatic access to a remote GitHub repository. Requires a Windows PowerShell environment with a GITHUB_TOKEN environment variable configured.
---

# GitHub Repository Access and Content Retrieval

**Environment requirement:** this skill is written exclusively for **Windows PowerShell**. It relies on `Invoke-RestMethod` and PowerShell-native syntax, and explicitly forbids `curl`, `wget`, `jq`, and `base64`. Do not run this skill in a Linux/bash environment — it will not work there.

## Error Handling (strict)

If any command, API request, or step returns an error, a status code ≥ 400, or a command failure, you MUST:

1. Stop **all** further execution immediately.
2. Print the exact error message received to the user.
3. Do **not** attempt self-correction, debugging, or custom scripts.
4. Wait for user input.

## Standard PowerShell API Template

For all GitHub API requests, strictly use this exact pattern:

```powershell
$headers = @{
    "Authorization" = "Bearer $env:GITHUB_TOKEN"
    "Accept"        = "application/vnd.github+json"
}
$response = Invoke-RestMethod -Uri "<API_URL>" -Headers $headers -Method Get
```

## Workflow

### Step 1 — Authenticate with GitHub

1. Read the GitHub Personal Access Token (PAT) from the `GITHUB_TOKEN` environment variable:

   ```powershell
   if (-not $env:GITHUB_TOKEN) {
       Write-Error "GITHUB_TOKEN is not set. Please configure it."
       return
   }
   ```

2. If `GITHUB_TOKEN` is not set or is empty, instruct the user to configure it, then **stop skill execution**.

3. Include the following headers in every API request:
   - `Authorization: Bearer $GITHUB_TOKEN`
   - `Accept: application/vnd.github+json`

   ```powershell
   $headers = @{
       "Authorization" = "Bearer $env:GITHUB_TOKEN"
       "Accept"        = "application/vnd.github+json"
   }
   $authCheck = Invoke-RestMethod -Uri "https://api.github.com/rate_limit" -Headers $headers -Method Get
   ```

4. Validate authentication with an HTTP GET request to `https://api.github.com/rate_limit`.

5. Interpret the HTTP response status code:
   - `200` → authentication succeeded; continue to the next step.
   - `401` → the token is invalid or expired.
   - `403` → check the `X-RateLimit-Remaining` header before treating the response as an authentication failure.

6. If authentication fails, report the specific error, instruct the user to provide a valid token, then **stop skill execution**.

7. **Security rule:** never expose the PAT. Do not print or log it, do not leak the `Authorization` header, do not write it to files, and do not include it in error messages.

### Step 2 — Connect to the Repository

1. Determine `OWNER` and `REPO` from the user's request. Accept the repository as:
   - a GitHub repository URL (e.g. `https://github.com/OWNER/REPO`, optionally with a trailing `.git` or `/`);
   - an `OWNER/REPO` identifier.

   When parsing a URL, strip any trailing `.git` suffix and trailing slashes before extracting `OWNER` and `REPO`.

   If the repository cannot be determined, ask the user to provide a valid GitHub repository and stop skill execution.

2. Request repository metadata:

   ```powershell
   $repoData = Invoke-RestMethod -Uri "https://api.github.com/repos/$OWNER/$REPO" -Headers $headers -Method Get
   $DEFAULT_BRANCH = $repoData.default_branch
   ```

3. Handle the response:
   - `200` → store the repository owner, name, and `default_branch` for use in subsequent steps.
   - `404` → inform the user that the repository does not exist or is not accessible, then stop.
   - `403` → inform the user that current credentials lack permission, then stop.
   - Other non-2xx → report that the API is unreachable or returned an error, then stop.

### Step 3 — Retrieve the Repository Structure

1. Request the complete repository tree using the default branch obtained in Step 2:

   ```powershell
   $treeData = Invoke-RestMethod -Uri "https://api.github.com/repos/$OWNER/$REPO/git/trees/$DEFAULT_BRANCH?recursive=1" -Headers $headers -Method Get
   ```

2. If the request fails (non-2xx), report the error and stop.

3. Parse the JSON response:
   - Check the `truncated` field. If `true`, warn the user that the repository exceeds the API size limit and the structure may be incomplete.
   - Iterate through the `tree` array and extract `path`, `type` (`blob` = file, `tree` = directory), and `sha`.

4. Preserve the repository hierarchy and store the parsed structure in memory.

### Step 4 — Display the Repository Structure

1. Format the stored tree as an indented directory structure — directories listed before files, sorted alphabetically within each level. Use standard ASCII characters (`|--`, `\--`) for drawing the tree to avoid console encoding issues.
2. Print the formatted structure to the console.
3. Additionally, output all files (`type: blob`) as a flat list of paths. This flat list is the input for any subsequent file-content retrieval tasks.

### Step 5 — Retrieve File Contents

Perform this step only if the user explicitly requests file contents, or if they are required to complete the current task.

1. Determine the file(s) to retrieve.

2. Make an HTTP GET request to the Contents API:

   ```powershell
   $fileResponse = Invoke-RestMethod -Uri "https://api.github.com/repos/$OWNER/$REPO/contents/$FILE_PATH?ref=$DEFAULT_BRANCH" -Headers $headers -Method Get
   ```

3. Parse the JSON response:
   - If successful (`200`), extract the `content` string, remove any whitespace characters, and decode it from Base64 to plain text.
   - If `encoding` is `"none"` (file exceeds the 1MB limit), fall back to the Git Blobs API using the file's `sha` from Step 3:

     ```powershell
     $fileResponse = Invoke-RestMethod -Uri "https://api.github.com/repos/$OWNER/$REPO/git/blobs/$FILE_SHA" -Headers $headers -Method Get
     ```

4. To decode the `content` field from the API response, strictly use this PowerShell snippet:

   ```powershell
   $cleanBase64 = $fileResponse.content -replace '\s', ''
   $decodedText = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($cleanBase64))
   Write-Host $decodedText
   ```

5. If the file is not found (`404`), report that the path does not exist and skip it (continue with other requested files).
6. For any other failure (`401`, `403`, `5xx`), report the error and stop.
7. Make all successfully retrieved file contents available for subsequent tasks.

## Constraints

- **No file creation:** you are strictly forbidden from creating, writing, or editing any files on the local filesystem (including `.ps1`, `.py`, `.sh`, `.txt` files). Perform all operations directly in the console. If an operation cannot be performed directly in the console, report it as an error and stop.
- **No command substitution:** never use command substitution (e.g. `$(...)`). Execute commands directly.
- **Environment:** you are executing in Windows PowerShell.
- **Forbidden tools:** never use `curl`, `wget`, `jq`, `tr`, `base64`, or bash command substitution.
- **Native PowerShell only:** you must use `Invoke-RestMethod` for API requests. Do not attempt to pipe (`|`) raw text between external utilities.
- **No auto-debugging or workarounds:** if any command, API request, or step fails, you must immediately stop skill execution. It is strictly forbidden to attempt self-correction, write custom helper scripts (PowerShell, Python, etc.), or try alternative commands to bypass the error. Report the exact error message to the user and halt completely.
- Access repository data only through the GitHub REST API.
- Never send `POST`, `PUT`, `PATCH`, or `DELETE` requests to the GitHub API.
- Never create, modify, or delete files, branches, or repository settings.
- Never access a local clone or local filesystem.
- If the user specifies a branch, tag, or commit SHA, use it instead of `default_branch` for all subsequent requests.
- Before displaying decoded content, check the file extension or the presence of null bytes in the decoded output. If the file appears to be binary (image, archive, compiled artifact, etc.), report its size and type instead of printing raw content.