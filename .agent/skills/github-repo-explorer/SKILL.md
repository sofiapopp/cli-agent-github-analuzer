---
name: github-repo-explorer
description: GitHub repository access and content retrieval via PowerShell. Use this skill whenever the user needs to access or explore a remote GitHub repository, browse its directory structure, list files, retrieve file contents, or inspect repository metadata. Trigger on requests like "show the repository structure", "list all files in this repo", "read a file from GitHub", "browse a repository", "explore a GitHub project", "get the contents of a file", or any task requiring programmatic access to a remote GitHub repository. Requires a Windows PowerShell environment with a GITHUB_TOKEN environment variable configured.
---

# GitHub Repository Access and Content Retrieval

**Environment requirement:** this skill is written exclusively for **Windows PowerShell**. It relies on `Invoke-RestMethod` and PowerShell-native syntax, and explicitly forbids `curl`, `wget`, `jq`. Do not run this skill in a Linux/bash environment — it will not work there.

## Constraints
- **No file creation:** you are strictly forbidden from creating, writing, or editing any files on the local filesystem (including `.ps1`, `.py`, `.sh`, `.txt` files). Perform all operations directly in the console. If an operation cannot be performed directly in the console, report it as an error and stop.
- **No command substitution:** never use command substitution (e.g. `$(...)`). Execute commands directly.
- **Environment:** you are executing in Windows PowerShell.
- **Forbidden tools:** never use `curl`, `wget`, `jq`, `tr`, or bash command substitution.
- **Native PowerShell only:** You must strictly execute only the PowerShell commands and workflows explicitly defined in this skill document. Do not attempt to pipe (`|`) raw text between external utilities.
- **No auto-debugging or workarounds:** if any command, API request, or step fails, you must immediately stop skill execution. It is strictly forbidden to attempt self-correction, write custom helper scripts (PowerShell, Python, etc.), or try alternative commands to bypass the error. Report the exact error message to the user and halt completely.
- Access repository data only through the GitHub REST API.
- Never send `POST`, `PUT`, `PATCH`, or `DELETE` requests to the GitHub API.
- Never create, modify, or delete files, branches, or repository settings.
- Never access a local clone or local filesystem.
- If the user specifies a branch, tag, or commit SHA, use it instead of `default_branch` for all subsequent requests.
- Before displaying decoded content, check the file extension or the presence of null bytes in the decoded output. If the file appears to be binary (image, archive, compiled artifact, etc.), report its size and type instead of printing raw content.

## Error Handling (strict)

If any command, API request, or step returns an error, a status code ≥ 400, or a command failure, you MUST:

1. Stop **all** further execution immediately.
2. Print the exact error message received to the user.
3. Do **not** attempt self-correction, debugging, or custom scripts.
4. Wait for user input.

## Workflow

Copy this checklist and track your progress:

- [ ] **Step 1: Authenticate with GitHub**
- [ ] **Step 2: Connect to the Repository**
- [ ] **Step 3: Retrieve the Repository Structure**
- [ ] **Step 4: Display the Repository Structure**
- [ ] **Step 5: Perform this step only if the user explicitly requests. Retrieve File Contents**

### Step 1 — Authenticate with GitHub

Execute only the commands provided below first.

1. Read the GitHub Personal Access Token (PAT) from the `GITHUB_TOKEN` environment variable and Validate:
   Execute the following PowerShell commands:
   ```powershell
   $token = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN")

   if ([string]::IsNullOrWhiteSpace($token)) {
      Write-Error "GITHUB_TOKEN is not set or is empty. Please configure it."
      return
   }
   ```
   If the command reports that `GITHUB_TOKEN` is missing or empty:
   - Inform the user that the GitHub Personal Access Token is not configured.
   - Ask the user to configure the `GITHUB_TOKEN` environment variable.
   - Stop skill execution.

3. Create the following HTTP headers and include them in every subsequent GitHub API request:
   Execute the following PowerShell commands:

   ```powershell
   $headers = @{
      "Authorization" = "Bearer $token"
      "Accept"        = "application/vnd.github+json"
   }
   ```
7. **Security rule:** never expose the PAT. Do not print or log it, do not leak the `Authorization` header, do not write it to files, and do not include it in error messages.

### Step 2 — Connect to the Repository


1. Accept the repository in one of the following formats:
   - a GitHub repository URL (for example, `https://github.com/OWNER/REPO`, optionally ending with `.git` or `/`);
   - an `OWNER/REPO` identifier.

