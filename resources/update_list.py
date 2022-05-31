import json
import hashlib
from pathlib import Path


def update():
    resource_list = []
    for file in Path("images").rglob("*"):
        if not file.is_file():
            continue
        resource_list.append(
            {"path": str(file), "hash": hashlib.md5(file.read_bytes()).hexdigest()}
        )
    resource_list.sort(key=lambda i: i["path"])
    with open("resource_list.json", "w", encoding="utf-8") as f:
        json.dump(resource_list, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    update()
