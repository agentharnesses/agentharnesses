from pathlib import Path

from .errors import ValidationError
from .parser import parse, ParseError


def validate(harness_path: Path) -> list[str]:
    """Return a list of validation error messages. Empty list means valid."""
    errors: list[str] = []

    harness_md = harness_path / "HARNESS.md"
    if not harness_md.exists():
        errors.append(f"{harness_path}: missing required HARNESS.md")
        return errors

    try:
        harness = parse(harness_path)
    except ParseError as e:
        errors.append(str(e))
        return errors

    if not harness.name:
        errors.append(f"{harness_md}: 'name' is required in frontmatter")
    if not harness.description:
        errors.append(f"{harness_md}: 'description' is required in frontmatter")

    for skill in harness.skills:
        if not skill.name:
            errors.append(f"{skill.path / 'SKILL.md'}: 'name' is required in frontmatter")
        if not skill.description:
            errors.append(f"{skill.path / 'SKILL.md'}: 'description' is required in frontmatter")

    for ref in harness.references:
        if not ref.description:
            errors.append(f"{ref.path}: 'description' is recommended in frontmatter")

    return errors
