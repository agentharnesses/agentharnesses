# Data Analyst Assistant

An example harness for an agent that answers data questions by querying databases, reading spreadsheets, and generating reports.

## What this harness does

This harness gives an agent the ability to retrieve company data from multiple sources, interpret it, and present findings in a format appropriate for the audience. It is structured with grouped subdirectories to demonstrate the `SKILLS.md` and `REFERENCES.md` pattern for organizing larger harnesses.

## Structure

```
data-analyst-assistant/
├── HARNESS.md
├── skills/
│   ├── data-access/
│   │   ├── SKILLS.md
│   │   ├── query-database/
│   │   └── read-spreadsheet/
│   └── reporting/
│       ├── SKILLS.md
│       └── generate-report/
└── references/
    ├── data-sources/
    │   ├── REFERENCES.md
    │   ├── data-dictionary.md
    │   ├── query-patterns.md
    │   └── known-data-issues.md
    ├── report-standards/
    │   ├── REFERENCES.md
    │   ├── reporting-standards.md
    │   └── audience-templates.md
    └── business-context/
        ├── REFERENCES.md
        ├── kpi-definitions.md
        └── team-glossary.md
```

## Skills

**data-access**
- `query-database` — runs read-only SQL queries against a product database via a Python script
- `read-spreadsheet` — reads rows and columns from CSV or Excel files via a Python script

**reporting**
- `generate-report` — formats query results into markdown tables, chart descriptions, or executive summaries based on reporting standards

## References

**data-sources** — everything the agent needs to understand the data it is working with: the schema, approved query idioms, and known data quality issues to work around.

**report-standards** — rules for how results should be presented, including number formatting, chart selection, and templates for different audiences (executive, team lead, ad-hoc).

**business-context** — domain knowledge for interpreting results correctly: official KPI definitions and team terminology.

## What makes this example notable

This harness uses grouped subdirectories for both skills and references, with `SKILLS.md` and `REFERENCES.md` summary files at each level. This keeps `HARNESS.md` short while still giving the agent a complete map of what is available.
