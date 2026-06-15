# Contributing to Agent Harnesses

## What We Accept

- **Documentation improvements** — typos, clarity, better examples
- **Bug reports** — open an Issue with steps to reproduce
- **Proposals** — open a Discussion before filing a PR for spec changes
- **Ecosystem listings** — clients or tools must be publicly available and demonstrably support the harness standard today

## What We're Not Accepting Yet

- Major architectural changes to the spec
- Harness submissions to a central registry (not yet available)
- Code contributions to `harnesses-ref` that add new commands (discuss first)

## AI Disclosure

If you used AI assistance to prepare your contribution, you must disclose it in the pull request or issue. This applies to all non-trivial changes. Include: what tool you used, which parts it generated, and confirmation that you reviewed and understood the output.

## Spec Philosophy

It is much easier to add things to a specification than to remove them. The bar for adding to the spec is high: proposals should address real implementation challenges you've encountered, not theoretical concerns. Demonstrate the actual problem before proposing a solution.

## Process

1. Fork the repository
2. Create a focused branch (`fix/typo-in-spec`, `proposal/nested-harnesses`)
3. Preview doc changes locally: `cd docs && npx mint dev`
4. Submit a pull request linked to any related issues

All contributions are licensed under Apache 2.0 (code/spec) or CC-BY-4.0 (documentation).
