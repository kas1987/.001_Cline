#!/usr/bin/env python3
"""Repo validator for .001_Cline.

Quality gate enforced in CI (see .github/workflows/validate.yml).
Checks:
  1. Required governance files exist.
  2. No secret-looking strings are committed.
  3. Markdown files are non-empty and have a top-level heading.
  4. No merge-conflict markers anywhere.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "LICENSE",
    "CODEOWNERS",
    "REPO_STATUS.md",
    ".clinerules/01-workflow.md",
    ".github/workflows/validate.yml",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
]

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{36,}"),
    re.compile(r"gho_[A-Za-z0-9]{36,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]

MERGE_MARKER = re.compile(r"^(<{7}|={7}|>{7}) ", re.MULTILINE)

SKIP_DIRS = {".git", "node_modules", "__pycache__", "_Per_Cline_Chat"}
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".json", ".py", ".toml", ".cfg", ".txt", ".gitignore", ""}


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO_ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.name in {".gitignore", ".gitattributes", ".editorconfig", "CODEOWNERS"} or path.suffix in TEXT_SUFFIXES:
            files.append(path)
    return files


def main() -> int:
    errors: list[str] = []

    # 1. Required files
    for rel in REQUIRED_FILES:
        if not (REPO_ROOT / rel).is_file():
            errors.append(f"Missing required file: {rel}")

    # 2-4. Content scans
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue  # binary or unreadable: skip
        rel = path.relative_to(REPO_ROOT).as_posix()

        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"Possible secret in {rel}: matches {pattern.pattern!r}")

        if MERGE_MARKER.search(text):
            errors.append(f"Merge-conflict marker found in {rel}")

        if path.suffix == ".md":
            stripped = text.strip()
            if not stripped:
                errors.append(f"Empty markdown file: {rel}")
            elif not stripped.startswith("#"):
                errors.append(f"Markdown file missing top-level heading: {rel}")

    if errors:
        print(f"FAIL: {len(errors)} problem(s) found:\n")
        for err in errors:
            print(f"  - {err}")
        return 1

    count = len(iter_text_files())
    print(f"OK: all required files present, {count} text files scanned, no secrets or conflict markers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
