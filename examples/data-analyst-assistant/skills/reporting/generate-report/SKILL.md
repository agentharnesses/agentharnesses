---
name: Generate Report
description: Produce a formatted markdown summary or chart description from structured data.
---

Use this skill after fetching data with `query-database` or `read-spreadsheet` to present findings clearly.

**Steps**
1. Review the data and the user's original question.
2. Consult `references/report-standards/reporting-standards.md` for the preferred format, chart type, and rounding rules.
3. Choose the appropriate output format:
   - For small result sets (< 20 rows): a markdown table
   - For trends over time: describe a line chart with axes labeled
   - For comparisons across categories: describe a bar chart
   - For executive summaries: 3–5 bullet points with key findings
4. Write the report in the format specified by `reporting-standards.md`.
5. End with a one-sentence interpretation of the most important finding.
