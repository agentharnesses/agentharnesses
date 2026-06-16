# Agent Harnesses

A standardized way to give AI agents roles, environments, and capabilities.

## What is an Agent Harness?

A harness is a portable folder that gives an AI agent everything it needs to fulfill a role: an identity (`HARNESS.md`), a set of skills, and cross-cutting reference material. Agents load harnesses at startup and use progressive disclosure to pull in only what each task requires.

```
my-harness/
├── HARNESS.md        # Required: metadata + instructions
├── skills/           # Optional: Agent Skills (one per subdirectory)
└── references/       # Optional: cross-skill reference documents
```

## Relationship to Agent Skills

Harnesses build on the [Agent Skills](https://github.com/agentskills/agentskills) standard. A skill is an atomic unit of capability; a harness bundles many skills together to define a complete agent role.

## Documentation

See [agentharnesses.dev](https://agentharnesses.dev) for the full specification and guides.

## Reference Library

The [`harnesses-ref`](./harnesses-ref) directory contains a Python reference implementation and CLI for validating, reading, and rendering harnesses.

```bash
pip install harnesses-ref
harnesses-ref validate ./my-harness
```

## Examples

The [`examples/`](./examples) directory contains three fully worked harnesses:

| Example | Description |
|---|---|
| [`data-analyst-assistant`](./examples/data-analyst-assistant) | Queries databases, reads spreadsheets, and generates reports |
| [`software-development-assistant`](./examples/software-development-assistant) | Reads code, makes edits, and runs tests in a codebase |
| [`writing-publishing-assistant`](./examples/writing-publishing-assistant) | Searches existing posts, finds reusable images, and drafts new content |

## License

Code: Apache 2.0 | Documentation: CC-BY-4.0
