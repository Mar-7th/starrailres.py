from pathlib import Path
from typing import Type, TypeVar

from msgspec.json import decode

T = TypeVar("T")


def decode_json(path: Path, t: Type[T]) -> T:
    if not path.exists():
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8") as f:
        return decode(f.read(), type=t)
