import textwrap
from pathlib import Path

from harnesses_ref.validator import validate, warnings

SKILL_DETECTORS = "skill=SKILL.md\n"


def make_harness(tmp_path: Path, harness_md: str, leaf_detectors: str | None = None) -> Path:
    d = tmp_path / "harness"
    d.mkdir()
    (d / "HARNESS.md").write_text(textwrap.dedent(harness_md).strip())
    if leaf_detectors is not None:
        (d / ".leaf-detectors").write_text(leaf_detectors)
    return d


def test_valid_harness(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test
        description: A valid harness.
        ---
        Body.
    """)
    assert validate(d) == []


def test_missing_name(tmp_path):
    d = make_harness(tmp_path, """
        ---
        description: A harness without a name.
        ---
    """)
    errors = validate(d)
    assert any("name" in e for e in errors)


def test_missing_description(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test
        ---
    """)
    errors = validate(d)
    assert any("description" in e for e in errors)


def test_missing_harness_md(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    errors = validate(d)
    assert any("HARNESS.md" in e for e in errors)


def test_skill_missing_name(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test
        description: A valid harness.
        ---
    """, leaf_detectors=SKILL_DETECTORS)
    skill_dir = d / "skills" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\ndescription: Does a thing.\n---\nBody.")
    errors = validate(d)
    assert any("name" in e for e in errors)


def test_skill_missing_description(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test
        description: A valid harness.
        ---
    """, leaf_detectors=SKILL_DETECTORS)
    skill_dir = d / "skills" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: My Skill\n---\nBody.")
    errors = validate(d)
    assert any("description" in e for e in errors)


def test_grouping_dir_missing_routing_file(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test
        description: A valid harness.
        ---
    """, leaf_detectors=SKILL_DETECTORS)
    # tools/database/ is a non-leaf grouping dir — should warn about missing TOOLS.md
    group = d / "tools" / "database"
    group.mkdir(parents=True)
    skill_dir = group / "query-database"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\nname: Query Database\ndescription: Runs SQL.\n---\nInstructions."
    )
    assert validate(d) == []
    warns = warnings(d)
    assert any("TOOLS.md" in w for w in warns)


def test_skills_dir_missing_skills_md(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test
        description: A valid harness.
        ---
    """, leaf_detectors=SKILL_DETECTORS)
    group = d / "skills" / "data-access"
    group.mkdir(parents=True)
    skill_dir = group / "query-database"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\nname: Query\ndescription: Queries the db.\n---\nInstructions."
    )
    assert validate(d) == []
    warns = warnings(d)
    assert any("SKILLS.md" in w for w in warns)


def test_content_file_missing_description(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test
        description: A valid harness.
        ---
    """)
    context_dir = d / "context"
    context_dir.mkdir()
    (context_dir / "style-guide.md").write_text("No frontmatter here.")
    assert validate(d) == []
    warns = warnings(d)
    assert any("description" in w for w in warns)


def test_harnessleaf_dir_not_warned(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test
        description: A valid harness.
        ---
    """)
    leaf_dir = d / "data" / "case-law"
    leaf_dir.mkdir(parents=True)
    (leaf_dir / ".harnessleaf").write_text("")
    # case-law/ is a leaf — should NOT warn about missing DATA.md inside it
    warns = warnings(d)
    assert not any("case-law" in w for w in warns)
