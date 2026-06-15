---
name: Edit Code
description: Make targeted, minimal edits to source files to implement a change or fix a bug.
---

Use this skill after reading the relevant code with `read-codebase` and confirming the approach with the user.

**Steps**
1. Confirm the exact change with the user before writing anything.
2. Follow the conventions in `references/conventions.md`.
3. Make the smallest edit that achieves the goal — do not refactor surrounding code unless asked.
4. After editing, run the test suite with the `run-tests` skill to confirm nothing is broken.
5. Show the user a diff of what changed.

**Safety rules**
- Never delete files without explicit user confirmation.
- Never modify lock files (`package-lock.json`, `uv.lock`, etc.) directly.
- Never commit changes — leave that to the user.
