---
name: Run Tests
description: Execute the project test suite and interpret pass/fail results.
---

Use this skill after making code changes, or when the user asks about test status.

**Steps**
1. Run `scripts/run_tests.sh` from the project root.
2. If all tests pass, report the count and confirm the change is safe.
3. If tests fail, show the failing test names and error messages.
4. Diagnose the failures — determine whether they were caused by your change or were pre-existing.
5. If caused by your change, revert or fix before reporting back.

**Script:** `scripts/run_tests.sh`
