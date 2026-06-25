import textwrap
from pathlib import Path

import pytest

from harnesses_ref.errors import ParseError
from harnesses_ref.parser import parse

SKILL_DETECTORS = "skill=SKILL.md\n"


def make_harness(tmp_path: Path, harness_md: str, leaf_detectors: str | None = None) -> Path:
    harness_dir = tmp_path / "harness"
    harness_dir.mkdir()
    (harness_dir / "HARNESS.md").write_text(textwrap.dedent(harness_md).strip())
    if leaf_detectors is not None:
        (harness_dir / ".leaf-detectors").write_text(leaf_detectors)
    return harness_dir


def test_parse_minimal(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test Harness
        description: A test harness.
        ---

        Body text.
    """)
    h = parse(d)
    assert h.name == "Test Harness"
    assert h.description == "A test harness."
    assert "Body text." in h.body
    assert h.directories == []


def test_parse_with_skill(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test Harness
        description: A test harness.
        ---
    """, leaf_detectors=SKILL_DETECTORS)
    skill_dir = d / "skills" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: My Skill\ndescription: Does a thing.\n---\nInstructions."
    )
    h = parse(d)
    assert len(h.directories) == 1
    assert h.directories[0].name == "skills"
    assert h.directories[0].routing_file_name == "SKILLS.md"
    assert len(h.directories[0].skills) == 1
    assert h.directories[0].skills[0].name == "My Skill"
    assert h.directories[0].skills[0].description == "Does a thing."


def test_parse_without_leaf_detectors_skill_not_detected(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test Harness
        description: A test harness.
        ---
    """)
    skill_dir = d / "skills" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: My Skill\ndescription: Does a thing.\n---\nInstructions."
    )
    h = parse(d)
    # Without .leaf-detectors declaring skill=SKILL.md, the directory is traversed,
    # not treated as a skill leaf.
    assert h.directories[0].skills == []
    assert any(f.filename == "SKILL.md" for f in h.directories[0].content)


def test_parse_with_content_file(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test Harness
        description: A test harness.
        ---
    """)
    context_dir = d / "context"
    context_dir.mkdir()
    (context_dir / "style-guide.md").write_text(
        "---\ndescription: Typography and tone rules.\n---\nContent."
    )
    h = parse(d)
    assert len(h.directories) == 1
    assert h.directories[0].name == "context"
    assert h.directories[0].routing_file_name == "CONTEXT.md"
    assert len(h.directories[0].content) == 1
    assert h.directories[0].content[0].filename == "style-guide.md"
    assert h.directories[0].content[0].description == "Typography and tone rules."


def test_parse_routing_file_description(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test Harness
        description: A test harness.
        ---
    """)
    tools_dir = d / "tools"
    tools_dir.mkdir()
    (tools_dir / "TOOLS.md").write_text(
        "---\ndescription: Data retrieval and compute tools.\n---\nBody."
    )
    h = parse(d)
    assert h.directories[0].description == "Data retrieval and compute tools."


def test_parse_arbitrary_top_level_dir(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test Harness
        description: A test harness.
        ---
    """)
    for name in ["brand", "campaigns", "outputs"]:
        (d / name).mkdir()
    h = parse(d)
    assert {dir_.name for dir_ in h.directories} == {"brand", "campaigns", "outputs"}
    assert {dir_.routing_file_name for dir_ in h.directories} == {
        "BRAND.md", "CAMPAIGNS.md", "OUTPUTS.md"
    }


def test_parse_harnessleaf_stops_traversal(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test Harness
        description: A test harness.
        ---
    """)
    data_dir = d / "data" / "case-law"
    data_dir.mkdir(parents=True)
    (data_dir / ".harnessleaf").write_text("")
    (data_dir / "2024-01-ruling.md").write_text("---\ndescription: A ruling.\n---\nContent.")
    h = parse(d)
    assert h.directories[0].content == []


def test_parse_skill_md_stops_traversal(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test Harness
        description: A test harness.
        ---
    """, leaf_detectors=SKILL_DETECTORS)
    skill_dir = d / "tools" / "query-database"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: Query Database\ndescription: Runs SQL queries.\n---\nInstructions."
    )
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "run_query.py").write_text("# script")
    h = parse(d)
    assert len(h.directories) == 1
    assert h.directories[0].name == "tools"
    assert len(h.directories[0].skills) == 1
    assert h.directories[0].skills[0].name == "Query Database"


def test_parse_leaf_detectors_custom_pattern(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test Harness
        description: A test harness.
        ---
    """, leaf_detectors="resource=RESOURCE.md\n")
    resource_dir = d / "data" / "case-law"
    resource_dir.mkdir(parents=True)
    (resource_dir / "RESOURCE.md").write_text("---\ndescription: Case law index.\n---")
    (resource_dir / "2024-ruling.md").write_text("---\ndescription: A ruling.\n---\nContent.")
    h = parse(d)
    # case-law/ is a resource leaf — contents not collected, not treated as a skill
    assert h.directories[0].skills == []
    assert h.directories[0].content == []


def test_parse_missing_harness_md(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(ParseError):
        parse(empty)


def test_parse_missing_frontmatter(tmp_path):
    d = tmp_path / "harness"
    d.mkdir()
    (d / "HARNESS.md").write_text("No frontmatter here.")
    with pytest.raises(ParseError):
        parse(d)
