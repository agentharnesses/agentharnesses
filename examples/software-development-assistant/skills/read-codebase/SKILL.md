---
name: Read Codebase
description: Search for and read source files in the project to understand existing code.
---

Use this skill before making any code suggestions or edits — always read the relevant code first.

**Steps**
1. If the user describes a feature or bug without specifying a file, search for the relevant code:
   - Use `grep -r "<term>" .` to find references
   - Use `find . -name "<pattern>"` to locate files by name
2. Read the identified files in full before drawing conclusions.
3. If the code references other modules or functions, trace them as needed.
4. Summarize your understanding to the user before proposing any changes.

Consult `references/architecture.md` if you're unsure where to look.
