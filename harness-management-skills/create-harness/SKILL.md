---
name: Create Harness
description: Scaffold a new harness directory from scratch, including HARNESS.md, skills, and references.
---

Use this skill when the user asks you to create a new harness, set up an agent for a new role, or build a harness for a described use case.

## Process

### Step 1 — Understand the role

Before creating anything, gather the following from the user (or infer from context):

- **Name** — what is this agent called?
- **Role** — what is the agent's core job in one sentence?
- **Capabilities** — what specific things should the agent be able to do? (These become skills.)
- **Knowledge** — what cross-cutting information does the agent need? (These become references.)
- **Location** — where should the harness directory be created?

If the user's description is vague, ask clarifying questions before proceeding. A harness is only as clear as the role it encodes.

### Step 2 — Design the structure

Before writing any files, lay out the intended structure and confirm it with the user:

```
<harness-name>/
├── HARNESS.md
├── skills/
│   ├── <skill-1>/
│   │   └── SKILL.md
│   └── <skill-2>/
│       └── SKILL.md
└── references/
    └── <reference>.md
```

Each skill should be **atomic** — one clear responsibility. If a proposed skill seems to do two distinct things, split it.

### Step 3 — Write HARNESS.md

Create `HARNESS.md` at the harness root with the following structure:

```markdown
---
name: <name>
description: <one sentence describing what this agent does>
---

<one short paragraph describing the agent's role>

**Skills**
- `<skill-name>` — <one-line description>

**References**
- `<filename>` — <one-line description>
```

The body must be brief. It is loaded into the agent's context window on every activation.

### Step 4 — Write each SKILL.md

For each skill, create `skills/<skill-name>/SKILL.md`:

```markdown
---
name: <Skill Name>
description: <one sentence — when should this skill be used?>
---

<instructions for the agent>
```

Instructions should be written as numbered steps. Be explicit about what the agent should do, what it should check, and what it should produce. If the skill requires a script, note the script name and its interface.

### Step 5 — Write each reference

For each reference, create `references/<filename>.md`:

```markdown
---
description: <one sentence — what does this document cover?>
---

<content>
```

If the content isn't known yet, create a template with placeholder sections and instruct the user to fill it in.

### Step 6 — Validate

After creating all files, run:

```bash
harnesses-ref validate ./<harness-name>
```

Fix any reported errors before presenting the harness to the user.

### Step 7 — Present the result

Show the user:
1. The final directory tree
2. The content of `HARNESS.md`
3. A one-line summary of each skill and reference created
4. Any placeholders the user needs to fill in
