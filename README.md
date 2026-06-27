# Agent Harnesses

A standardized, open format for giving AI agents a defined role, context, and capabilities.

## What is a Harness?

A harness is a directory that gives an AI agent everything it needs to fulfill a role. At session start the agent loads `HARNESS.md` to establish its identity; as tasks arrive, it pulls in only the content each task requires — **progressive disclosure** applied at the harness level.

```
my-harness/
├── HARNESS.md          # Required: identity + routing overview
├── .leaf-detectors     # Optional: leaf boundary patterns
├── tools/              # Top-level dirs are named by the harness author
│   ├── TOOLS.md        # Routing file — describes what's in this branch
│   └── query-db/
│       └── SKILL.md
└── data/
    ├── DATA.md
    └── schema.md
```

Top-level directory names are chosen by the harness author. `skills/` and `references/` are common conventions but not required — any structure that fits the domain works.

## Key Concepts

### HARNESS.md

The required entry point. Uses YAML frontmatter followed by a brief routing body:

```markdown
---
name: Marketing Assistant
description: Helps create and review content across blog, social, and visual channels.
---

You are a marketing assistant. Produce content that is on-brand and channel-appropriate.

- `tools/` — content creation and research capabilities (see TOOLS.md)
- `brand/` — tone, typography, and visual guidelines (see BRAND.md)
- `campaigns/` — active campaign briefs and goals (see CAMPAIGNS.md)
```

Keep the body minimal — it is loaded on every activation and competes with task context.

### Routing Files

Each top-level directory uses a **routing file** named after it in all-caps: `TOOLS.md` for `tools/`, `DATA.md` for `data/`, and so on. This convention propagates through the entire subtree — every grouping subdirectory within `tools/` also uses `TOOLS.md`. Routing files let an agent decide whether a branch is relevant without opening every file inside it.

### Termination (Leaves)

Two mechanisms mark a directory as a leaf — a terminal point the routing layer does not recurse into:

- **`.harnessleaf`** — a file placed in any directory to signal an explicit boundary
- **`.leaf-detectors`** — a root-level file defining keyword patterns; e.g. `skill=SKILL.md` automatically marks any directory containing `SKILL.md` as a skill leaf

Leaf type names are meaningful: a `skill` leaf is loaded and executed as an Agent Skill; other types are treated as opaque boundaries.

### Loading Model

| Phase | Trigger | What happens |
|---|---|---|
| **Load** | Session start | Full `HARNESS.md` is injected, establishing the agent's role |
| **Discovery** | Task received | Agent reads routing files to find relevant branches |
| **Activation** | Routing aligns | Agent reads the content of a relevant skill, directory, or file |
| **Execution** | Action required | Agent runs a script bundled within a skill |

## Relationship to Agent Skills

Harnesses build on the [Agent Skills](https://github.com/agentskills/agentskills) standard. A skill is an atomic unit of capability; a harness bundles many skills together to define a complete agent role — like a job title where skills are the job requirements.

## Documentation

See [agentharnesses.io](https://agentharnesses.io) for the full specification, quickstart, best practices, and client implementation guide.

## Reference Implementation

The [`harnesses-ref`](./harnesses-ref) directory contains a Python reference implementation and CLI for validating, reading, and rendering harnesses.

```bash
pip install harnesses-ref
harnesses-ref validate ./my-harness
harnesses-ref prompt ./my-harness
```

## Examples

The [`examples/`](./examples) directory contains three example harnesses:

| Example | Description |
|---|---|
| [`data-analyst-assistant`](./examples/data-analyst-assistant) | Queries databases, reads spreadsheets, and generates reports — demonstrates the subdirectory pattern |
| [`software-development-assistant`](./examples/software-development-assistant) | Reads code, makes edits, and runs tests in a codebase |
| [`writing-publishing-assistant`](./examples/writing-publishing-assistant) | Searches existing posts, finds reusable images, and drafts new content |

## License

Code: Apache 2.0 | Documentation: CC-BY-4.0
