#!/usr/bin/env python3
"""Grade outputs from the iteration-1 workspace against assertions in evals.json.

Writes grading.json into each run directory with this shape:
    {"expectations": [{"text": "...", "passed": true/false, "evidence": "..."}, ...]}

Uses field names text/passed/evidence (the viewer expects these exact names).
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DEFAULT_ITERATION = ROOT / "user-story-mapping-workspace" / "iteration-11"
EVALS_PATH = ROOT / "skills" / "user-story-mapping" / "evals" / "evals.json"


def get_iteration() -> Path:
    if len(sys.argv) > 1:
        return ROOT / "user-story-mapping-workspace" / sys.argv[1]
    return DEFAULT_ITERATION


ITERATION = get_iteration()

REQUIRED_FILES_CANONICAL = ["design.md", "storymap.md", "storymap.csv", "storymap.mmd", "backlog.md", "backlog.csv"]

SYSTEM_WORDS = re.compile(r"\b(api|service|module|database|backend|frontend|microservice|endpoint|schema|sdk|orm)\b", re.IGNORECASE)
USER_VERBS = re.compile(r"\b(find|search|browse|submit|review|approve|sign|book|schedule|view|save|select|enter|see|get|make|create|edit|share|invite|import|connect|install|launch|reject|accept|choose|complete|start|finish|navigate|tap|click|set|configure|send|read|return|arrive|bring|reach|land|onboard|setup|set-up|track|monitor|cancel|delete|update|upload|download|export|publish|deploy|test|verify|confirm|notify|message|chat|comment|like|follow|join|leave|filter|sort|order|pay|buy|purchase|check|sign-in|sign-up|log-in|log-out|discover|evaluate|try|integrate|organize|plan|decide|learn|explore|manage|handle|process|prepare|request|ship|deliver|store|retrieve|generate|draft|invoice|bill|capture|log|recover|reconcile|approve|deny|escalate|assign|tag|mark|hide|show|toggle|measure|mint|provision|grant|revoke|enable|disable|switch|fetch|push|pull|run|build|debug|profile|inspect|sync|reset|rotate)\b", re.IGNORECASE)


def list_files(out_dir: Path) -> list[str]:
    return [p.name.lower() for p in out_dir.rglob("*") if p.is_file()]


def read_all_text(out_dir: Path) -> str:
    text = []
    for p in out_dir.rglob("*"):
        if p.is_file() and p.suffix in {".md", ".csv", ".mmd", ".txt", ".json"}:
            try:
                text.append(p.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                pass
    return "\n".join(text)


def read_file(out_dir: Path, name: str) -> str | None:
    for p in out_dir.rglob(name):
        if p.is_file():
            try:
                return p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                return None
    return None


def grade_canonical_files(out_dir: Path) -> dict:
    files = list_files(out_dir)
    missing = [f for f in REQUIRED_FILES_CANONICAL if f.lower() not in files]
    return {
        "text": "Produces all six canonical files: design.md, storymap.md, storymap.csv, storymap.mmd, backlog.md, backlog.csv",
        "passed": not missing,
        "evidence": f"files present: {sorted(files)[:30]}; missing: {missing}",
    }


def grade_csv_header(out_dir: Path) -> dict:
    text = read_file(out_dir, "storymap.csv")
    # v0.0.3+ added status + status_evidence columns; accept either schema.
    legacy_header = "id,activity,task,story,persona,outcome,slice"
    current_header = "id,activity,task,story,persona,outcome,slice,status,status_evidence"
    if text is None:
        return {"text": "storymap.csv has canonical header", "passed": False, "evidence": "storymap.csv not found"}
    first = text.splitlines()[0].strip() if text.strip() else ""
    passed = first.lower() in (legacy_header, current_header)
    return {
        "text": f"storymap.csv has the canonical header (legacy 7-col OR current 9-col with status/status_evidence)",
        "passed": passed,
        "evidence": f"header was: {first!r}",
    }


def grade_mermaid(out_dir: Path) -> dict:
    text = read_file(out_dir, "storymap.mmd")
    if text is None:
        return {"text": "storymap.mmd valid Mermaid", "passed": False, "evidence": "storymap.mmd not found"}
    first = text.strip().splitlines()[0] if text.strip() else ""
    return {
        "text": "storymap.mmd starts with 'graph TD' (valid Mermaid)",
        "passed": first.startswith("graph TD"),
        "evidence": f"first line: {first!r}",
    }


def grade_personas(out_dir: Path) -> dict:
    text = read_file(out_dir, "design.md") or ""
    has = bool(re.search(r"(^|\n)#+\s*persona", text, re.IGNORECASE))
    return {
        "text": "Design doc contains a personas section",
        "passed": has,
        "evidence": "personas heading found" if has else "no personas heading in design.md (or design.md missing)",
    }


def grade_outcome(out_dir: Path) -> dict:
    text = read_file(out_dir, "design.md") or ""
    has = bool(re.search(r"(outcome|goal|success)", text, re.IGNORECASE))
    return {
        "text": "Design doc contains an explicit outcome statement",
        "passed": has,
        "evidence": "outcome/goal/success keyword in design.md" if has else "no such keyword (or design.md missing)",
    }


def grade_assumptions(out_dir: Path) -> dict:
    text = read_file(out_dir, "design.md") or ""
    has = bool(re.search(r"assumption", text, re.IGNORECASE))
    return {
        "text": "Design doc has an 'Assumptions to validate' section (no live user was available)",
        "passed": has,
        "evidence": "found 'assumption' keyword" if has else "no 'assumption' keyword in design.md",
    }


def extract_backbone_activities(out_dir: Path) -> list[str]:
    """Pull activity names from storymap.md (## Activity: lines) or storymap.csv col 1."""
    text = read_file(out_dir, "storymap.md") or ""
    acts = re.findall(r"^##\s*Activity:\s*(.+)$", text, re.MULTILINE)
    if acts:
        return [a.strip() for a in acts]
    # Fallback to csv
    csv_text = read_file(out_dir, "storymap.csv") or ""
    activities = []
    for line in csv_text.splitlines()[1:]:
        cols = line.split(",")
        if len(cols) > 1 and cols[1] and cols[1] not in activities:
            activities.append(cols[1])
    return activities


def grade_backbone_user_voice(out_dir: Path) -> dict:
    acts = extract_backbone_activities(out_dir)
    # Cross-cutting / non-backbone activities are explicitly not user-voice per
    # the skill's slicing guidance. Exclude them from this check the same way
    # slice-coverage does.
    backbone_acts = [a for a in acts if not a.strip().lower().startswith("non-backbone")]
    if len(backbone_acts) < 3:
        return {"text": "Backbone has 3+ activities written in user voice", "passed": False, "evidence": f"only {len(backbone_acts)} backbone activities: {backbone_acts}"}
    # Per-activity check: an activity is user-voice if it starts with or contains
    # a user verb. Pure system-shaped activities (no user verb, only system words)
    # are bad — e.g., "Login Module" or "Search API". An activity like "Discover
    # and evaluate the API" contains a user verb AND a tech noun, which is fine
    # — developers genuinely "evaluate the API".
    def classify(act: str) -> str:
        has_user_verb = bool(USER_VERBS.search(act))
        has_only_system = bool(SYSTEM_WORDS.search(act)) and not has_user_verb
        if has_only_system:
            return "system"
        if has_user_verb:
            return "user"
        return "neither"
    classifications = [(a, classify(a)) for a in backbone_acts]
    user_hits = [a for a, c in classifications if c == "user"]
    system_hits = [a for a, c in classifications if c == "system"]
    passed = len(backbone_acts) >= 3 and len(system_hits) == 0 and len(user_hits) >= max(1, len(backbone_acts) // 2)
    return {
        "text": "Backbone has 3+ activities written in user voice (verbs like 'find', 'submit', 'review'), not system voice (no 'API', 'service', 'module', 'database' as the only noun)",
        "passed": passed,
        "evidence": f"{len(backbone_acts)} backbone activities, {len(user_hits)} user-voice, {len(system_hits)} system-only. Backbone: {backbone_acts}",
    }


def _read_storymap_rows(out_dir: Path) -> tuple[list[str], list[dict]]:
    """Return (header, list of row-dicts) using proper CSV parsing."""
    text = read_file(out_dir, "storymap.csv") or ""
    if not text.strip():
        return [], []
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return [], []
    header = [c.strip().lower() for c in rows[0]]
    data = []
    for r in rows[1:]:
        if not r:
            continue
        # Pad short rows
        while len(r) < len(header):
            r.append("")
        data.append({header[i]: r[i] for i in range(len(header))})
    return header, data


def grade_first_slice_coverage(out_dir: Path) -> dict:
    header, rows = _read_storymap_rows(out_dir)
    if not rows:
        return {"text": "First slice includes story from every backbone activity", "passed": False, "evidence": "storymap.csv missing or empty"}
    if "slice" not in header or "activity" not in header:
        return {"text": "First slice includes story from every backbone activity", "passed": False, "evidence": f"unexpected header: {header}"}
    slice_first_choices = ["walking-skeleton", "pi-1", "pi1", "now", "mvp", "must"]
    slice_values_seen = [r["slice"].strip().lower() for r in rows if r["slice"].strip()]
    chosen = None
    for cand in slice_first_choices:
        if cand in slice_values_seen:
            chosen = cand
            break
    if chosen is None and slice_values_seen:
        chosen = slice_values_seen[0]
    # Only backbone activities count toward the coverage rule. Items in a
    # "Non-backbone:" or "Non-backbone /" activity are explicitly cross-cutting
    # per the skill's slicing guidance and must not be counted.
    def is_backbone(act: str) -> bool:
        a = act.strip().lower()
        return bool(a) and not a.startswith("non-backbone")
    all_activities = {r["activity"].strip() for r in rows if is_backbone(r["activity"])}
    first_slice_activities = {r["activity"].strip() for r in rows if r["slice"].strip().lower() == chosen and is_backbone(r["activity"])}
    missing = all_activities - first_slice_activities
    passed = bool(all_activities) and not missing
    return {
        "text": "First slice includes at least one story from EVERY backbone activity",
        "passed": passed,
        "evidence": f"first slice = {chosen!r}; covers {len(first_slice_activities)}/{len(all_activities)} backbone activities; missing: {sorted(missing)}",
    }


def grade_method_columns(out_dir: Path, method: str) -> dict:
    """Check backlog.csv carries the chosen prioritization method's columns.

    Accepts EITHER the wsjf_*-prefixed form (legacy) OR the canonical SAFe / RICE
    column names that the skill's prioritization-frameworks.md teaches. The agent
    will produce one or the other; both are valid.
    """
    text = read_file(out_dir, "backlog.csv") or ""
    # For each method, list ONE acceptable column-set; if the prefixed form isn't
    # found, fall back to the canonical form. Pass if either is fully present.
    columns_map = {
        "wsjf": (
            ["wsjf_value", "wsjf_time", "wsjf_risk", "wsjf_size"],          # prefixed form
            # Canonical SAFe WSJF inputs: cost-of-delay components + job size + score column.
            # Accept any of several common naming variants for each input.
            None,  # see below — WSJF canonical check uses keyword groups
        ),
        "rice": (
            ["rice_reach", "rice_impact", "rice_confidence", "rice_effort"],
            ["reach", "impact", "confidence", "effort", "rice_score"],
        ),
        "moscow": (["moscow"], ["moscow"]),
    }
    prefixed, canonical = columns_map[method]
    if not text.strip():
        return {"text": f"backlog.csv has {method.upper()} columns", "passed": False, "evidence": "backlog.csv missing or empty"}
    header = text.splitlines()[0].lower()
    prefixed_missing = [c for c in prefixed if c not in header]
    if method == "wsjf":
        # Canonical SAFe WSJF: need (user-business-value | bv) + (time-criticality | tc) +
        # (risk-reduction / opportunity-enablement | rroe | risk-reduction-opportunity-enablement)
        # + (job-size) + an overall wsjf score column.
        canonical_groups = [
            ("user_business_value", "business_value", "bv"),
            ("time_criticality", "tc"),
            ("risk_reduction_opportunity_enablement", "risk_reduction_opp_enablement", "risk_reduction", "rroe"),
            ("job_size", "size"),
            ("wsjf",),
        ]
        canonical_ok = all(any(name in header for name in group) for group in canonical_groups)
    else:
        canonical_ok = canonical is not None and all(c in header for c in canonical)
    passed = (not prefixed_missing) or canonical_ok
    if passed:
        evidence = "prefixed form" if not prefixed_missing else "canonical form"
    else:
        evidence = f"header: {header[:200]}; neither prefixed ({prefixed}) nor canonical form found"
    return {
        "text": f"backlog.csv contains {method.upper()} scoring columns (prefixed OR canonical SAFe/RICE form)",
        "passed": passed,
        "evidence": evidence,
    }


def grade_pi_terminology(out_dir: Path) -> dict:
    text = read_all_text(out_dir).lower()
    has = bool(re.search(r"\bpi[ -]?\d", text)) or "program increment" in text
    return {
        "text": "Slicing uses SAFe PI terminology (PI 1 / PI 2 / PI 3 or equivalent), since user explicitly mentioned PI planning",
        "passed": has,
        "evidence": "PI terminology found" if has else "no PI/program-increment terminology",
    }


def grade_non_goals_recorded(out_dir: Path, terms: list[str]) -> dict:
    text = read_all_text(out_dir).lower()
    found = [t for t in terms if t.lower() in text]
    passed = len(found) >= len(terms) - 1  # tolerate one missing
    return {
        "text": f"Non-goals from the brief recorded somewhere ({', '.join(terms)})",
        "passed": passed,
        "evidence": f"found: {found}",
    }


def grade_metrics_referenced(out_dir: Path, metric_strings: list[str]) -> dict:
    text = read_all_text(out_dir)
    found = [m for m in metric_strings if m in text]
    return {
        "text": f"References at least one quantitative target from the brief ({', '.join(metric_strings)})",
        "passed": len(found) >= 1,
        "evidence": f"found: {found}",
    }


def grade_jira_keys_preserved(out_dir: Path, keys: list[str]) -> dict:
    text = read_all_text(out_dir)
    found = [k for k in keys if k in text]
    return {
        "text": "All 18 original PROP-XXX Jira keys preserved somewhere in the outputs",
        "passed": len(found) == len(keys),
        "evidence": f"{len(found)}/{len(keys)} preserved; missing: {[k for k in keys if k not in found]}",
    }


def grade_orphans_surfaced(out_dir: Path) -> dict:
    text = read_all_text(out_dir).lower()
    keywords = ["prop-103", "prop-115", "prop-116", "dark mode", "localization", "tech debt", "tech-debt"]
    found = [k for k in keywords if k in text]
    return {
        "text": "Surfaces tech-debt / orphan items (mentions PROP-103, PROP-115, PROP-116, dark mode, or localization as needing separate treatment)",
        "passed": len(found) >= 2,
        "evidence": f"found: {found}",
    }


def grade_gstack_handoff(out_dir: Path) -> list[dict]:
    """Three assertions for the gstack-handoff eval."""
    text = read_all_text(out_dir)
    text_lower = text.lower()
    gstack_commands = ["/plan-ceo-review", "/plan-eng-review", "/plan-design-review", "/plan-devex-review", "/office-hours", "/autoplan"]
    named = [c for c in gstack_commands if c in text_lower]
    a1 = {
        "text": "Handoff message names at least 2 specific gstack slash commands",
        "passed": len(named) >= 2,
        "evidence": f"named: {named}",
    }
    # Check mapping: does the handoff explicitly tie a command to an output file?
    mapping_signals = [
        ("/plan-ceo-review" in text_lower and "design.md" in text_lower),
        ("/plan-eng-review" in text_lower and "storymap.md" in text_lower),
        ("/plan-devex-review" in text_lower and "backlog" in text_lower),
        ("/plan-design-review" in text_lower and ("persona" in text_lower or "design.md" in text_lower or "storymap.md" in text_lower)),
    ]
    a2 = {
        "text": "Handoff maps each named gstack command to a specific output file",
        "passed": sum(mapping_signals) >= 2,
        "evidence": f"command-to-file mapping signals: {sum(mapping_signals)}/4",
    }
    # Check no auto-invocation: look for actual auto-call language patterns,
    # not just any mention of "invoke". The skill itself says "do not auto-
    # invoke" so the word naturally appears in the negative.
    bad_patterns = re.compile(r"\b(running|executing|invoking|auto-running|auto-invoking|i'll (run|execute|invoke|call))\b\s+/(plan|office-hours|autoplan|ship|qa|canary|review)", re.IGNORECASE)
    no_auto = not bad_patterns.search(text)
    a3 = {
        "text": "Handoff does NOT auto-invoke gstack commands — only suggests them",
        "passed": no_auto,
        "evidence": "no auto-invocation language detected" if no_auto else f"matched: {bad_patterns.search(text).group(0) if bad_patterns.search(text) else ''}",
    }
    return [a1, a2, a3]


def grade_gsd_handoff(out_dir: Path) -> list[dict]:
    """Five assertions for the gsd-handoff eval."""
    text = read_all_text(out_dir)
    text_lower = text.lower()
    # Terminology-collision: must mention both "slice" and "Slice" with the collision explicitly
    collision_signals = [
        "collision" in text_lower,
        "terminology" in text_lower,
        ("gsd" in text_lower and "milestone" in text_lower and "slice" in text_lower),
    ]
    a1 = {
        "text": "Handoff explicitly names the GSD terminology collision (this skill's 'slice' = GSD 'Milestone')",
        "passed": sum(collision_signals) >= 2,
        "evidence": f"collision signals: {sum(collision_signals)}/3",
    }
    a2 = {
        "text": "Handoff maps design.md to GSD's Brief",
        "passed": "brief" in text_lower and "design.md" in text_lower,
        "evidence": "design.md → Brief mapping found" if ("brief" in text_lower and "design.md" in text_lower) else "missing",
    }
    gsd_commands = ["/gsd discuss", "/gsd plan-milestone", "/gsd auto", "/gsd next", "/gsd execute-task"]
    named = [c for c in gsd_commands if c in text_lower]
    a3 = {
        "text": "Handoff suggests a specific /gsd command",
        "passed": len(named) >= 1,
        "evidence": f"named: {named}",
    }
    # Check that no .gsd/ directory was written
    gsd_dir_written = any(p.exists() for p in [out_dir / ".gsd", out_dir / "outputs" / ".gsd"])
    a4 = {
        "text": "Handoff does NOT write into .gsd/ directly — only produces the canonical files",
        "passed": not gsd_dir_written,
        "evidence": ".gsd/ directory not present" if not gsd_dir_written else ".gsd/ directory was created",
    }
    # Check Now/Next/Later slicing
    csv_text = read_file(out_dir, "storymap.csv") or ""
    csv_lower = csv_text.lower()
    nnl_signals = ["now" in csv_lower, "next" in csv_lower, "later" in csv_lower]
    a5 = {
        "text": "Uses Now/Next/Later as the slicing strategy",
        "passed": sum(nnl_signals) >= 2,
        "evidence": f"Now/Next/Later signals in storymap.csv: {sum(nnl_signals)}/3",
    }
    return [a1, a2, a3, a4, a5]


def grade_interview_synthesis(out_dir: Path) -> list[dict]:
    """Six assertions for eval-11 (customer interview synthesis)."""
    text = read_all_text(out_dir)
    text_lower = text.lower()
    design = read_file(out_dir, "design.md") or ""

    # Verbatim quotes — look for distinctive customer-statement phrases
    verbatim_phrases = ["20-minute", "$100 auto-approve", "never use the bulk", "audit log is critical", "tableau", "2027 conversation", "would not trust"]
    found_verbatim = [p for p in verbatim_phrases if p.lower() in text_lower]
    a1 = {
        "text": "design.md includes verbatim quotes from interviews (extraction-fidelity check)",
        "passed": len(found_verbatim) >= 3,
        "evidence": f"verbatim phrases found: {found_verbatim}",
    }

    # Theme cluster signal
    cluster_signal = ("theme" in design.lower() or "cluster" in design.lower() or "n=" in design.lower() or "verbatim" in design.lower())
    a2 = {
        "text": "design.md has a theme/cluster section synthesizing across interviews",
        "passed": cluster_signal,
        "evidence": "found theme/cluster/verbatim section" if cluster_signal else "no synthesis evidence in design.md",
    }

    # 3 personas — Aisha/Marcus/Priya or CS Rep/CS Lead/Director
    persona_signals = sum([
        ("aisha" in text_lower or "cs rep" in text_lower),
        ("marcus" in text_lower or "cs lead" in text_lower),
        ("priya" in text_lower or "director" in text_lower),
    ])
    a3 = {
        "text": "All three interviewees surface as personas (or persona roles)",
        "passed": persona_signals == 3,
        "evidence": f"persona signals matched: {persona_signals}/3",
    }

    # Non-goals include anti-signals
    nongoals = sum([
        "auto-approv" in text_lower or "ai auto" in text_lower or "ai-auto" in text_lower or "trust" in text_lower,
        "self-serv" in text_lower or "customer self" in text_lower or "2027" in text_lower,
        "another tool" in text_lower or "new tool" in text_lower or "tabs" in text_lower,
    ])
    a4 = {
        "text": "Non-goals capture explicit anti-signals from interviews (AI auto-approval, customer self-service, new tool sprawl)",
        "passed": nongoals >= 2,
        "evidence": f"anti-signals captured: {nongoals}/3",
    }

    # Slice-1 ACs file present
    ac_file = (out_dir / "slice-1-acceptance-criteria.md").exists()
    a5 = {
        "text": "Produces slice-1-acceptance-criteria.md (per skill's Step 4a)",
        "passed": ac_file,
        "evidence": "file present" if ac_file else "missing",
    }

    # Now/Next/Later
    csv_text = read_file(out_dir, "storymap.csv") or ""
    nnl = sum(["now" in csv_text.lower(), "next" in csv_text.lower(), "later" in csv_text.lower()])
    a6 = {
        "text": "Uses Now/Next/Later slicing as user requested",
        "passed": nnl >= 2,
        "evidence": f"Now/Next/Later signals in storymap.csv: {nnl}/3",
    }

    return [a1, a2, a3, a4, a5, a6]


def grade_dependency_tracking(out_dir: Path) -> list[dict]:
    """Six assertions for eval-12 (dependency-aware backlog)."""
    text = read_all_text(out_dir)
    text_lower = text.lower()
    backlog = read_file(out_dir, "backlog.csv") or ""

    # depends_on column in backlog.csv
    has_deps_col = "depends_on" in backlog.lower()
    a1 = {
        "text": "backlog.csv has depends_on column",
        "passed": has_deps_col,
        "evidence": "depends_on column present" if has_deps_col else "missing",
    }

    # depends_on column populated (not all blank) — look for H: or S: or story-id refs
    dep_refs = sum(1 for line in backlog.splitlines() if "h:s-" in line.lower() or "s:s-" in line.lower() or "h:s0" in line.lower())
    a2 = {
        "text": "depends_on column has actual dependency entries (not all blank)",
        "passed": dep_refs >= 5,
        "evidence": f"dependency-formatted entries found: {dep_refs}",
    }

    # Cycle detection
    cycle_signal = ("cycle" in text_lower or "circular" in text_lower) and ("s-template" in text_lower)
    a3 = {
        "text": "S-TEMPLATE ↔ S-TEMPLATE-MGMT cycle is detected and surfaced (not silently broken)",
        "passed": cycle_signal,
        "evidence": "cycle terminology + S-TEMPLATE reference found" if cycle_signal else "missing",
    }

    # PI 1 feasibility check
    feasibility = ("feasibility" in text_lower or "feasible" in text_lower) and ("pi 1" in text_lower or "pi-1" in text_lower or "pi1" in text_lower)
    a4 = {
        "text": "PI-1 feasibility check is performed (dependencies of PI-1 stories also in PI-1)",
        "passed": feasibility,
        "evidence": "feasibility + PI-1 mentioned" if feasibility else "missing",
    }

    # All 14 stories preserved
    story_ids = ["S-AUTH", "S-PATIENT", "S-VIEW", "S-ANNOT", "S-SHARE", "S-NOTIFY", "S-RECEIVE", "S-AUDIT", "S-EXPORT", "S-RBAC", "S-EMRGY", "S-BULK", "S-TEMPLATE", "S-TEMPLATE-MGMT"]
    found = [s for s in story_ids if s in text]
    a5 = {
        "text": "All 14 user-provided story IDs preserved in outputs",
        "passed": len(found) >= 13,  # allow 1 missing for naming variation
        "evidence": f"{len(found)}/14 found",
    }

    # WSJF
    a6 = grade_method_columns(out_dir, "wsjf")

    return [a1, a2, a3, a4, a5, a6]


def grade_thin_brief_gap_discovery(out_dir: Path) -> list[dict]:
    """Six assertions for eval-14 (thin brief → gap-discovery via persona sim)."""
    text = read_all_text(out_dir)
    text_lower = text.lower()
    design = read_file(out_dir, "design.md") or ""
    handoff = read_file(out_dir, "handoff.md") or ""

    # Gap inventory in design.md
    a1 = {
        "text": "design.md has an explicit 'gaps' section listing what's blocking commitment",
        "passed": "gap" in design.lower(),
        "evidence": "gap section found" if "gap" in design.lower() else "missing",
    }

    # Source tagging (user-stated, simulated, inferred)
    tags = sum([
        "[user-stated]" in text or "user-stated" in text_lower,
        "[simulated" in text or "simulated:" in text_lower,
        "[inferred]" in text or "inferred" in text_lower,
    ])
    a2 = {
        "text": "Sources are tagged ([user-stated], [simulated: X], [inferred])",
        "passed": tags >= 2,
        "evidence": f"source tags found: {tags}/3",
    }

    # Conflict matrix or persona perspective table
    a3 = {
        "text": "design.md surfaces a persona conflict matrix or perspective table",
        "passed": "conflict" in design.lower() or "matrix" in design.lower() or "perspective" in design.lower(),
        "evidence": "conflict/matrix/perspective terminology found in design.md",
    }

    # Blocking decisions in handoff.md
    a4 = {
        "text": "handoff.md documents blocking decisions / smallest-next-decision",
        "passed": ("blocking" in handoff.lower() or "smallest next" in handoff.lower() or "next decision" in handoff.lower()),
        "evidence": "blocking/next-decision terminology found in handoff.md",
    }

    # Conditional commitments tagged with gap-ids
    gap_dep_tags = ("gap_dep" in text_lower or "gap-dep" in text_lower or "gap_dependency" in text_lower or "gap-dependency" in text_lower or re.search(r"gap.{0,5}\bg\d", text_lower) is not None)
    a5 = {
        "text": "Conditional commitments tagged with gap-ids (or equivalent)",
        "passed": gap_dep_tags,
        "evidence": "gap-id tagging found" if gap_dep_tags else "missing",
    }

    # All six files + slice-1 ACs
    files = list_files(out_dir)
    has_all = all(f in files for f in [f.lower() for f in REQUIRED_FILES_CANONICAL]) and ("slice-1-acceptance-criteria.md" in files)
    a6 = {
        "text": "All six canonical files + slice-1-acceptance-criteria.md produced",
        "passed": has_all,
        "evidence": f"files: {sorted(files)[:20]}",
    }

    return [a1, a2, a3, a4, a5, a6]


def grade_multi_stakeholder_conflict(out_dir: Path) -> list[dict]:
    """Six assertions for eval-15 (user-input-authoritative under conflict)."""
    text = read_all_text(out_dir)
    text_lower = text.lower()
    design = read_file(out_dir, "design.md") or ""
    csv_text = read_file(out_dir, "storymap.csv") or ""
    backlog = read_file(out_dir, "backlog.csv") or ""

    # Approval-gated env creation NOT in PI 1
    # Look for the story; check its slice
    has_approval_story = "approval" in csv_text.lower() and ("env" in csv_text.lower() or "creation" in csv_text.lower())
    pi1_has_approval = False
    if has_approval_story:
        for line in csv_text.splitlines()[1:]:
            cells = [c.strip().lower() for c in line.split(",")]
            joined = " ".join(cells)
            if "approval" in joined and ("env" in joined or "creation" in joined or "gate" in joined):
                # check slice column (index 6 typically)
                if len(cells) > 6 and ("pi-1" in cells[6] or "pi1" in cells[6] or cells[6] == "must"):
                    pi1_has_approval = True
                    break
    a1 = {
        "text": "Approval-gated env creation is NOT in PI 1 (user stance honored)",
        "passed": not pi1_has_approval,
        "evidence": "no approval-gated env story in PI 1" if not pi1_has_approval else "VIOLATION: approval story found in PI 1",
    }

    # User-input-authoritative explicitly mentioned/honored
    a2 = {
        "text": "User-input-authoritative principle explicitly invoked",
        "passed": ("user-input-authoritative" in text_lower or "user input" in text_lower and "authoritative" in text_lower or "vp eng" in text_lower or "vp engineering" in text_lower),
        "evidence": "principle explicitly invoked" if "user-input-authoritative" in text_lower else "VP Eng stance referenced",
    }

    # Platform-team objections logged as risk/future-slice (not silenced)
    a3 = {
        "text": "Platform-team objections logged as future-slice risk, not silenced",
        "passed": ("platform team" in text_lower and ("risk" in text_lower or "deferred" in text_lower or "pi 2" in text_lower or "pi-2" in text_lower or "future" in text_lower)),
        "evidence": "platform team objections preserved as risk/deferred",
    }

    # Conflict matrix in design.md
    a4 = {
        "text": "design.md has a conflict matrix showing how each conflict was resolved",
        "passed": ("conflict" in design.lower() and ("matrix" in design.lower() or "resolution" in design.lower() or "resolved" in design.lower())),
        "evidence": "conflict matrix / resolution terminology found",
    }

    # Decisions log captures the contested decisions
    a5 = {
        "text": "Decisions log captures contested decisions (approval-gated env creation deferred)",
        "passed": ("decisions log" in design.lower() or "decisions:" in design.lower()) and ("deferred" in design.lower() or "approval" in design.lower()),
        "evidence": "decisions log + deferred/approval mention found",
    }

    # WSJF columns
    a6 = grade_method_columns(out_dir, "wsjf")

    return [a1, a2, a3, a4, a5, a6]
    """Six assertions for eval-13 (OKR-aligned roadmap)."""
    text = read_all_text(out_dir)
    text_lower = text.lower()
    design = read_file(out_dir, "design.md") or ""
    backlog = read_file(out_dir, "backlog.csv") or ""

    # okr column in backlog.csv
    has_okr_col = "okr" in backlog.lower().splitlines()[0] if backlog.strip() else False
    a1 = {
        "text": "backlog.csv has okr column",
        "passed": has_okr_col,
        "evidence": "okr column present in header" if has_okr_col else "missing",
    }

    # okr column populated — look for KR-x.y references
    kr_refs = sum(1 for line in backlog.splitlines() if re.search(r"kr-?\d\.\d", line.lower()))
    a2 = {
        "text": "okr column has KR-x.y references populated",
        "passed": kr_refs >= 5,
        "evidence": f"KR-x.y references in backlog: {kr_refs}",
    }

    # OKR coverage matrix in design.md
    matrix_signal = "coverage" in design.lower() and ("kr-" in design.lower() or "kr " in design.lower())
    a3 = {
        "text": "design.md has an OKR coverage matrix",
        "passed": matrix_signal,
        "evidence": "coverage + KR mentioned in design.md" if matrix_signal else "missing",
    }

    # Orphan KRs surfaced — should call out KR-2.1, KR-2.2, KR-2.3 as belonging to other ARTs or surface gaps
    orphan_signal = ("orphan" in text_lower or "gap" in text_lower or "no coverage" in text_lower or "no platform" in text_lower or "another art" in text_lower or "other arts" in text_lower or "escalat" in text_lower)
    a4 = {
        "text": "Orphan KRs (KRs we own but have no story coverage) are surfaced",
        "passed": orphan_signal,
        "evidence": "orphan/gap terminology found" if orphan_signal else "missing",
    }

    # All 9 KRs referenced
    kr_ids = [f"KR-{o}.{i}" for o in (1, 2, 3) for i in (1, 2, 3)]
    found_krs = sum(1 for kr in kr_ids if kr in text or kr.lower() in text_lower or kr.replace("-", "") in text)
    a5 = {
        "text": "All 9 KRs (KR-1.1 through KR-3.3) referenced in outputs",
        "passed": found_krs >= 8,  # tolerance for one naming variation
        "evidence": f"{found_krs}/9 KRs referenced",
    }

    # WSJF
    a6 = grade_method_columns(out_dir, "wsjf")

    return [a1, a2, a3, a4, a5, a6]


def grade_okr_alignment(out_dir: Path) -> list[dict]:
    """Six assertions for eval-13 (OKR-aligned roadmap)."""
    text = read_all_text(out_dir)
    text_lower = text.lower()
    design = read_file(out_dir, "design.md") or ""
    backlog = read_file(out_dir, "backlog.csv") or ""

    has_okr_col = "okr" in backlog.lower().splitlines()[0] if backlog.strip() else False
    a1 = {
        "text": "backlog.csv has okr column",
        "passed": has_okr_col,
        "evidence": "okr column present in header" if has_okr_col else "missing",
    }
    kr_refs = sum(1 for line in backlog.splitlines() if re.search(r"kr-?\d\.\d", line.lower()))
    a2 = {
        "text": "okr column has KR-x.y references populated",
        "passed": kr_refs >= 5,
        "evidence": f"KR-x.y references in backlog: {kr_refs}",
    }
    matrix_signal = "coverage" in design.lower() and ("kr-" in design.lower() or "kr " in design.lower())
    a3 = {
        "text": "design.md has an OKR coverage matrix",
        "passed": matrix_signal,
        "evidence": "coverage + KR mentioned in design.md" if matrix_signal else "missing",
    }
    orphan_signal = ("orphan" in text_lower or "gap" in text_lower or "no coverage" in text_lower or "no platform" in text_lower or "another art" in text_lower or "other arts" in text_lower or "escalat" in text_lower)
    a4 = {
        "text": "Orphan KRs (KRs we own but have no story coverage) are surfaced",
        "passed": orphan_signal,
        "evidence": "orphan/gap terminology found" if orphan_signal else "missing",
    }
    kr_ids = [f"KR-{o}.{i}" for o in (1, 2, 3) for i in (1, 2, 3)]
    found_krs = sum(1 for kr in kr_ids if kr in text or kr.lower() in text_lower or kr.replace("-", "") in text)
    a5 = {
        "text": "All 9 KRs (KR-1.1 through KR-3.3) referenced in outputs",
        "passed": found_krs >= 8,
        "evidence": f"{found_krs}/9 KRs referenced",
    }
    a6 = grade_method_columns(out_dir, "wsjf")
    return [a1, a2, a3, a4, a5, a6]


def grade_snapshot_breaks_limits(out_dir: Path) -> list[dict]:
    """Eight assertions for eval-16 (Mode D snapshot + breach detection)."""
    text = read_all_text(out_dir)
    text_lower = text.lower()
    handoff = read_file(out_dir, "handoff.md") or ""

    a1 = {
        "text": "Output includes a snapshot of current state (capacity used / remaining / cap)",
        "passed": "snapshot" in text_lower and ("capacity" in text_lower or "sp" in text_lower or "remaining" in text_lower),
        "evidence": "snapshot terminology + capacity/SP found",
    }
    breach_terms = sum([
        "breach" in text_lower,
        "overrun" in text_lower or "over capacity" in text_lower or "underwater" in text_lower,
        "trade-off" in text_lower or "tradeoff" in text_lower or "option a" in text_lower or "option b" in text_lower,
        "what gives" in text_lower or "decision needed" in text_lower or "your decision" in text_lower,
    ])
    a2 = {
        "text": "Breaches surfaced with explicit trade-off options (not silently absorbed)",
        "passed": breach_terms >= 3,
        "evidence": f"breach-language signals: {breach_terms}/4",
    }
    a3 = {
        "text": "Capacity breach analyzed (PI-1 remaining capacity vs new SCIM work)",
        "passed": ("50 sp" in text_lower or "50sp" in text_lower or "remaining" in text_lower) and ("25 sp" in text_lower or "scim" in text_lower),
        "evidence": "capacity + SCIM SP arithmetic referenced",
    }
    new_activity = ("provision" in text_lower and ("tenant" in text_lower or "user" in text_lower)) and ("backbone" in text_lower or "activity" in text_lower or "slice" in text_lower)
    a4 = {
        "text": "New backbone activity 'Provision tenant users' handled per slice-1 rule (decision required, not silent acceptance)",
        "passed": new_activity,
        "evidence": "new activity + backbone/slice terminology present",
    }
    deadline = ("soc 2" in text_lower or "soc2" in text_lower or "kr-1.1" in text_lower) and ("5 weeks" in text_lower or "deadline" in text_lower or "audit window" in text_lower or "racing" in text_lower or "collide" in text_lower or "scim" in text_lower)
    a5 = {
        "text": "SOC 2 audit deadline vs SCIM EOQ deadline collision is surfaced",
        "passed": deadline,
        "evidence": "SOC 2 + deadline collision referenced",
    }
    f_scim_stories = sum(1 for line in text.splitlines() if "f-scim" in line.lower()) >= 3
    a6 = {
        "text": "F-SCIM decomposed into specific stories (3+ stories referenced)",
        "passed": f_scim_stories,
        "evidence": "3+ F-SCIM story references found",
    }
    kr21_risk = ("kr-2.1" in text_lower or "kr2.1" in text_lower) and ("displace" in text_lower or "cut" in text_lower or "risk" in text_lower or "slip" in text_lower or "re-baseline" in text_lower or "rebaseline" in text_lower)
    a7 = {
        "text": "KR-2.1 displacement risk surfaced (if any KR-2.1 story is cut for SCIM)",
        "passed": kr21_risk,
        "evidence": "KR-2.1 + displacement/risk/cut/slip terminology found",
    }
    diff_format = ("added:" in handoff.lower() or "added " in handoff.lower()) or ("changes from" in handoff.lower() or "diff" in handoff.lower() or "before/after" in handoff.lower() or "moved:" in handoff.lower())
    a8 = {
        "text": "handoff.md includes a diff-style summary of changes (ADDED / MOVED / CUT / UNCHANGED)",
        "passed": diff_format,
        "evidence": "diff-style terminology found in handoff.md",
    }
    return [a1, a2, a3, a4, a5, a6, a7, a8]


def grade_run(eval_id: int, out_dir: Path) -> list[dict]:
    """Return list of expectation dicts for one run."""
    results = []
    results.append(grade_canonical_files(out_dir))
    results.append(grade_csv_header(out_dir))
    results.append(grade_mermaid(out_dir))
    results.append(grade_personas(out_dir))

    if eval_id == 1:
        results.append(grade_outcome(out_dir))
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        results.append(grade_assumptions(out_dir))
        results.append(grade_method_columns(out_dir, "wsjf"))
        results.append(grade_pi_terminology(out_dir))
    elif eval_id == 2:
        results.append(grade_outcome(out_dir))
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        results.append(grade_method_columns(out_dir, "rice"))
        results.append(grade_non_goals_recorded(out_dir, ["web onboarding", "enterprise SSO", "gamification"]))
        results.append(grade_metrics_referenced(out_dir, ["60%", "41%", "47%", "22%", "73%", "82%"]))
    elif eval_id == 3:
        results.append(grade_outcome(out_dir))
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        results.append(grade_method_columns(out_dir, "moscow"))
        prop_keys = [f"PROP-{n}" for n in range(101, 119)]
        results.append(grade_jira_keys_preserved(out_dir, prop_keys))
        results.append(grade_orphans_surfaced(out_dir))
    elif eval_id == 4:
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        results.append(grade_method_columns(out_dir, "wsjf"))
        results.extend(grade_gstack_handoff(out_dir))
    elif eval_id == 5:
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        results.extend(grade_gsd_handoff(out_dir))
    elif eval_id == 11:
        results.extend(grade_interview_synthesis(out_dir))
    elif eval_id == 12:
        results.extend(grade_dependency_tracking(out_dir))
    elif eval_id == 13:
        results.extend(grade_okr_alignment(out_dir))
    elif eval_id == 14:
        results.extend(grade_thin_brief_gap_discovery(out_dir))
    elif eval_id == 15:
        results.extend(grade_multi_stakeholder_conflict(out_dir))
    elif eval_id == 16:
        # Mode D eval skips canonical/header checks; only snapshot-specific
        results = []
        results.extend(grade_snapshot_breaks_limits(out_dir))
    elif eval_id == 6:
        results.append(grade_outcome(out_dir))
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        csv_text = read_file(out_dir, "storymap.csv") or ""
        nnl_signals = sum(["now" in csv_text.lower(), "next" in csv_text.lower(), "later" in csv_text.lower()])
        results.append({
            "text": "Uses Now/Next/Later slicing as user requested",
            "passed": nnl_signals >= 2,
            "evidence": f"Now/Next/Later signals: {nnl_signals}/3",
        })
        text = read_all_text(out_dir).lower()
        results.append({
            "text": "Backbone in developer voice (install/integrate/handle errors)",
            "passed": any(w in text for w in ["install", "integrate", "make first call", "handle error", "go to production", "discover"]),
            "evidence": "developer-journey verbs found",
        })
    elif eval_id == 7:
        results.append(grade_outcome(out_dir))
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        results.append(grade_method_columns(out_dir, "wsjf"))
        text = read_all_text(out_dir).lower()
        results.append({
            "text": "Desktop concerns addressed (install / auto-update / code-signing / keychain)",
            "passed": sum([w in text for w in ["install", "auto-update", "auto update", "signing", "keychain", "offline"]]) >= 3,
            "evidence": "3+ desktop-specific concerns found",
        })
    elif eval_id == 8:
        results.append(grade_outcome(out_dir))
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        results.append(grade_method_columns(out_dir, "wsjf"))
        text = read_all_text(out_dir).lower()
        results.append({
            "text": "Two distinct personas (Tenant Admin AND End User) surface in outputs",
            "passed": (("tenant admin" in text or "tenant-admin" in text) and ("end user" in text or "end-user" in text)),
            "evidence": "both personas surface",
        })
        results.append({
            "text": "SOC 2 / SAML / SCIM / RBAC requirements addressed",
            "passed": sum([w in text for w in ["soc 2", "soc2", "saml", "scim", "rbac"]]) >= 3,
            "evidence": "3+ enterprise requirements addressed",
        })
    elif eval_id == 9:
        results.append(grade_outcome(out_dir))
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        results.append(grade_method_columns(out_dir, "moscow"))
        text = read_all_text(out_dir).lower()
        results.append({
            "text": "Distribution channels (brew / scoop / apt / cargo / GitHub releases) addressed",
            "passed": sum([w in text for w in ["brew", "scoop", "apt", "cargo", "github release"]]) >= 3,
            "evidence": "3+ distribution channels mentioned",
        })
    elif eval_id == 10:
        results.append(grade_outcome(out_dir))
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        results.append(grade_method_columns(out_dir, "rice"))
        csv_text = read_file(out_dir, "storymap.csv") or ""
        results.append({
            "text": "Slicing as MVP / R2 (retention) / R3 (growth) per user framing",
            "passed": "mvp" in csv_text.lower() and ("r2" in csv_text.lower() or "retention" in csv_text.lower()) and ("r3" in csv_text.lower() or "growth" in csv_text.lower()),
            "evidence": "MVP/R2/R3 slicing found",
        })
    elif eval_id == 17:
        design = read_file(out_dir, "design.md") or ""
        text = read_all_text(out_dir).lower()
        results.append({
            "text": "design.md contains 'Context loop trace' section",
            "passed": "context loop trace" in design.lower() or ("loop" in design.lower() and "trace" in design.lower()),
            "evidence": "loop trace section found",
        })
        results.append({
            "text": "Loop short-circuited (early-exit / empty-dir signal documented)",
            "passed": any(t in text for t in ["short-circuit", "exited early", "empty dir", "empty working", "no codebase", "early exit", "exit"]) and "loop" in text,
            "evidence": "early-exit signal found",
        })
        results.append({
            "text": "Spends saved budget on persona simulation (ADHD persona)",
            "passed": "persona" in text and ("adhd" in text or "simulat" in text),
            "evidence": "persona-sim + ADHD context found",
        })
        csv_text = read_file(out_dir, "storymap.csv") or ""
        story_count = max(0, len(csv_text.splitlines()) - 1)
        results.append({
            "text": "Story count ~15-25 (discovery scope, not detailed PI planning)",
            "passed": 12 <= story_count <= 30,
            "evidence": f"{story_count} stories",
        })
        nnl_signals = sum(["now" in csv_text.lower(), "next" in csv_text.lower(), "later" in csv_text.lower()])
        results.append({
            "text": "Uses Now/Next/Later slicing as user requested",
            "passed": nnl_signals >= 2,
            "evidence": f"NNL signals: {nnl_signals}/3",
        })
    elif eval_id == 18:
        design = read_file(out_dir, "design.md") or ""
        text = read_all_text(out_dir).lower()
        handoff = read_file(out_dir, "handoff.md") or ""
        results.append({
            "text": "design.md has 'Backbone criteria' section with 6 rows (Frame/Persona/Time/Granularity/Scope/Aggregation)",
            "passed": "backbone criteria" in design.lower() and all(w in design.lower() for w in ["frame", "persona", "horizon", "granularity", "scope", "aggregation"]),
            "evidence": "criteria table present" if "backbone criteria" in design.lower() else "missing",
        })
        results.append({
            "text": "Reads .gsd/ artifacts first (source-tags Brief / Roadmap / Decisions)",
            "passed": ".gsd" in text or "decision 0001" in text or "from .gsd" in text or "d0001" in text,
            "evidence": ".gsd-sourced content found",
        })
        results.append({
            "text": "Perspective question defaulted to consultant-only with rationale + override-pending tag",
            "passed": ("default applied" in text or "override pending" in text or "consultant-only" in text or "consultant only" in text),
            "evidence": "default disclosure found",
        })
        results.append({
            "text": "Honors Decision 0001 (single-user constraint)",
            "passed": "single-user" in text or "single user" in text or "decision 0001" in text,
            "evidence": "single-user constraint preserved",
        })
        csv_text = read_file(out_dir, "storymap.csv") or ""
        results.append({
            "text": "Uses M1/M2/M3 slicing per existing GSD Roadmap",
            "passed": ("m1" in csv_text.lower() or "milestone 1" in csv_text.lower() or "m-1" in csv_text.lower()),
            "evidence": "M-slice naming present",
        })
        results.append({
            "text": "handoff.md has Mode D diff (NEW vs ALREADY-IN-GSD)",
            "passed": ("new" in handoff.lower() and ("already" in handoff.lower() or "diff" in handoff.lower() or "from .gsd" in handoff.lower())),
            "evidence": "Mode D diff format found",
        })
    elif eval_id == 19:
        # Output routing — from-scratch branch
        handoff = read_file(out_dir, "handoff.md") or ""
        text = read_all_text(out_dir).lower()
        results.append(grade_outcome(out_dir))
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        results.append(grade_method_columns(out_dir, "moscow"))
        results.append({
            "text": "Routes to from-scratch branch (mentions from-scratch detection / tracker seeding)",
            "passed": any(t in text for t in ["from-scratch", "from scratch", "seed the tracker", "seed a tracker", "seed tracker"]),
            "evidence": "from-scratch routing signal found",
        })
        results.append({
            "text": "Generates a tracker import command/script (gh / az boards / Jira CSV / Linear)",
            "passed": any(t in text for t in ["gh issue create", "gh project", "az boards", "jira csv", "jira import", "linear import", "import script", "bulk-import", "bulk import"]),
            "evidence": "tracker import mechanics named",
        })
        results.append({
            "text": "Does NOT auto-run the import script (asks user to run it)",
            "passed": any(t in handoff.lower() for t in ["don't auto-run", "do not auto-run", "you run it", "run this when", "not run", "have not run", "haven't run", "run the script", "user to run", "you to run", "review before running", "run when ready"]) or ("script" in handoff.lower() and "not" in handoff.lower()),
            "evidence": "explicit non-execution signal",
        })
        results.append({
            "text": "References .user-story-mapping/state.json for Mode-D continuity",
            "passed": ".user-story-mapping" in text or "state.json" in text,
            "evidence": ".user-story-mapping reference found",
        })
        results.append({
            "text": "TODO.md is NOT the primary destination (from-scratch → tracker is system of record)",
            "passed": not (re.search(r"todo\.md", handoff.lower()) and "primary" in handoff.lower()),
            "evidence": "TODO.md not designated as primary",
        })
    elif eval_id == 20:
        # Output routing — existing-project cascade
        handoff = read_file(out_dir, "handoff.md") or ""
        text = read_all_text(out_dir).lower()
        results.append(grade_outcome(out_dir))
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        results.append(grade_method_columns(out_dir, "wsjf"))
        results.append({
            "text": "Routes to existing-project keep-in-place cascade",
            "passed": any(t in text for t in ["existing project", "existing-project", "keep-in-place", "keep in place", "in-place", "cascade"]),
            "evidence": "existing-project routing signal found",
        })
        results.append({
            "text": "Writes slice-1 to TODO.md (no framework state available)",
            "passed": "todo.md" in text or "todo md" in text,
            "evidence": "TODO.md destination found",
        })
        results.append({
            "text": "Honors user's no-tracker constraint (no gh issue create / no GitHub bulk import)",
            "passed": not any(t in text for t in ["gh issue create", "gh project create", "bulk-create", "bulk create"]) or "do not push" in text or "not push" in text or "won't push" in text or "skip tracker" in text,
            "evidence": "tracker-push avoided",
        })
        results.append({
            "text": "Handoff line names TODO.md as the destination",
            "passed": "todo.md" in handoff.lower() and any(t in handoff.lower() for t in ["→", "written to", "wrote to", "landed in", "destination"]),
            "evidence": "TODO.md named in handoff",
        })
    elif eval_id == 21:
        # Step 0.5 — progress reconciliation
        text = read_all_text(out_dir).lower()
        design = read_file(out_dir, "design.md") or ""
        storymap = read_file(out_dir, "storymap.md") or ""
        handoff = read_file(out_dir, "handoff.md") or ""
        # Story IDs live in CSV, not in storymap.md prose. Use tracker IDs (PROJ-101..104 etc.) as proxy.
        results.append({
            "text": "Step 0.5 ran (design.md has Implementation status or Activity status section)",
            "passed": ("implementation status" in design.lower() or "activity status" in design.lower()),
            "evidence": "Step 0.5 section header found in design.md",
        })
        done_count = sum(p in storymap for p in ("PROJ-101", "PROJ-102", "PROJ-103", "PROJ-104"))
        results.append({
            "text": "Sign-in tracker items (PROJ-101..104) marked status:done",
            "passed": done_count >= 3 and ("status: done" in storymap.lower() or "status:done" in storymap.lower()),
            "evidence": f"{done_count}/4 PROJ-10x IDs present + status:done annotation",
        })
        results.append({
            "text": "Activity 'Sign in' graduated (## Shipped foundation or GRADUATED mention)",
            "passed": any(t in storymap.lower() for t in ["shipped foundation", "graduated"]) and "sign in" in storymap.lower(),
            "evidence": "graduation signal on Sign in activity",
        })
        progress_in_progress = "in-progress" in storymap.lower() and (
            ("PROJ-105" in storymap or "PROJ-106" in storymap)
            or ("find-by-id" in storymap.lower() or "find-by-email" in storymap.lower())
        )
        results.append({
            "text": "Find-transaction items (PROJ-105/106) marked status:in-progress (active branches)",
            "passed": progress_in_progress,
            "evidence": "in-progress status on Find-transaction stories",
        })
        deferred_count = sum(p in storymap for p in ("PROJ-109", "PROJ-110", "PROJ-112"))
        results.append({
            "text": "Approver + late-audit items (PROJ-109/110/112) marked status:deferred (Fix Version pushed)",
            "passed": "deferred" in storymap.lower() and deferred_count >= 2,
            "evidence": f"deferred status; {deferred_count}/3 PROJ-1XX IDs present",
        })
        results.append({
            "text": "Orphan tracker items (PROJ-113/114/115) surfaced in handoff drift section",
            "passed": ("detected drift" in handoff.lower() or "orphan" in handoff.lower()) and sum(p in handoff for p in ["PROJ-113", "PROJ-114", "PROJ-115"]) >= 2,
            "evidence": "orphan tracker items listed",
        })
        results.append({
            "text": "Graduated activity excluded from active slice-1 coverage requirement",
            "passed": "active backbone" in text or "active backbone activities" in text or "excluded from active slicing" in text or "graduated activities don't" in text,
            "evidence": "active-vs-graduated distinction documented",
        })
        results.append({
            "text": "Any tracker-status-update script generated is NOT auto-run",
            "passed": ("tracker-status-update" not in text) or any(t in text for t in ["don't auto-run", "do not auto-run", "review before running", "user runs", "you run"]),
            "evidence": "no auto-execution of write-back script",
        })
    elif eval_id == 22:
        # Per-persona slice-1 coverage enforcement
        text = read_all_text(out_dir).lower()
        design = read_file(out_dir, "design.md") or ""
        csv_text = read_file(out_dir, "storymap.csv") or ""
        results.append({
            "text": "Design doc names all three personas (Business Owner, Accountant, Customer)",
            "passed": all(p in design.lower() for p in ["business owner", "accountant", "customer"]),
            "evidence": "three personas present in design.md",
        })
        # Per-persona slice-1 coverage check via CSV — use csv.reader to handle quoted commas in story column.
        slice1_personas = set()
        if csv_text.strip():
            reader = csv.reader(io.StringIO(csv_text))
            header = next(reader, [])
            # Find column indices defensively (schema may have added columns).
            try:
                persona_idx = header.index("persona")
                slice_idx = header.index("slice")
            except ValueError:
                persona_idx, slice_idx = 4, 6  # legacy default
            for row in reader:
                if len(row) > max(persona_idx, slice_idx):
                    sv = row[slice_idx].strip().lower()
                    if sv in ("1", "slice-1", "walking-skeleton", "skeleton", "mvp"):
                        slice1_personas.add(row[persona_idx].strip().lower())
        # "slice 1" can be either walking-skeleton or mvp depending on the run's slicing interpretation;
        # the eval prompt says "walking-skeleton" but agents sometimes fold walking-skeleton+mvp into slice-1.
        covers_all_3 = sum(any(p in sp for sp in slice1_personas) for p in ["owner", "accountant", "customer"]) >= 3
        results.append({
            "text": "Slice-1 includes ≥1 story per persona (Business Owner + Accountant + Customer)",
            "passed": covers_all_3,
            "evidence": f"slice-1 personas: {sorted(slice1_personas)[:10]}",
        })
        results.append({
            "text": "Any missing-persona case flagged in design doc (forced re-check, not silent drop)",
            "passed": covers_all_3 or any(t in design.lower() for t in ["forced re-check", "re-run step 1", "re-run step 3", "persona has zero", "no slice-1 story for"]),
            "evidence": "forced re-check disclosure" if not covers_all_3 else "all three personas covered (re-check not needed)",
        })
        results.append({
            "text": "Stories tagged with source where applicable ([simulated]/[inferred]/[interview: ...])",
            "passed": any(t in design.lower() for t in ["[simulated", "[inferred", "[interview"]) or any(t in csv_text.lower() for t in ["[simulated", "[inferred", "[interview"]),
            "evidence": "source-tag conventions used",
        })
        results.append(grade_method_columns(out_dir, "moscow"))
        results.append({
            "text": "Walking-skeleton slicing terminology used (not PI-1)",
            "passed": "walking" in text or "skeleton" in text,
            "evidence": "walking-skeleton terminology found",
        })
    elif eval_id == 23:
        # Step 2.5 — role hints
        text = read_all_text(out_dir).lower()
        role_hints = read_file(out_dir, "role-hints.md") or ""
        results.append({
            "text": "role-hints.md is produced as a top-level artifact",
            "passed": bool(role_hints) and len(role_hints) > 200,
            "evidence": f"role-hints.md present ({len(role_hints)} chars)" if role_hints else "missing",
        })
        results.append({
            "text": "role-hints.md has a UX/UI designer section (persona snapshots / flow inventory / open UX questions)",
            "passed": any(t in role_hints.lower() for t in ["ux/ui designer", "ux designer", "for the ux", "designer:", "for ux", "## ux"]) and any(t in role_hints.lower() for t in ["persona snapshot", "flow inventory", "open ux", "ux questions", "friction"]),
            "evidence": "UX section + at least one expected sub-heading",
        })
        results.append({
            "text": "role-hints.md has an architect section (cross-cutting / boundaries / open architecture questions)",
            "passed": any(t in role_hints.lower() for t in ["for the architect", "architect:", "## architect"]) and any(t in role_hints.lower() for t in ["cross-cutting", "boundary candidate", "open architecture", "architecture questions", "risky integration"]),
            "evidence": "architect section + at least one expected sub-heading",
        })
        results.append({
            "text": "HIPAA constraint surfaced (architect / cross-cutting hint)",
            "passed": "hipaa" in role_hints.lower() or "hipaa" in text,
            "evidence": "HIPAA referenced",
        })
        results.append({
            "text": "PCI constraint surfaced for billing flow",
            "passed": "pci" in role_hints.lower() or "pci" in text,
            "evidence": "PCI referenced",
        })
        results.append({
            "text": "Twilio + Stripe noted as risky integrations with risk notes",
            "passed": all(t in role_hints.lower() for t in ["twilio", "stripe"]) and any(t in role_hints.lower() for t in ["risk", "rate limit", "webhook", "deliverability"]),
            "evidence": "both third parties + risk note",
        })
        results.append({
            "text": "Skill-chaining attempted or 'no advisor skill installed' noted for at least one flow",
            "passed": any(t in role_hints.lower() for t in ["[skill:", "no advisor skill installed", "would benefit from domain expertise", "advisor skill"]),
            "evidence": "skill-chaining outcome documented",
        })
        # RICE column naming varies: canonical is reach/impact/confidence/effort/rice_score; some teams use rice_reach/etc.
        backlog_csv = read_file(out_dir, "backlog.csv") or ""
        header = backlog_csv.splitlines()[0].lower() if backlog_csv.strip() else ""
        rice_canonical = all(c in header for c in ("reach", "impact", "confidence", "effort", "rice_score"))
        rice_prefixed = all(c in header for c in ("rice_reach", "rice_impact", "rice_confidence", "rice_effort"))
        results.append({
            "text": "backlog.csv contains RICE scoring columns (reach/impact/confidence/effort + rice_score, OR rice_*-prefixed)",
            "passed": rice_canonical or rice_prefixed,
            "evidence": f"header: {header[:200]}",
        })
    elif eval_id == 24:
        # Plan-stage auto-trigger via gstack /office-hours cue
        handoff = read_file(out_dir, "handoff.md") or ""
        text = read_all_text(out_dir).lower()
        results.append({
            "text": "Auto-activates on gstack /office-hours cue (storymap.md produced, not just free-form discussion)",
            "passed": bool(read_file(out_dir, "storymap.md")),
            "evidence": "storymap.md present",
        })
        results.append(grade_backbone_user_voice(out_dir))
        results.append(grade_first_slice_coverage(out_dir))
        results.append(grade_method_columns(out_dir, "wsjf"))
        results.append({
            "text": "Handoff references gstack /plan-*-review commands",
            "passed": ("/plan-ceo-review" in handoff.lower() or "/plan-eng-review" in handoff.lower() or "/plan-design-review" in handoff.lower() or "/plan-devex-review" in handoff.lower()) and ("/plan-" in handoff.lower()),
            "evidence": "gstack plan-review commands named",
        })
        results.append({
            "text": "Backbone uses user-voice verbs (search/save/get-notified/etc.)",
            "passed": any(v in text for v in ["search", "save", "subscribe", "get notified", "browse", "explore"]),
            "evidence": "user-voice verbs found",
        })
    elif eval_id == 25:
        # Tracker write-back script emitted
        text = read_all_text(out_dir).lower()
        handoff = read_file(out_dir, "handoff.md") or ""
        storymap = read_file(out_dir, "storymap.md") or ""
        script_text = ""
        for name in ("tracker-status-update.sh", "tracker-status-update.md", "tracker-status-update.bash", "tracker-status-update.ps1"):
            t = read_file(out_dir, name)
            if t:
                script_text = t
                break
        # Use tracker IDs (CMS-106, CMS-107) as the canonical lookup — storymap.md story lines often don't carry S0XX IDs.
        results.append({
            "text": "Step 0.5 ran (status reconciliation against prior storymap + tracker)",
            "passed": "status: " in storymap.lower() or "status:" in storymap.lower() or "implementation status" in (read_file(out_dir, "design.md") or "").lower(),
            "evidence": "status annotations or implementation-status section present",
        })
        results.append({
            "text": "CMS-106 (S006) marked status:cut",
            "passed": "cms-106" in storymap.lower() and ("status: cut" in storymap.lower() or "status:cut" in storymap.lower()),
            "evidence": "CMS-106 marked cut in storymap",
        })
        results.append({
            "text": "CMS-107 (S007) marked status:deferred",
            "passed": "cms-107" in storymap.lower() and ("status: deferred" in storymap.lower() or "status:deferred" in storymap.lower()),
            "evidence": "CMS-107 marked deferred in storymap",
        })
        results.append({
            "text": "tracker-status-update.* script generated as a separate file",
            "passed": bool(script_text),
            "evidence": f"script file present ({len(script_text)} chars)" if script_text else "no tracker-status-update.* file found",
        })
        results.append({
            "text": "Script contains Jira CLI transition for CMS-106 (cut)",
            "passed": bool(script_text) and "cms-106" in script_text.lower() and any(t in script_text.lower() for t in ["won't do", "wontfix", "wont-fix", "transition", "close"]),
            "evidence": "CMS-106 cut operation",
        })
        results.append({
            "text": "Script contains Fix Version push for CMS-107 to PI-2",
            "passed": bool(script_text) and "cms-107" in script_text.lower() and any(t in script_text.lower() for t in ["pi-2", "pi_2", "fix-version", "fixversion", "fix version"]),
            "evidence": "CMS-107 deferral operation",
        })
        results.append({
            "text": "Script contains create operations for two new stories (permission boundary check + rate-limit)",
            "passed": bool(script_text) and any(t in script_text.lower() for t in ["jira issue create", "issue create", "create issue", "new-item", "create-issue"]) and ("permission" in script_text.lower() or "rate-limit" in script_text.lower() or "rate limit" in script_text.lower()),
            "evidence": "new-story create operations",
        })
        results.append({
            "text": "Script header / docs explicitly say it is NOT auto-executed (must be reviewed)",
            "passed": bool(script_text) and any(t in script_text.lower() for t in ["review before", "do not auto", "don't auto", "manually", "you run", "user runs", "review this"]),
            "evidence": "non-execution disclaimer in script",
        })
        results.append({
            "text": "Handoff line names tracker-status-update.* as an output to review",
            "passed": ("tracker-status-update" in handoff.lower()) and ("review" in handoff.lower() or "before running" in handoff.lower()),
            "evidence": "handoff references the script + review prompt",
        })

    return results


def main() -> int:
    evals = json.loads(EVALS_PATH.read_text(encoding="utf-8"))["evals"]
    eval_dirs = sorted(ITERATION.iterdir())
    summary = []
    for eval_dir in eval_dirs:
        if not eval_dir.is_dir() or not eval_dir.name.startswith("eval-"):
            continue
        eval_id = int(eval_dir.name.split("-")[1])
        for run_name in ("with_skill", "without_skill"):
            run_dir = eval_dir / run_name
            out_dir = run_dir / "outputs"
            if not out_dir.exists():
                print(f"missing: {out_dir}", file=sys.stderr)
                continue
            expectations = grade_run(eval_id, out_dir)
            passed = sum(1 for e in expectations if e["passed"])
            total = len(expectations)
            grading_path = run_dir / "grading.json"
            grading_path.write_text(
                json.dumps({"expectations": expectations}, indent=2), encoding="utf-8"
            )
            print(f"{eval_dir.name}/{run_name}: {passed}/{total} passed")
            summary.append({"eval_dir": eval_dir.name, "run": run_name, "passed": passed, "total": total})
    return 0


if __name__ == "__main__":
    sys.exit(main())
