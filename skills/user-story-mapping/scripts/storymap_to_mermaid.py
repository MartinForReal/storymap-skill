#!/usr/bin/env python3
"""Convert storymap.md to a Mermaid graph (storymap.mmd).

Expects the same canonical markdown shape as storymap_to_csv.py. See that
script's docstring for the format.

The generated diagram uses Mermaid's `graph TD` (top-down) with subgraphs
per backbone activity, then arrows showing the slicing layers below.

Usage:
    python storymap_to_mermaid.py storymap.md > storymap.mmd
    python storymap_to_mermaid.py storymap.md -o storymap.mmd

Mermaid output renders natively in GitHub, GitLab, Notion, and most modern
docs platforms. To render locally, install mermaid-cli:
    npm install -g @mermaid-js/mermaid-cli
    mmdc -i storymap.mmd -o storymap.png
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

# Reuse parser from storymap_to_csv to keep one source of truth for the format.
sys.path.insert(0, str(Path(__file__).parent))
from storymap_to_csv import parse_storymap  # noqa: E402


def slugify(text: str, max_len: int = 40) -> str:
    """Mermaid-safe node id."""
    s = re.sub(r"[^a-zA-Z0-9_]+", "_", text).strip("_")
    return s[:max_len] or "node"


def escape_label(text: str) -> str:
    """Escape characters Mermaid mishandles inside node labels."""
    return text.replace('"', "&quot;").replace("\n", " ")


def build_mermaid(rows: list[dict]) -> str:
    """Generate the Mermaid source from parsed story rows."""
    if not rows:
        return "graph TD\n  empty[\"(no stories parsed)\"]"

    activities: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    slice_order: list[str] = []
    slice_seen: set[str] = set()

    for row in rows:
        activities[row["activity"]][row["task"]].append(row)
        slice_name = row["slice"] or "unsliced"
        if slice_name not in slice_seen:
            slice_order.append(slice_name)
            slice_seen.add(slice_name)

    lines = ["graph TD"]
    lines.append("  classDef activity fill:#e0e7ff,stroke:#4338ca,stroke-width:2px;")
    lines.append("  classDef task fill:#fef3c7,stroke:#b45309,stroke-width:1px;")
    lines.append("  classDef story fill:#ecfdf5,stroke:#047857,stroke-width:1px;")
    lines.append("")

    # Backbone row: activities side-by-side
    activity_ids = {}
    for activity, tasks in activities.items():
        aid = "A_" + slugify(activity)
        activity_ids[activity] = aid
        lines.append(f'  {aid}["{escape_label(activity)}"]:::activity')

    # Link activities left-to-right to enforce the narrative reading order
    aid_list = list(activity_ids.values())
    if len(aid_list) > 1:
        lines.append("  " + " --> ".join(aid_list))

    lines.append("")

    # Tasks under each activity
    for activity, tasks in activities.items():
        aid = activity_ids[activity]
        for task_name, stories in tasks.items():
            tid = aid + "_T_" + slugify(task_name)
            lines.append(f'  {tid}["{escape_label(task_name)}"]:::task')
            lines.append(f"  {aid} --> {tid}")

            # Group stories by slice under each task
            by_slice: dict[str, list[dict]] = defaultdict(list)
            for story in stories:
                by_slice[story["slice"] or "unsliced"].append(story)

            for slice_name in slice_order:
                if slice_name not in by_slice:
                    continue
                for i, story in enumerate(by_slice[slice_name]):
                    sid = tid + f"_{slice_name}_S{i}"
                    sid = slugify(sid, max_len=80)
                    label = (story["story"][:60] + "…") if len(story["story"]) > 60 else story["story"]
                    label = f"[{slice_name}] {label}"
                    lines.append(f'  {sid}["{escape_label(label)}"]:::story')
                    lines.append(f"  {tid} --> {sid}")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("input", type=Path, help="Path to storymap.md")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Path to write Mermaid source. Default: stdout.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"error: {args.input} does not exist", file=sys.stderr)
        return 1

    md_text = args.input.read_text(encoding="utf-8")
    rows = list(parse_storymap(md_text))
    mermaid = build_mermaid(rows)

    if args.output:
        args.output.write_text(mermaid, encoding="utf-8")
    else:
        sys.stdout.write(mermaid)

    return 0


if __name__ == "__main__":
    sys.exit(main())
