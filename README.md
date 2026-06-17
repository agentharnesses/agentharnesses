# Agent Harnesses

A standardized format for giving AI agents a defined role, skills, and reference material.

## What is an Agent Harness?

A harness is a folder that gives an AI agent everything it needs to fulfill a role. As tasks arrive, the agent is able to pull skills and references relevent to that task.

```
my-harness/
├── HARNESS.md        # Required: identity + overview
├── skills/           # Optional: Agent Skills (one per subdirectory)
└── references/       # Optional: cross-skill reference documents
```

For larger harnesses, skills and references can be organized into named subdirectories. Adding a `SKILLS.md` or `REFERENCES.md` summary file to each grouping subdirectory is optional but strongly encouraged — it lets the agent navigate the structure without loading every file upfront.

## Relationship to Agent Skills

Harnesses build on the [Agent Skills](https://github.com/agentskills/agentskills) standard. A skill is an atomic unit of capability; a harness bundles many skills together to define a complete agent role.

## Documentation

See [agentharnesses.io](https://agentharnesses.io) for the full specification and guides.

## Reference Implementation

The [`harnesses-ref`](./harnesses-ref) directory contains a Python reference implementation and CLI for validating, reading, and rendering harnesses.

```bash
pip install "git+https://github.com/agentharnesses/agentharnesses.git#subdirectory=harnesses-ref"
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
