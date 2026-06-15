---
name: Search Posts
description: Search through existing published posts by topic, keyword, or date range.
---

Use this skill when the user wants to find what has already been written on a topic, locate a specific post, or check whether a topic has been covered before.

**Steps**
1. Ask the user for a search term, topic, or date range if not provided.
2. Search the posts directory or content store for matching entries.
3. Return a list of matching posts with: title, publish date, and a one-sentence summary.
4. If no matches are found, suggest related topics that were covered.

Consult `references/topic-index.md` for a structured index of covered topics before running a full-text search.
