import textwrap
from pathlib import Path

import pytest

from harnesses_ref.errors import ParseError
from harnesses_ref.parser import parse


def make_harness(tmp_path: Path, harness_md: str, skills: dict = None, refs: dict = None) -> Path:
    harness_dir = tmp_path / "harness"
    harness_dir.mkdir()
    (harness_dir / "HARNESS.md").write_text(textwrap.dedent(harness_md).strip())

    if skills:
        for skill_name, skill_md in skills.items():
            skill_dir = harness_dir / "skills" / skill_name
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(textwrap.dedent(skill_md).strip())

    if refs:
        refs_dir = harness_dir / "references"
        refs_dir.mkdir()
        for filename, content in refs.items():
            (refs_dir / filename).write_text(textwrap.dedent(content).strip())

    return harness_dir


def test_parse_minimal(tmp_path):
    harness_dir = make_harness(tmp_path, """
        ---
        name: Test Harness
        description: A test harness.
        ---

        Body text.
    """)
    h = parse(harness_dir)
    assert h.name == "Test Harness"
    assert h.description == "A test harness."
    assert "Body text." in h.body
    assert h.skills == []
    assert h.references == []


def test_parse_with_skills(tmp_path):
    harness_dir = make_harness(
        tmp_path,
        """
        ---
        name: Test Harness
        description: A test harness.
        ---
        """,
        skills={
            "my-skill": """
                ---
                name: My Skill
                description: Does a thing.
                ---
                Instructions here.
            """
        },
    )
    h = parse(harness_dir)
    assert len(h.skills) == 1
    assert h.skills[0].name == "My Skill"
    assert h.skills[0].description == "Does a thing."


def test_parse_with_references(tmp_path):
    harness_dir = make_harness(
        tmp_path,
        """
        ---
        name: Test Harness
        description: A test harness.
        ---
        """,
        refs={
            "style-guide.md": """
                ---
                description: Typography and tone rules.
                ---
                Content here.
            """
        },
    )
    h = parse(harness_dir)
    assert len(h.references) == 1
    assert h.references[0].filename == "style-guide.md"
    assert h.references[0].description == "Typography and tone rules."


def test_parse_missing_harness_md(tmp_path):
    harness_dir = tmp_path / "empty"
    harness_dir.mkdir()
    with pytest.raises(ParseError):
        parse(harness_dir)


def test_parse_missing_frontmatter(tmp_path):
    harness_dir = tmp_path / "harness"
    harness_dir.mkdir()
    (harness_dir / "HARNESS.md").write_text("No frontmatter here.")
    with pytest.raises(ParseError):
        parse(harness_dir)
