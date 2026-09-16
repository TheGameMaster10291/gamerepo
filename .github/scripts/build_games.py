#!/usr/bin/env python3
"""Rewrite games.json with every .html file in the repo.

raw.githubusercontent.com can only serve a file by its exact path - it cannot
list a folder - so the repo carries its own index and the library reads that.
Run from the root of the repo, or let the GitHub Action run it on every push.
"""

import json
import os

IGNORE = {"index.html", "readme.html"}
SKIP_DIRS = {".git", ".github", "node_modules"}

games = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for name in files:
        if not name.lower().endswith((".html", ".htm")):
            continue
        if name.lower() in IGNORE:
            continue
        path = os.path.relpath(os.path.join(root, name), ".").replace(os.sep, "/")
        games.append({"file": path, "size": os.path.getsize(path)})

games.sort(key=lambda g: g["file"].lower())

with open("games.json", "w", encoding="utf-8") as fh:
    json.dump({"games": games}, fh, indent=2)
    fh.write("\n")

print("games.json written -", len(games), "games")
for g in games:
    print("  ", g["file"], "-", round(g["size"] / 1048576, 1), "MB")