2. Extract the GitHub repository owner (`OWNER`) and repository name (`REPO`) from the user's request:
   Execute the following PowerShell commands:

   ```powershell
   $inputRepo = "..." # Repository provided by the user

   $repoPath = $inputRepo `
      -replace '^https://github\.com/', '' `
      -replace '\.git$', '' `
      -replace '/$', ''

   if ($repoPath -notmatch '^[^/]+/[^/]+$') {
      Write-Error "Invalid repository format. Please provide 'OWNER/REPO' or a valid GitHub repository URL."
      return
   }

   $parts = $repoPath -split '/'
   $owner = $parts[0]
   $repo = $parts[1]
   ```

   If the repository cannot be determined or the format is invalid:
   - Inform the user that the repository could not be parsed.
   - Ask the user to provide a valid GitHub repository URL or `OWNER/REPO` identifier.
   - Stop skill execution.


3. Request repository metadata:
   Execute the following PowerShell commands:

   ```powershell
   try {
      $repoUrl = "https://api.github.com/repos/$owner/$repo"
      $repoData = Invoke-RestMethod -Uri $repoUrl -Headers $headers -Method Get -ErrorAction Stop

      # Store metadata for subsequent steps
      $global:repoOwner = $repoData.owner.login
      $global:repoName = $repoData.name
      $global:defaultBranch = $repoData.default_branch

      Write-Host "Successfully connected to: $($repoData.full_name)"
   }
   catch {
      $status = $_.Exception.Response.StatusCode.value__

      switch ($status) {
         404 { Write-Error "Repository '$owner/$repo' does not exist or is not accessible."; return }
         403 { Write-Error "Permission denied: Current credentials lack access to this repository."; return }
         Default { Write-Error "API Error ($status): The repository metadata could not be retrieved. $($_.Exception.Message)"; return }
      }
   }
   ```
   If the request fails:
   - Inform the user of the reason for the failure.
   - Stop skill execution.

   Use the following values in subsequent steps:
   - `repoOwner`
   - `repoName`
   - `defaultBranch`



### Step 3 — Retrieve the Repository Structure

1. Request the complete repository tree using the repository's default branch.

   Execute the following PowerShell commands:

   ```powershell
   try {
      $treeUrl = "https://api.github.com/repos/$global:repoOwner/$global:repoName/git/trees/$global:defaultBranch`?recursive=1"
      $treeData = Invoke-RestMethod -Uri $treeUrl -Headers $headers -Method Get -ErrorAction Stop

      # Check for truncation
      if ($treeData.truncated) {
         Write-Warning "Repository exceeds the GitHub API size limit. The structure may be incomplete."
      }

      # Store the structure in memory
      $global:repoStructure = $treeData.tree | Select-Object path, type, sha

      Write-Host "Successfully retrieved structure for $($global:repoName)."
   }
   catch {
      Write-Error "Failed to retrieve repository tree: $($_.Exception.Message)"
      return
   }
   ```
   If the request succeeds:
   - Check the `truncated` field. If it is `true`, inform the user that the repository exceeds the GitHub API size limit and the returned structure may be incomplete.
   - Preserve the repository hierarchy.
   - Store the parsed repository structure for subsequent steps.

   If the request fails:
   - Inform the user of the reason for the failure.
   - Stop skill execution.

### Step 4 — Display the Repository Structure

1. Display the repository structure in a tree-like format using ASCII characters (`|--`, `\--`) for drawing the tree to avoid 
console encoding issues.
   The tree is a presentation format only.
   Do not generate custom tree-building algorithms, recursive data structures, nested hashtables, or helper scripts.
   Use only the paths already returned by the GitHub API and format them for display.

2. Print the formatted structure to the console.

3. Additionally, output all files (`type: blob`) as a flat list of paths. This flat list is the input for any subsequent file-content retrieval tasks.

### Step 5 — Retrieve File Contents

Perform this step only if the user explicitly requests file contents or if they are required to complete the current task.

Determine the file(s) to retrieve.

Execute the following PowerShell commands:

```powershell
function Get-FileContent($filePath) {
    try {
        $apiUrl = "https://api.github.com/repos/$global:repoOwner/$global:repoName/contents/$filePath"
        $fileData = Invoke-RestMethod -Uri $apiUrl -Headers $headers -Method Get -ErrorAction Stop

        # Handle files exceeding the Contents API size limit
        if ($fileData.encoding -eq "none") {
            $blobData = Invoke-RestMethod -Uri $fileData.git_url -Headers $headers -Method Get -ErrorAction Stop
            $rawContent = $blobData.content
        }
        else {
            $rawContent = $fileData.content
        }

        # Decode Base64 content
        $bytes = [System.Convert]::FromBase64String(($rawContent -replace '\s', ''))
        return [System.Text.Encoding]::UTF8.GetString($bytes)
    }
    catch {
        $status = $_.Exception.Response.StatusCode.value__

        if ($status -eq 404) {
            Write-Error "Path '$filePath' does not exist."
            return $null
        }

        Write-Error "Failed to retrieve '$filePath': $($_.Exception.Message)"
        return $null
    }
}
```

If the request succeeds:
- Decode the `content` field from Base64 to plain text.
- If `encoding` is `none`, retrieve the file content using the Git Blobs API.
- Make the retrieved file contents available for subsequent tasks.

If a file is not found (`404`):
- Inform the user that the specified path does not exist.
- Skip the file and continue processing any remaining requested files.

If any other request fails (`401`, `403`, `5xx`, or another unexpected error):
- Inform the user of the reason for the failure.
- Stop skill execution.

