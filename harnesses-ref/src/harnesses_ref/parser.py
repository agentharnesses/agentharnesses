import re
from pathlib import Path

import strictyaml

from .errors import ParseError
from .models import ContentFile, Harness, HarnessDirectory, SkillRef

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)", re.DOTALL)

def _split_frontmatter(text: str, path: str) -> tuple[dict, str]:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        raise ParseError(path, "missing YAML frontmatter (expected --- block at top of file)")
    try:
        fm = strictyaml.load(match.group(1)).data
    except strictyaml.YAMLError as e:
        raise ParseError(path, f"invalid YAML frontmatter: {e}") from e
    return fm, match.group(2).strip()


def load_leaf_detectors(harness_path: Path) -> dict[str, str]:
    """Return leaf detector patterns declared in .leaf-detectors at the harness root."""
    detectors: dict[str, str] = {}
    leaf_file = harness_path / ".leaf-detectors"
    if leaf_file.exists():
        for line in leaf_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                leaf_type, rel_path = line.split("=", 1)
                detectors[leaf_type.strip()] = rel_path.strip()
    return detectors


def leaf_type(directory: Path, detectors: dict[str, str]) -> str | None:
    """Return the leaf type of a directory, or None if it is not a leaf."""
    if (directory / ".harnessleaf").exists():
        return "leaf"
    for ltype, rel_path in detectors.items():
        if (directory / rel_path).exists():
            return ltype
    return None


def is_leaf(directory: Path, detectors: dict[str, str]) -> bool:
    return leaf_type(directory, detectors) is not None


def _parse_skill(skill_dir: Path) -> SkillRef:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise ParseError(str(skill_dir), "missing SKILL.md")
    fm, _ = _split_frontmatter(skill_md.read_text(), str(skill_md))
    return SkillRef(
        name=fm.get("name", ""),
        description=fm.get("description", ""),
        path=skill_dir,
    )


def _parse_content_file(path: Path) -> ContentFile:
    description = ""
    if path.suffix == ".md":
        try:
            fm, _ = _split_frontmatter(path.read_text(), str(path))
            description = fm.get("description", "")
        except ParseError:
            pass
    return ContentFile(filename=path.name, description=description, path=path)


def _collect(
    directory: Path,
    routing_file_name: str,
    detectors: dict[str, str],
) -> tuple[list[SkillRef], list[ContentFile]]:
    skills: list[SkillRef] = []
    content: list[ContentFile] = []
    for item in sorted(directory.iterdir()):
        if item.name.startswith("."):
            continue
        if item.name == routing_file_name:
            continue
        if item.is_dir():
            ltype = leaf_type(item, detectors)
            if ltype == "skill":
                skills.append(_parse_skill(item))
            elif ltype is not None:
                pass  # other leaf types: stop traversal, don't collect
            else:
                sub_skills, sub_content = _collect(item, routing_file_name, detectors)
                skills.extend(sub_skills)
                content.extend(sub_content)
        elif item.is_file():
            content.append(_parse_content_file(item))
    return skills, content


def parse(harness_path: Path) -> Harness:
    harness_md = harness_path / "HARNESS.md"
    if not harness_md.exists():
        raise ParseError(str(harness_path), "missing HARNESS.md")

    fm, body = _split_frontmatter(harness_md.read_text(), str(harness_md))
    detectors = load_leaf_detectors(harness_path)

    directories: list[HarnessDirectory] = []
    for item in sorted(harness_path.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue
        routing_file_name = item.name.upper() + ".md"
        dir_description = ""
        routing_file = item / routing_file_name
        if routing_file.exists():
            try:
                dir_fm, _ = _split_frontmatter(routing_file.read_text(), str(routing_file))
                dir_description = dir_fm.get("description", "")
            except ParseError:
                pass
        skills, content = _collect(item, routing_file_name, detectors)
        directories.append(HarnessDirectory(
            name=item.name,
            routing_file_name=routing_file_name,
            description=dir_description,
            path=item,
            skills=skills,
            content=content,
        ))

    return Harness(
        name=fm.get("name", ""),
        description=fm.get("description", ""),
        body=body,
        path=harness_path,
        directories=directories,
    )
