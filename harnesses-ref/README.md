# harnesses-ref

A reference library for Agent Harnesses.

## Installation

```bash
pip install harnesses-ref
```

## Usage

```bash
harnesses-ref validate <path>
harnesses-ref read <path> <property>
harnesses-ref prompt <path>
```

## Releasing

Versions are derived from git tags. To publish a new release to PyPI:

```bash
git tag v0.1.3
git push origin v0.1.3
```

The CI workflow builds and publishes automatically on any `v*` tag push. No changes to `pyproject.toml` are needed.
