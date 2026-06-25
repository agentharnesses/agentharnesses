from pathlib import Path

from .parser import ParseError, is_leaf, load_leaf_detectors, parse


def _collect_routing_warnings(
    parent: Path,
    routing_file_name: str,
    detectors: dict[str, str],
    out: list[str],
) -> None:
    if not parent.exists():
        return
    for child in sorted(parent.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if is_leaf(child, detectors):
            continue
        if not (child / routing_file_name).exists():
            out.append(
                f"{child}: grouping subdirectory is missing {routing_file_name} — "
                f"add one to summarize its contents"
            )
        _collect_routing_warnings(child, routing_file_name, detectors, out)


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

    for directory in harness.directories:
        for skill in directory.skills:
            if not skill.name:
                errors.append(f"{skill.path / 'SKILL.md'}: 'name' is required in frontmatter")
            if not skill.description:
                errors.append(f"{skill.path / 'SKILL.md'}: 'description' is required in frontmatter")

    return errors


def warnings(harness_path: Path) -> list[str]:
    """Return advisory warnings for missing routing files and missing file descriptions."""
    out: list[str] = []
    harness_md = harness_path / "HARNESS.md"
    if not harness_md.exists():
        return out
    detectors = load_leaf_detectors(harness_path)
    for item in sorted(harness_path.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue
        routing_file_name = item.name.upper() + ".md"
        _collect_routing_warnings(item, routing_file_name, detectors, out)
    try:
        harness = parse(harness_path)
        for directory in harness.directories:
            for item in directory.content:
                if item.path.suffix == ".md" and not item.description:
                    out.append(
                        f"{item.path}: markdown file should have a 'description' in frontmatter"
                    )
    except ParseError:
        pass
    return out
