from .models import Harness


def to_prompt_xml(harness: Harness) -> str:
    """Render a harness as prompt XML suitable for injection into an agent context."""
    lines: list[str] = []
    lines.append(f'<harness name="{harness.name}">')
    lines.append(f"  <description>{harness.description}</description>")

    if harness.body:
        lines.append("  <overview>")
        for line in harness.body.splitlines():
            lines.append(f"    {line}" if line else "")
        lines.append("  </overview>")

    if harness.skills:
        lines.append("  <skills>")
        for skill in harness.skills:
            lines.append(f'    <skill name="{skill.name}">{skill.description}</skill>')
        lines.append("  </skills>")

    if harness.references:
        lines.append("  <references>")
        for ref in harness.references:
            lines.append(f'    <reference filename="{ref.filename}">{ref.description}</reference>')
        lines.append("  </references>")

    lines.append("</harness>")
    return "\n".join(lines)
