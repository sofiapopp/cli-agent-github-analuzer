---
name: github-repo-analyzer
description: GitHub repository analysis and reporting. Use this skill when the user wants to analyze a GitHub repository, understand its architecture, identify the technologies it uses, evaluate its strengths and weaknesses, generate improvement recommendations, or produce a repository analysis report. Trigger on requests such as "analyze this repository", "review this project", "summarize the codebase", "identify the technologies", "generate a repository report", "assess the project structure", or any task requiring repository-level analysis of repo.
---

# GitHub Repository Analysis and Reporting

## Constraints

- Perform the analysis exclusively using the repository context acquired in Step 1.
- Do not retrieve additional repository data unless the available context is insufficient to complete the requested analysis.
- Do not modify the repository, its files, branches, or settings.
- Generate exactly two output files:
  - `output/report.md`
  - `output/analysis.json`
- Create the `output` directory only if it does not already exist.
- Ensure the Markdown report and JSON output are consistent and describe the same analysis results.

## Analysis Rules

- Base every conclusion on evidence found in the repository context.
- Do not speculate about files, technologies, or architecture that are not present.
- If information is insufficient, explicitly state that it could not be determined.
- Distinguish confirmed findings from recommendations.

## Workflow

Copy this checklist and track your progress

- [ ] **Step 1: Acquire Repository Context**
- [ ] **Step 2: Analyze the Repository**
- [ ] **Step 3: Generate the Analysis Report**
- [ ] **Step 4: Generate Structured Output**
- [ ] **Step 5: Save Results**


### Step 1. Acquire Repository Context

  1. Ensure the repository context is available.

  2. If the repository context is not available, invoke the `github-repo-explorer` skill to retrieve:
    - repository metadata;
    - repository structure;
    - the complete file list.

  3. Identify the files required for repository-level analysis. Prioritize files that describe the project, its dependencies, configuration, build process, or entry points. Typical examples include:
    - `README.md`
    - `LICENSE`
    - `.gitignore`
    - dependency manifests (e.g. `package.json`, `requirements.txt`, `pom.xml`, `Cargo.toml`, `go.mod`)
    - build and configuration files (e.g. `Dockerfile`, `docker-compose.yml`, `Makefile`, `CMakeLists.txt`)
    - CI/CD configuration (e.g. `.github/workflows/*`)
    - project configuration files (e.g. `tsconfig.json`, `pyproject.toml`, `composer.json`)
    - application entry points (e.g. `main.*`, `index.*`, `app.*`, `Program.cs`)

  4. Retrieve the contents of only the selected files. Avoid retrieving the contents of the entire repository unless explicitly requested by the user.

  5. Verify that the repository context includes:
    - the repository structure;
    - the complete file list;
    - the contents of the selected files.

  6. Continue to the next step only after the required repository context has been acquired.

### Step 2. Analyze the Repository

1. Analyze the repository using the acquired context.

2. Describe the overall project structure.

3. Identify the primary technologies, programming languages, frameworks, libraries, build tools, and package managers used in the repository.

4. Identify the repository's strengths, including positive aspects of its organization, architecture, documentation, or implementation.

5. Identify potential issues or areas for improvement, including maintainability, readability, scalability, reliability, consistency, documentation, configuration, dependency management, or project organization.

6. Provide actionable recommendations that address the identified issues.

7. Preserve all analysis results for the report generation and structured output steps.

### Step 3. Generate the Analysis Report

1. Generate a Markdown report based on the analysis results from Step 2.

2. Structure the report using the following sections, in order:
   - Repository Overview
   - Project Structure
   - Technologies
   - Strengths
   - Potential Issues
   - Recommendations

3. Ensure each section contains concise, evidence-based findings derived from the repository analysis.

4. Preserve the generated report for the output step.

### Step 4. Generate Structured Output

1. Generate a structured JSON object based on the analysis results from Step 2.

2. Use the following structure:

```json
{
  "summary": "",
  "technologies": [],
  "strengths": [],
  "issues": [],
  "recommendations": []
}
```
3. Ensure the JSON is valid and contains only the analysis results without additional commentary.

4. Preserve the generated JSON for the output step.


### Step 5. Save Results

1. Create the `output/` directory if it does not already exist.

2. Save the generated Markdown report as:
   - `output/report.md`

3. Save the generated structured JSON as:
   - `output/analysis.json`

4. Confirm that both files have been created successfully.


