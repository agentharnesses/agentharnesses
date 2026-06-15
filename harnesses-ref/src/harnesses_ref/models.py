from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SkillRef:
    name: str
    description: str
    path: Path


@dataclass
class ReferenceDoc:
    filename: str
    description: str
    path: Path


@dataclass
class Harness:
    name: str
    description: str
    body: str
    path: Path
    skills: list[SkillRef] = field(default_factory=list)
    references: list[ReferenceDoc] = field(default_factory=list)
