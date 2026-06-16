# Writing and Publishing Assistant

An example harness for an agent that helps find, draft, and improve written content while maintaining consistency across publications.

## What this harness does

This harness gives an agent the ability to search a library of existing posts, locate reusable images, and draft new content. It is designed to help a writer or editor stay consistent with past work and avoid repeating topics that have already been covered.

## Structure

```
writing-publishing-assistant/
├── HARNESS.md
├── skills/
│   ├── search-posts/
│   ├── find-images/
│   └── draft-post/
└── references/
    ├── style-guide.md
    └── topic-index.md
```

## Skills

- `search-posts` — searches existing published posts by topic, keyword, or date to find relevant prior work
- `find-images` — locates images from past posts that could be reused in a new piece
- `draft-post` — drafts a new post from an outline, brief, or topic description, following the style guide

## References

- `style-guide.md` — tone, formatting, and structure rules that all written output must follow
- `topic-index.md` — index of topics already covered, used to avoid repetition and identify content gaps

## What makes this example notable

This harness shows how references carry editorial context that applies across every skill. The style guide and topic index are consulted regardless of whether the agent is searching, finding images, or drafting — making them a natural fit for `references/` rather than being duplicated inside each skill.
