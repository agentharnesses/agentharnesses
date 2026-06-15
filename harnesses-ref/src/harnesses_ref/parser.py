import re
from pathlib import Path

import strictyaml

from .errors import ParseError
from .models import Harness, ReferenceDoc, SkillRef

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)", re.DOTALL)


def _split_frontmatter(text: str, path: str) -> tuple[dict, str]:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        raise ParseError(path, "missing YAML frontmatter (expected --- block at top of file)")
    try:
        fm = strictyaml.load(match.group(1)).data
    except strictyaml.YAMLError as e:
        raise ParseError(path, f"invalid YAML frontmatter: {e}") from e
    return fm, match.group(2).strip()


def _parse_skill(skill_dir: Path) -> SkillRef:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise ParseError(str(skill_dir), "missing SKILL.md")
    fm, _ = _split_frontmatter(skill_md.read_text(), str(skill_md))
    return SkillRef(
        name=fm.get("name", skill_dir.name),
        description=fm.get("description", ""),
        path=skill_dir,
    )


def _parse_reference(ref_path: Path) -> ReferenceDoc:
    fm, _ = _split_frontmatter(ref_path.read_text(), str(ref_path))
    return ReferenceDoc(
        filename=ref_path.name,
        description=fm.get("description", ""),
        path=ref_path,
    )


def parse(harness_path: Path) -> Harness:
    harness_md = harness_path / "HARNESS.md"
    if not harness_md.exists():
        raise ParseError(str(harness_path), "missing HARNESS.md")

    fm, body = _split_frontmatter(harness_md.read_text(), str(harness_md))

    skills: list[SkillRef] = []
    skills_dir = harness_path / "skills"
    if skills_dir.exists():
        for skill_md in sorted(skills_dir.rglob("SKILL.md")):
            skills.append(_parse_skill(skill_md.parent))

    references: list[ReferenceDoc] = []
    refs_dir = harness_path / "references"
    if refs_dir.exists():
        for ref in sorted(refs_dir.rglob("*.md")):
            references.append(_parse_reference(ref))

    return Harness(
        name=fm.get("name", ""),
        description=fm.get("description", ""),
        body=body,
        path=harness_path,
        skills=skills,
        references=references,
    )
