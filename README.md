# StarRailRes-Python

A python library for StarRailRes.

## Installation

```bash
pip install starrailres
```

## Usage

```python
from pathlib import Path
from starrailres import CharacterBasicInfo, Index, LevelInfo

# replace with index folder
index = Index(Path("index") / "en")

basic = CharacterBasicInfo(
    id="1102",
    rank=0,
    level=70,
    promotion=5,
    skill_tree_levels=[
        LevelInfo(id="1102001", level=2),
        LevelInfo(id="1102002", level=5),
        LevelInfo(id="1102003", level=6),
        LevelInfo(id="1102004", level=5),
        LevelInfo(id="1102007", level=1),
        LevelInfo(id="1102101", level=1),
        LevelInfo(id="1102102", level=1),
        LevelInfo(id="1102201", level=1),
        LevelInfo(id="1102202", level=1),
    ],
)

character = index.get_character_info(basic)
print(character)
```

For more examples, see `examples`.
