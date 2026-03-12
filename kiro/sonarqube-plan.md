---
inclusion: manual
---

# Sonarqube Plan

This skill fetches all non logic changing issues from SonarQube for a repository and create a jira story to fix those issues

## Parameters

- <SONARQUBE_PROJECT_KEY>: e.g. "remediation-ui"
- <REPO_NAME>: e.g. "remediation-ui"
- <EPIC_KEY>: e.g. "EA-24631"

## Steps
1. Connect to SonarQube and fetch all mechanical (non-logic-affecting) BLOCKER, CRITICAL, and MAJOR issues for the project key `<SONARQUBE_PROJECT_KEY>` (use the SonarQube API at https://sonarqube.build.r7ops.com with token from MCP config).

2. Create a Jira type "Story" in project key "EA" with:
   - Summary: "[<REPO_NAME>] Fix all BLOCKER, CRITICAL, and MAJOR SonarQube issues in <REPO_NAME> to achieve Maintainability Rating A"
   - Description: List all issues grouped by severity (BLOCKER, CRITICAL, MAJOR), with full file paths, line numbers, rule IDs, and issue messages
   - Conditions of Satisfaction (customfield_10104):
     1. All BLOCKER, CRITICAL, and MAJOR SonarQube issues are resolved
     2. SonarQube Maintainability Rating reaches A on new code
     3. All existing unit and integration tests continue to pass
   - Team(s) (customfield_10108): Aard-Mind-Muggles (id: 18284)
   - Epic Link (customfield_10014): <EPIC_KEY>
   - Label: generated_by_kiro
