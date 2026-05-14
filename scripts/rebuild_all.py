from __future__ import annotations

import subprocess

CMDS = [
    ["python", "scripts/build_graph.py"],
    ["python", "scripts/build_indexes.py"],
]

for cmd in CMDS:
    subprocess.run(cmd, check=True)
print("rebuild complete")
