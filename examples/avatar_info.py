from pathlib import Path

from starrailres import Index

# replace with index folder
index = Index(Path("index") / "en")

avatar = index.get_avatar_info("200001")
print(avatar)
