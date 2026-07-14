# GitHub Repository Analysis Skills

A collection of Gemini CLI skills for accessing, exploring, and analyzing remote GitHub repositories through the GitHub REST API. The skills work together to retrieve repository context, analyze project structure, identify technologies, generate recommendations, and produce structured reports without requiring a local repository clone.

---

## Features

- Authenticate with GitHub using a Personal Access Token (PAT)
- Access remote GitHub repositories through the GitHub REST API
- Retrieve repository metadata, directory structure, and file contents
- Analyze repository architecture and organization
- Identify programming languages, frameworks, libraries, and build tools
- Detect strengths and potential issues
- Generate actionable improvement recommendations
- Produce Markdown and JSON analysis reports

---

## Skills

### github-repo-explorer

Retrieves repository information directly from the GitHub REST API.

**Responsibilities**

- Authenticate with GitHub
- Connect to a remote repository
- Retrieve repository metadata
- Retrieve the complete repository structure
- Retrieve file contents on demand
- Provide repository context for subsequent analysis

---

### github-repo-analyzer

Analyzes the repository context and generates reports.

**Responsibilities**

- Analyze the repository structure
- Identify technologies and project organization
- Detect strengths and potential issues
- Generate improvement recommendations
- Produce a Markdown report
- Produce structured JSON output

---

## Requirements

- Gemini CLI
- GitHub Personal Access Token (PAT)
- Internet connection
- GitHub REST API access

---

## Installation

Copy the skills into your Gemini CLI skills directory.

```text
.agent/
└── skills/
    ├── github-repo-explorer/
    │   └── SKILL.md
    └── github-repo-analyzer/
        └── SKILL.md
```

---

## Configuration

Configure a GitHub Personal Access Token before using the skills.

Environment variable:

```text
GITHUB_TOKEN
```

---

## Usage

Example requests:

```text
Analyze this repository

Show the repository structure

Read README.md

Identify the technologies used in this repository

Generate a repository analysis report
```

---

## Workflow

```text
User Request
      │
      ▼
github-repo-explorer
      │
Retrieve repository context
      │
      ▼
github-repo-analyzer
      │
Analyze repository
      │
      ▼
Generate report.md + analysis.json
```

---

## Output

The analyzer generates the following files inside the `output` directory:

```text
output/
├── report_<repository>.md
└── analysis_<repository>.json
```

---

## Limitations

- Repository access is read-only.
- Repository data is retrieved exclusively through the GitHub REST API.
- A valid GitHub Personal Access Token is required.
- The analyzer only evaluates the repository context that has been retrieved.
- Conclusions are based solely on the available repository evidence.
