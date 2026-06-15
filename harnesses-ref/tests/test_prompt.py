from pathlib import Path

from harnesses_ref.models import Harness, SkillRef, ReferenceDoc
from harnesses_ref.prompt import to_prompt_xml


def test_prompt_xml_minimal():
    h = Harness(name="Test", description="A test.", body="Overview.", path=Path("."))
    xml = to_prompt_xml(h)
    assert '<harness name="Test">' in xml
    assert "<description>A test.</description>" in xml
    assert "Overview." in xml


def test_prompt_xml_with_skills():
    h = Harness(
        name="Test",
        description="A test.",
        body="",
        path=Path("."),
        skills=[SkillRef(name="summarize", description="Condense text.", path=Path("."))],
    )
    xml = to_prompt_xml(h)
    assert '<skill name="summarize">Condense text.</skill>' in xml


def test_prompt_xml_with_references():
    h = Harness(
        name="Test",
        description="A test.",
        body="",
        path=Path("."),
        references=[ReferenceDoc(filename="style.md", description="Style rules.", path=Path("."))],
    )
    xml = to_prompt_xml(h)
    assert '<reference filename="style.md">Style rules.</reference>' in xml
