#!/usr/bin/env python3
"""Convert storymap.md to storymap.csv.

Expected markdown shape (the canonical format this skill produces):

    # Story Map: <Project Name>
    > Outcome: <one-line outcome>
    > Personas: <persona1>, <persona2>
    > Slicing: <walking-skeleton/mvp/r2 | pi-1/pi-2 | now/next/later>

    ## Activity: <activity name>

    ### Task: <task name>

    - [slice:<slice>] [persona:<persona>] [status:<status> | <evidence>] As a <persona>, I want to <action>, so that <outcome>
    - [slice:<slice>] <story without persona form>
    - ...

    ### Task: <task name>
    ...

    ## Activity: <activity name>
    ...

The slice tag is required on every story. Persona tag is optional; if missing,
the script attempts to extract from "As a <persona>" form. If both fail, persona
is left blank. Status tag is optional (added by Step 0.5 reconciliation); first
token before `|` becomes the `status` column, the remainder becomes
`status_evidence` verbatim.

Usage:
    python storymap_to_csv.py storymap.md > storymap.csv
    python storymap_to_csv.py storymap.md -o storymap.csv

Output columns:
    id, activity, task, story, persona, outcome, slice, status, status_evidence
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Iterator


SLICE_RE = re.compile(r"\[slice:([^\]]+)\]", re.IGNORECASE)
PERSONA_TAG_RE = re.compile(r"\[persona:([^\]]+)\]", re.IGNORECASE)
STATUS_TAG_RE = re.compile(r"\[status:([^\]]+)\]", re.IGNORECASE)
AS_A_RE = re.compile(r"\bAs an?\s+([^,]+?),", re.IGNORECASE)
SO_THAT_RE = re.compile(r"\bso that\s+(.+?)\s*$", re.IGNORECASE)


def parse_storymap(md_text: str) -> Iterator[dict]:
    """Walk the markdown, yielding one dict per story.

    Lines inside HTML comment blocks (`<!-- ... -->`) are skipped. This matters
    because the canonical template embeds usage notes as comment-block bullets
    that would otherwise be parsed as phantom stories.
    """
    activity = None
    task = None
    story_id = 0
    in_comment = False

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip()

        # Handle HTML comment blocks. Supports both single-line `<!-- x -->`
        # (skip just this line) and multi-line `<!-- ... \n ... \n -->` (skip
        # everything between open and close, inclusive).
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line:
            if "-->" not in line:
                in_comment = True
            # Either way, don't parse content on the opening line.
            continue

        if line.startswith("## Activity:"):
            activity = line[len("## Activity:"):].strip()
            task = None
            continue

        # Cross-cutting / non-backbone sections per slicing-strategies.md use
        # `## Non-backbone / cross-cutting` (any text after `## Non-backbone`)
        # followed by `### Theme: <name>` headers. Treat the theme as the
        # activity ("Non-backbone: <theme>") and the next `### Task:` as the
        # task, OR treat the theme itself as both activity and task when no
        # explicit task header follows.
        if line.startswith("## ") and "non-backbone" in line.lower():
            activity = None  # waits for a ### Theme: header
            task = None
            in_non_backbone = True
            continue

        if line.startswith("### Theme:"):
            theme = line[len("### Theme:"):].strip()
            activity = f"Non-backbone: {theme}"
            task = theme  # default task = theme name; overridden by `### Task:` if present
            continue

        if line.startswith("### Task:"):
            task = line[len("### Task:"):].strip()
            continue

        if line.startswith("- ") and activity and task:
            story_id += 1
            yield parse_story_line(line[2:], story_id, activity, task)


def parse_story_line(text: str, story_id: int, activity: str, task: str) -> dict:
    """Parse a single story line into a row dict."""
    slice_match = SLICE_RE.search(text)
    slice_name = slice_match.group(1).strip() if slice_match else ""

    persona_tag_match = PERSONA_TAG_RE.search(text)
    persona = persona_tag_match.group(1).strip() if persona_tag_match else ""

    status_tag_match = STATUS_TAG_RE.search(text)
    # First token before `|` is the canonical status (done / in-progress / blocked / deferred / cut / unchanged).
    # Remainder (date, tracker id, branch, etc.) is preserved verbatim in status_evidence.
    status = ""
    status_evidence = ""
    if status_tag_match:
        raw = status_tag_match.group(1).strip()
        if "|" in raw:
            head, _, rest = raw.partition("|")
            status = head.strip()
            status_evidence = rest.strip()
        else:
            status = raw

    # Strip tags from the story body
    body = SLICE_RE.sub("", text)
    body = PERSONA_TAG_RE.sub("", body)
    body = STATUS_TAG_RE.sub("", body).strip()

    # If persona wasn't tagged, try to extract from "As a <persona>" form
    if not persona:
        as_a_match = AS_A_RE.search(body)
        if as_a_match:
            persona = as_a_match.group(1).strip()

    # Extract outcome from "so that <outcome>" form
    outcome = ""
    so_that_match = SO_THAT_RE.search(body)
    if so_that_match:
        outcome = so_that_match.group(1).strip().rstrip(".")

    return {
        "id": f"S{story_id:03d}",
        "activity": activity,
        "task": task,
        "story": body,
        "persona": persona,
        "outcome": outcome,
        "slice": slice_name,
        "status": status,
        "status_evidence": status_evidence,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("input", type=Path, help="Path to storymap.md")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Path to write CSV. Default: stdout.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"error: {args.input} does not exist", file=sys.stderr)
        return 1

    md_text = args.input.read_text(encoding="utf-8")
    rows = list(parse_storymap(md_text))

    if not rows:
        print(
            "warning: no stories parsed. Check that storymap.md uses '## Activity:', "
            "'### Task:', and '- [slice:...]' headers.",
            file=sys.stderr,
        )

    fieldnames = ["id", "activity", "task", "story", "persona", "outcome", "slice", "status", "status_evidence"]
    out_handle = args.output.open("w", encoding="utf-8", newline="") if args.output else sys.stdout
    try:
        writer = csv.DictWriter(out_handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    finally:
        if args.output:
            out_handle.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
