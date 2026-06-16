# Software Development Assistant

An example harness for an agent that helps users understand, navigate, and modify a codebase.

## What this harness does

This harness gives an agent the ability to read source files, make targeted edits, and run the test suite. It is designed to be dropped into a software project alongside project-specific reference documents that describe the codebase's architecture and conventions.

## Structure

```
software-development-assistant/
├── HARNESS.md
├── skills/
│   ├── read-codebase/
│   ├── edit-code/
│   └── run-tests/
│       └── scripts/
└── references/
    ├── architecture.md
    └── conventions.md
```

## Skills

- `read-codebase` — searches and reads files in the project to understand existing code before making changes
- `edit-code` — makes targeted, minimal edits to source files
- `run-tests` — executes the test suite via a shell script and interprets the results

## References

- `architecture.md` — high-level overview of the codebase structure and key modules, so the agent understands how components relate before navigating the code
- `conventions.md` — coding style, naming conventions, and patterns specific to this project, so edits are consistent with existing code

## What makes this example notable

This is a minimal flat harness — no subdirectories, three skills, two references. It illustrates the simplest valid harness structure and shows how project-specific context (architecture, conventions) is carried in references rather than embedded in skill files.
