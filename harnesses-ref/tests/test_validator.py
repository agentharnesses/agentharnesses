import textwrap
from pathlib import Path

from harnesses_ref.validator import validate, warnings


def make_harness(tmp_path: Path, harness_md: str) -> Path:
    d = tmp_path / "harness"
    d.mkdir()
    (d / "HARNESS.md").write_text(textwrap.dedent(harness_md).strip())
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


def test_skill_grouping_dir_missing_skills_md(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test
        description: A valid harness.
        ---
        Body.
    """)
    group = d / "skills" / "data-access"
    group.mkdir(parents=True)
    (group / "query-database").mkdir()
    (group / "query-database" / "SKILL.md").write_text(
        "---\nname: Query\ndescription: Queries the db.\n---\nInstructions."
    )
    assert validate(d) == []
    warns = warnings(d)
    assert any("SKILLS.md" in w for w in warns)


def test_reference_grouping_dir_missing_references_md(tmp_path):
    d = make_harness(tmp_path, """
        ---
        name: Test
        description: A valid harness.
        ---
        Body.
    """)
    group = d / "references" / "data-sources"
    group.mkdir(parents=True)
    (group / "schema.md").write_text(
        "---\ndescription: Schema overview.\n---\nContent."
    )
    assert validate(d) == []
    warns = warnings(d)
    assert any("REFERENCES.md" in w for w in warns)
