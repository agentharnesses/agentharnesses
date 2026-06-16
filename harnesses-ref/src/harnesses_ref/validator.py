from pathlib import Path

from .errors import ValidationError
from .parser import parse, ParseError


def _check_skill_subdirs(parent: Path, errors: list[str]) -> None:
    """Warn if any skill grouping directory is missing SKILLS.md.

    Leaf skill dirs (those containing SKILL.md) are not grouping dirs and are skipped,
    along with any of their descendants (e.g. scripts/).
    """
    if not parent.exists():
        return
    for child in sorted(parent.iterdir()):
        if not child.is_dir():
            continue
        if (child / "SKILL.md").exists():
            continue  # leaf skill dir, not a grouping dir
        if not (child / "SKILLS.md").exists():
            errors.append(
                f"{child}: skill grouping subdirectory is missing SKILLS.md — "
                f"add one to summarize its contents"
            )
        _check_skill_subdirs(child, errors)


def _check_reference_subdirs(parent: Path, errors: list[str]) -> None:
    """Warn if any reference grouping directory is missing REFERENCES.md."""
    if not parent.exists():
        return
    for child in sorted(parent.iterdir()):
        if not child.is_dir():
            continue
        if not (child / "REFERENCES.md").exists():
            errors.append(
                f"{child}: reference grouping subdirectory is missing REFERENCES.md — "
                f"add one to summarize its contents"
            )
        _check_reference_subdirs(child, errors)


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
        if ref.path.suffix == ".md" and not ref.description:
            errors.append(f"{ref.path}: markdown reference files are recommended to have a 'description' in frontmatter")

    _check_skill_subdirs(harness_path / "skills", errors)
    _check_reference_subdirs(harness_path / "references", errors)

    return errors
