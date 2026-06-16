---
name: Read Spreadsheet
description: Read rows and columns from a CSV or Excel file and return the contents.
---

Use this skill when the user references a spreadsheet, CSV, or Excel file.

**Steps**
1. Ask the user for the file path if they haven't provided one.
2. Run `scripts/read_spreadsheet.py` with the file path as the argument.
3. Inspect the column headers and a sample of rows to understand the data structure.
4. Answer the user's question based on the contents, summarizing or filtering as needed.

**Script:** `scripts/read_spreadsheet.py "<filepath>"`

Supported formats: `.csv`, `.xlsx`, `.xls`
