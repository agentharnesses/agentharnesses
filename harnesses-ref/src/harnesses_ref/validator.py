from pathlib import Path

from .parser import parse, ParseError


def _collect_skill_subdir_warnings(parent: Path, out: list[str]) -> None:
    """Collect warnings for skill grouping directories missing SKILLS.md.

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
            out.append(
                f"{child}: skill grouping subdirectory is missing SKILLS.md — "
                f"add one to summarize its contents"
            )
        _collect_skill_subdir_warnings(child, out)


def _collect_reference_subdir_warnings(parent: Path, out: list[str]) -> None:
    """Collect warnings for reference grouping directories missing REFERENCES.md."""
    if not parent.exists():
        return
    for child in sorted(parent.iterdir()):
        if not child.is_dir():
            continue
        if not (child / "REFERENCES.md").exists():
            out.append(
                f"{child}: reference grouping subdirectory is missing REFERENCES.md — "
                f"add one to summarize its contents"
            )
        _collect_reference_subdir_warnings(child, out)


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

    return errors


def warnings(harness_path: Path) -> list[str]:
    """Return a list of advisory warnings. Warnings do not indicate an invalid harness.

    Currently warns when skill or reference grouping subdirectories are missing their
    respective SKILLS.md / REFERENCES.md summary files, which enable progressive
    disclosure but are not required.
    """
    out: list[str] = []

    harness_md = harness_path / "HARNESS.md"
    if not harness_md.exists():
        return out

    _collect_skill_subdir_warnings(harness_path / "skills", out)
    _collect_reference_subdir_warnings(harness_path / "references", out)

    return out
