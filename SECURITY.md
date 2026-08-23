# Security Policy

## Supported

The `main` branch is the only supported branch.

## Reporting

Do **not** open a public issue for security vulnerabilities.

- Use GitHub's private vulnerability reporting on this repository, or
- Contact the owner via the email on the GitHub profile (@kas1987).

## Scope

This repository contains configuration, rules, and documentation for Cline. It should never
contain credentials, API tokens, or personal secrets. CI (`scripts/validate_repo.py`) scans
for common secret patterns on every PR and push — a failed secret scan blocks merge.
