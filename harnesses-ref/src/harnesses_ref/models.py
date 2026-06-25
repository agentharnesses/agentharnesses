from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SkillRef:
    name: str
    description: str
    path: Path


@dataclass
class ContentFile:
    filename: str
    description: str
    path: Path


@dataclass
class HarnessDirectory:
    name: str
    routing_file_name: str
    description: str
    path: Path
    skills: list[SkillRef] = field(default_factory=list)
    content: list[ContentFile] = field(default_factory=list)


@dataclass
class Harness:
    name: str
    description: str
    body: str
    path: Path
    directories: list[HarnessDirectory] = field(default_factory=list)
