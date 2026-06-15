from pathlib import Path

import click

from .parser import parse, ParseError
from .prompt import to_prompt_xml
from .validator import validate


@click.group()
def main():
    """Reference CLI for Agent Harnesses."""
    pass


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path))
def validate_cmd(path: Path):
    """Validate a harness directory structure."""
    errors = validate(path)
    if not errors:
        click.echo(f"✓ {path} is valid")
    else:
        for error in errors:
            click.echo(f"✗ {error}", err=True)
        raise SystemExit(1)


main.add_command(validate_cmd, name="validate")


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("property", type=click.Choice(["name", "description"]))
def read(path: Path, property: str):
    """Read a property from HARNESS.md frontmatter."""
    try:
        harness = parse(path)
    except ParseError as e:
        click.echo(str(e), err=True)
        raise SystemExit(1)
    click.echo(getattr(harness, property))


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path))
def prompt(path: Path):
    """Render harness as prompt XML for agent injection."""
    try:
        harness = parse(path)
    except ParseError as e:
        click.echo(str(e), err=True)
        raise SystemExit(1)
    click.echo(to_prompt_xml(harness))
