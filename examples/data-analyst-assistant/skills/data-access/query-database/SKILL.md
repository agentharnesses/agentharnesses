---
name: Query Database
description: Run a read-only SQL query against the product database and return results.
---

Use this skill when the user asks a question that requires fetching data from the database.

**Steps**
1. Identify what data the user needs. Consult `references/data-sources/data-dictionary.md` if you're unsure which table or column to use.
2. Write a read-only `SELECT` statement. Never use `INSERT`, `UPDATE`, `DELETE`, or `DROP`.
3. Run `scripts/run_query.py` with the SQL as a positional argument.
4. If the query returns an error, explain the issue to the user and suggest a correction.
5. Present results in a readable table or prose summary depending on the volume of data.

**Script:** `scripts/run_query.py "<sql>"`

**Environment variables required**
- `DB_HOST` — database hostname
- `DB_NAME` — database name
- `DB_USER` — read-only database user
- `DB_PASSWORD` — password for the read-only user
