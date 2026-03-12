---
inclusion: manual
---
# Sonarqube Work

This skill uses a sonarqube jira story to work through all the issues.

## Parameters

- `jira_ticket`: Ticket describing which sonarqube issues to fix. Eg:- EA-XXXXX
- `repo` : The repository/module name where changes have to be made

## Steps
1. I need you to fix all SonarQube code quality issues for listed in the ticket EA-XXXXX. Only fix the issues listed in the ticket and nothing more. 

2. Navigate to the local directory or ask user to navigate to that directory in the terminal

3. Create a new git branch named after the Jira ticket number (e.g., ea-XXXXX) from master (after making sure master is up to date) in the given repo.

4. Fix all the issues systematically:
   - Start with BLOCKER, then CRITICAL, then MAJOR
   - For each fix, verify it doesn't break compilation or change behavior
   - Verify that only non logic mechanical issues are fixed

5. After all fixes, run `mvn clean install` to verify: compilation, all unit tests pass, checkstyle passes, no dependency issues. Fix any compilation errors or test failures before proceeding.

6. Commit all changes, push the branch, and create a PR on GitHub with a mini summary of all changes grouped by SonarQube rule. Add the label "generated_by_kiro" to the PR.

Important:
- Always run `mvn clean install` (not just compile) to catch checkstyle and other plugin issues
- Some fixes like raw types (S3740) or Guava Function (S4738) may not be possible due to library API constraints — skip those and document why
- Constructor parameter count (S107) may require API-breaking changes — skip those and document why
- Never introduce new SonarQube issues while fixing existing ones
