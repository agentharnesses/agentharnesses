from pathlib import Path

from harnesses_ref.models import ContentFile, Harness, HarnessDirectory, SkillRef
from harnesses_ref.prompt import to_prompt_xml


def test_prompt_xml_minimal():
    h = Harness(name="Test", description="A test.", body="Overview.", path=Path("."))
    xml = to_prompt_xml(h)
    assert '<harness name="Test">' in xml
    assert "<description>A test.</description>" in xml
    assert "Overview." in xml


def test_prompt_xml_with_directory():
    h = Harness(
        name="Test",
        description="A test.",
        body="",
        path=Path("."),
        directories=[
            HarnessDirectory(
                name="tools",
                routing_file_name="TOOLS.md",
                description="Data tools.",
                path=Path("."),
                skills=[SkillRef(name="query-db", description="Runs SQL.", path=Path("."))],
            )
        ],
    )
    xml = to_prompt_xml(h)
    assert '<directory name="tools"' in xml
    assert 'description="Data tools."' in xml
    assert '<skill name="query-db">Runs SQL.</skill>' in xml


def test_prompt_xml_with_content():
    h = Harness(
        name="Test",
        description="A test.",
        body="",
        path=Path("."),
        directories=[
            HarnessDirectory(
                name="context",
                routing_file_name="CONTEXT.md",
                description="",
                path=Path("."),
                content=[ContentFile(filename="style.md", description="Style rules.", path=Path("."))],
            )
        ],
    )
    xml = to_prompt_xml(h)
    assert '<file filename="style.md">Style rules.</file>' in xml


def test_prompt_xml_no_description_omits_attribute():
    h = Harness(
        name="Test",
        description="A test.",
        body="",
        path=Path("."),
        directories=[
            HarnessDirectory(
                name="brand",
                routing_file_name="BRAND.md",
                description="",
                path=Path("."),
            )
        ],
    )
    xml = to_prompt_xml(h)
    assert 'description=""' not in xml
    assert '<directory name="brand">' in xml
