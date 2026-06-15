---
name: Update Harness
description: Iteratively improve an existing harness by refining skills, references, and HARNESS.md based on feedback or new requirements.
---

Use this skill when the user wants to improve, extend, or restructure an existing harness. This is an ongoing process — expect multiple rounds.

## Process

### Step 1 — Read the current harness

Before making any changes, fully read the harness:

1. Read `HARNESS.md` — understand the agent's current role and what skills and references are declared.
2. Read every `skills/<name>/SKILL.md` — understand each skill's scope and instructions.
3. Read every `references/<name>.md` — understand what cross-cutting knowledge is available.

Do not skip this step. Changes made without reading the full harness often introduce inconsistencies.

### Step 2 — Understand what needs to change

Identify the type of change being requested:

| Change type | What to do |
|---|---|
| Add a new capability | Create a new skill directory with `SKILL.md`; update `HARNESS.md` to list it |
| Remove a capability | Delete the skill directory; remove it from `HARNESS.md` |
| Refine skill instructions | Edit the relevant `SKILL.md` body |
| Add cross-cutting knowledge | Create a new reference file; update `HARNESS.md` to list it |
| Update existing knowledge | Edit the relevant reference file |
| Rename or restructure | Update the directory name, the frontmatter `name` field, and all references to it in `HARNESS.md` |
| Split an overloaded skill | Create two new focused skills; remove the original; update `HARNESS.md` |
| Merge redundant skills | Combine into one skill; remove the originals; update `HARNESS.md` |

### Step 3 — Check for consistency

After making changes, verify:

- Every skill listed in `HARNESS.md` has a corresponding `SKILL.md` on disk
- Every reference listed in `HARNESS.md` has a corresponding file on disk
- No skill in `HARNESS.md` is missing from the body index, and no skill on disk is absent from `HARNESS.md`
- The `HARNESS.md` body is still accurate — descriptions may need updating when skills change scope

### Step 4 — Keep HARNESS.md concise

After any edit, re-read `HARNESS.md` and ask: is every sentence necessary? The body must remain brief enough to fit comfortably in context. If it has grown too long:

- Move detailed information into a skill or reference where it belongs
- Shorten inline descriptions to one clause each
- Remove prose that restates information already in skills or references

### Step 5 — Validate

After all changes are complete, run:

```bash
harnesses-ref validate ./<harness-name>
```

Fix any reported errors before presenting the result.

### Step 6 — Summarize changes

Tell the user:
1. What was changed and why
2. Anything that was left unchanged and why
3. Any follow-up questions or gaps you noticed that may need a future update
