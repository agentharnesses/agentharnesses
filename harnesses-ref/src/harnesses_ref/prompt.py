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

    for directory in harness.directories:
        attrs = f'name="{directory.name}"'
        if directory.description:
            attrs += f' description="{directory.description}"'
        lines.append(f"  <directory {attrs}>")
        for skill in directory.skills:
            lines.append(f'    <skill name="{skill.name}">{skill.description}</skill>')
        for item in directory.content:
            lines.append(f'    <file filename="{item.filename}">{item.description}</file>')
        lines.append("  </directory>")

    lines.append("</harness>")
    return "\n".join(lines)
