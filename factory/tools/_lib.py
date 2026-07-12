"""Shared library for tools/agent/* factory scripts.

Design rules (see tools/agent/README.md):
- python3 stdlib only (no PyYAML, no pip installs)
- forgiving YAML-subset parser sized to our known file shapes
  (.factory/config.yaml, .factory/work-orders/*/state.yaml, doc front matter)
- exit codes are gates; error messages name the next action
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Repo layout
# ---------------------------------------------------------------------------

def repo_root():
    """tools/agent/_lib.py lives two levels below the repo root."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def config_path():
    return os.path.join(repo_root(), ".factory", "config.yaml")


def load_config():
    path = config_path()
    if not os.path.isfile(path):
        die(".factory/config.yaml not found — restore it from version control before "
            "running factory tools.")
    with open(path, encoding="utf-8") as f:
        return parse_yaml(f.read())


def wo_dir(wo_id, cfg=None):
    base = (cfg or {}).get("paths", {}).get("work_orders", ".factory/work-orders")
    return os.path.join(repo_root(), base, wo_id)


def templates_dir(cfg=None):
    base = (cfg or {}).get("paths", {}).get("templates", ".factory/templates")
    return os.path.join(repo_root(), base)


def rel(path):
    """Repo-relative path for messages."""
    return os.path.relpath(path, repo_root())


def die(msg, code=1):
    sys.stderr.write("error: %s\n" % msg)
    sys.exit(code)


def utcnow_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Forgiving YAML-subset parser
# ---------------------------------------------------------------------------
# Supports: nested mappings, block lists (scalars and mappings), inline lists
# [a, b], empty flow {} / [], single/double-quoted strings, null/~, ints,
# booleans, full-line and trailing comments. This intentionally covers only
# the shapes used by .factory/config.yaml, state.yaml, and doc front matter.

def _strip_comment(line):
    in_s = in_d = False
    i = 0
    while i < len(line):
        ch = line[i]
        if in_d and ch == "\\":
            i += 2  # skip backslash-escaped char inside a double-quoted span
            continue
        if ch == "'" and not in_d:
            in_s = not in_s
        elif ch == '"' and not in_s:
            in_d = not in_d
        elif ch == "#" and not in_s and not in_d:
            if i == 0 or line[i - 1] in " \t":
                return line[:i].rstrip()
        i += 1
    return line.rstrip()


def _split_inline_list(s):
    items, buf, in_s, in_d = [], "", False, False
    for ch in s:
        if ch == "'" and not in_d:
            in_s = not in_s
        elif ch == '"' and not in_s:
            in_d = not in_d
        if ch == "," and not in_s and not in_d:
            items.append(buf)
            buf = ""
        else:
            buf += ch
    if buf.strip():
        items.append(buf)
    return items


def _scalar(s):
    s = s.strip()
    if s == "" or s in ("null", "~", "Null", "NULL"):
        return None
    if s == "{}":
        return {}
    if s == "[]":
        return []
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [_scalar(x) for x in _split_inline_list(inner)] if inner else []
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return re.sub(r"\\(.)", r"\1", s[1:-1])
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        return s[1:-1].replace("''", "'")
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return s


_MAP_LINE = re.compile(r'^("(?:[^"\\]|\\.)*"|\'[^\']*\'|[^:#]+?):(?:\s+(.*)|\s*)$')


def _is_map_line(text):
    m = _MAP_LINE.match(text)
    return bool(m)


def _parse_block(lines):
    """lines: list of (indent, text). Returns parsed value."""
    if not lines:
        return None
    indent = lines[0][0]
    if lines[0][1].startswith("- ") or lines[0][1] == "-":
        items = []
        i = 0
        while i < len(lines):
            ind, text = lines[i]
            if ind != indent or not (text.startswith("- ") or text == "-"):
                raise ValueError("malformed list near: %r" % text)
            rest = text[1:].strip()
            j = i + 1
            sub = []
            while j < len(lines) and lines[j][0] > indent:
                sub.append(lines[j])
                j += 1
            if rest and _is_map_line(rest):
                items.append(_parse_block([(indent + 2, rest)] + sub))
            elif rest:
                items.append(_scalar(rest))
            else:
                items.append(_parse_block(sub) if sub else None)
            i = j
        return items
    # mapping
    d = {}
    i = 0
    while i < len(lines):
        ind, text = lines[i]
        if ind != indent:
            raise ValueError("bad indentation near: %r" % text)
        m = _MAP_LINE.match(text)
        if not m:
            raise ValueError("expected 'key: value' near: %r" % text)
        key = _scalar(m.group(1))
        val = m.group(2)
        j = i + 1
        sub = []
        while j < len(lines) and lines[j][0] > indent:
            sub.append(lines[j])
            j += 1
        if val is not None and val.strip():
            d[key] = _scalar(val)
        elif sub:
            d[key] = _parse_block(sub)
        else:
            d[key] = None
        i = j
    return d


def parse_yaml(text):
    lines = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.strip() == "---":
            continue
        leading = raw[:len(raw) - len(raw.lstrip())]
        if "\t" in leading:
            raise ValueError(
                "line %d: tab character in indentation — YAML forbids tabs; "
                "re-indent with spaces" % lineno)
        content = _strip_comment(raw)
        if not content.strip():
            continue
        indent = len(content) - len(content.lstrip(" "))
        lines.append((indent, content.strip()))
    parsed = _parse_block(lines)
    return parsed if parsed is not None else {}


def parse_front_matter(text):
    """Return (front_matter_dict, body). Front matter is optional."""
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            try:
                return parse_yaml("\n".join(lines[1:i])), "\n".join(lines[i + 1:])
            except ValueError:
                return {}, text
    return {}, text


# ---------------------------------------------------------------------------
# state.yaml
# ---------------------------------------------------------------------------

STATUSES = ["ready", "context", "contract", "planned", "in_progress",
            "in_review", "approved", "merged", "released"]
ALL_STATUSES = STATUSES + ["blocked"]
DONE_STATUSES = ["in_review", "approved", "merged", "released"]

PHASES = ["start", "context", "contract", "plan", "implement", "review",
          "verify", "adversarial", "converge", "handoff"]

TIERS = ["low", "medium", "high"]
TIER_RANK = {"low": 0, "medium": 1, "high": 2}

GATE_VALUES = {
    "contract": ["pending", "done", "skipped"],
    "plan_challenge": ["pending", "approve", "approve_with_risks", "revise",
                       "human_decision_required", "skipped"],
    "slice_reviews": ["pending", "approved", "changes_requested"],
    "verification_audit": ["pending", "approved", "changes_requested", "skipped"],
    "adversarial_qa": ["pending", "approved", "changes_requested", "skipped"],
    "convergence": ["pending", "done", "skipped"],
    "final_review": ["pending", "approved", "changes_requested"],
    "human_approval": ["pending", "approved", "not_required"],
}

# Values that satisfy a gate for validate-work-order.
GATE_SATISFIED = {
    "contract": {"done"},
    "plan_challenge": {"approve", "approve_with_risks"},
    "slice_reviews": {"approved"},
    "verification_audit": {"approved"},
    "adversarial_qa": {"approved"},
    "convergence": {"done"},
    "final_review": {"approved"},
    "human_approval": {"approved"},
}

# config.yaml `gates:` names -> state.yaml gate fields. The three high-tier
# adversarial lenses record their merged outcome in the single `adversarial_qa`
# field (synthesize-review merges the lenses); at medium tier the lens briefs
# fold into the final review round, so no adversarial gate is required there
# (`adversarial_combined` remains mapped for compatibility). `validate` means
# "this script ran" and is always satisfied.
CONFIG_GATE_TO_FIELD = {
    "contract": "contract",
    "plan_challenge": "plan_challenge",
    "slice_reviews": "slice_reviews",
    "verification_audit": "verification_audit",
    "adversarial_combined": "adversarial_qa",
    "adversarial_behavior": "adversarial_qa",
    "adversarial_operations": "adversarial_qa",
    "adversarial_architecture": "adversarial_qa",
    "convergence": "convergence",
    "final_review": "final_review",
    "human_approval": "human_approval",
    "validate": None,
}

# Skill that runs each gate — validate-work-order names it in failure messages
# so the fix is "run the gate", never just "set the field".
GATE_SKILL = {
    "contract": "compile-contract",
    "plan_challenge": "challenge-plan",
    "slice_reviews": "review-slice",
    "verification_audit": "audit-verification",
    "adversarial_qa": "adversarial-qa",
    "convergence": "converge-work-order",
    "final_review": "a fresh independent review round (review-log.md template)",
}


def allowed_next_statuses(current, blocked_from=None):
    """Lifecycle: ready→context→contract→planned→in_progress→in_review→approved→
    merged→released; in_review→in_progress on changes_requested.

    blocked is reachable from any state EXCEPT merged/released (completed WOs
    are immutable records and may not be laundered back through blocked).
    Resuming from blocked returns ONLY to the recorded `blocked_from` status;
    with no valid blocked_from recorded, no resume is allowed (repair first).
    """
    if current == "blocked":
        return {blocked_from} if blocked_from in STATUSES else set()
    nxt = set()
    if current not in ("merged", "released"):
        nxt.add("blocked")
    idx = STATUSES.index(current)
    if idx + 1 < len(STATUSES):
        nxt.add(STATUSES[idx + 1])
    if current == "in_review":
        nxt.add("in_progress")
    return nxt


def state_path(wo_id, cfg=None):
    return os.path.join(wo_dir(wo_id, cfg), "state.yaml")


def load_state(wo_id, cfg=None):
    path = state_path(wo_id, cfg)
    if not os.path.isfile(path):
        die("%s not found — run tools/agent/init-work-order --wo %s first."
            % (rel(path), wo_id))
    with open(path, encoding="utf-8") as f:
        try:
            state = parse_yaml(f.read())
        except ValueError as e:
            die("%s is not parseable (%s) — repair it to match "
                ".factory/templates/state.yaml." % (rel(path), e))
    if not isinstance(state, dict):
        die("%s is not a mapping — repair it to match .factory/templates/state.yaml."
            % rel(path))
    state.setdefault("gates", {})
    if not isinstance(state.get("gates"), dict):
        state["gates"] = {}
    if not isinstance(state.get("skip_reasons"), dict):
        state["skip_reasons"] = {}
    if not isinstance(state.get("waiver_approvers"), dict):
        state["waiver_approvers"] = {}
    return state


def _q(s):
    return '"%s"' % str(s).replace("\\", "\\\\").replace('"', '\\"')


def _sv(v, quote=False):
    if v is None:
        return "null"
    if isinstance(v, int):
        return str(v)
    return _q(v) if quote else str(v)


# Top-level state.yaml keys dump_state serializes explicitly, in this order.
# Anything else is an additive/unknown key and is preserved verbatim at the end.
KNOWN_STATE_KEYS = ["work_order", "status", "risk_tier", "risk_tier_set_by",
                    "risk_tier_set_computed", "current_phase",
                    "current_slice", "plan_revision", "last_verified_commit",
                    "next_action", "blocked_on", "blocked_from", "approver",
                    "gates", "skip_reasons", "waiver_approvers"]


def _dump_extra(key, val, indent=0):
    """Serialize an unknown (additive) key so it round-trips through parse_yaml."""
    pad = " " * indent
    if isinstance(val, dict):
        if not val:
            return ["%s%s: {}" % (pad, key)]
        lines = ["%s%s:" % (pad, key)]
        for k in sorted(val, key=str):
            lines.extend(_dump_extra(k, val[k], indent + 2))
        return lines
    if isinstance(val, list):
        if not val:
            return ["%s%s: []" % (pad, key)]
        lines = ["%s%s:" % (pad, key)]
        for item in val:
            lines.append("%s- %s" % (" " * (indent + 2),
                                     _sv(item, quote=isinstance(item, str))))
        return lines
    return ["%s%s: %s" % (pad, key, _sv(val, quote=isinstance(val, str)))]


def dump_state(state):
    """Canonical state.yaml serialization (keeps the template's comments).

    Unknown top-level keys and unknown `gates:` entries are preserved and
    serialized after the known ones — never silently dropped (additive schema
    tolerance). write_state round-trip-checks the output before writing.
    """
    g = state.get("gates", {}) or {}
    sk = state.get("skip_reasons", {}) or {}
    lines = [
        "# Machine-readable execution state — the resume point. Updated by",
        "# tools/agent/update-state at every checkpoint; never reconstructed from memory.",
        "# An agent resuming this WO reads this file first, then checklist.md, then the plan.",
        "",
        "work_order: %s" % _sv(state.get("work_order")),
        "status: %s            # ready|context|contract|planned|in_progress|in_review|approved|merged|released|blocked"
        % _sv(state.get("status")),
        "risk_tier: %s        # low|medium|high — set by tools/agent/risk-tier; humans may raise, agents may not lower"
        % _sv(state.get("risk_tier")),
        "risk_tier_set_by: %s  # human who set the tier via risk-tier --set (the only lowering path); null otherwise"
        % _sv(state.get("risk_tier_set_by"),
              quote=state.get("risk_tier_set_by") is not None),
        "risk_tier_set_computed: %s  # tier computed from paths when --set ran; --verify re-fails if risk grows past it"
        % _sv(state.get("risk_tier_set_computed")),
        "current_phase: %s     # start|context|contract|plan|implement|review|verify|adversarial|converge|handoff"
        % _sv(state.get("current_phase")),
        "current_slice: %s      # e.g. S02" % _sv(state.get("current_slice")),
        "plan_revision: %s" % _sv(state.get("plan_revision", 0)),
        "last_verified_commit: %s"
        % _sv(state.get("last_verified_commit"),
              quote=state.get("last_verified_commit") is not None),
        "next_action: %s" % _sv(state.get("next_action"), quote=True),
        "blocked_on: %s         # human-readable blocker; set whenever status=blocked"
        % _sv(state.get("blocked_on"), quote=state.get("blocked_on") is not None),
        "blocked_from: %s       # status held when entering blocked; resume returns ONLY here"
        % _sv(state.get("blocked_from")),
        "approver: %s           # human who recorded human_approval=approved (update-state --approver)"
        % _sv(state.get("approver"), quote=state.get("approver") is not None),
        "",
        "gates:",
        "  contract: %s              # pending|done|skipped" % _sv(g.get("contract", "pending")),
        "  plan_challenge: %s        # pending|approve|approve_with_risks|revise|human_decision_required|skipped"
        % _sv(g.get("plan_challenge", "pending")),
        "  slice_reviews: %s         # pending|approved|changes_requested (latest slice)"
        % _sv(g.get("slice_reviews", "pending")),
        "  verification_audit: %s    # pending|approved|changes_requested|skipped"
        % _sv(g.get("verification_audit", "pending")),
        "  adversarial_qa: %s        # pending|approved|changes_requested|skipped"
        % _sv(g.get("adversarial_qa", "pending")),
        "  convergence: %s           # pending|done|skipped" % _sv(g.get("convergence", "pending")),
        "  final_review: %s          # pending|approved|changes_requested"
        % _sv(g.get("final_review", "pending")),
        "  human_approval: %s        # pending|approved|not_required"
        % _sv(g.get("human_approval", "pending")),
    ]
    for k in sorted(g, key=str):
        if k not in GATE_VALUES:
            lines.append("  %s: %s  # unknown gate — preserved verbatim"
                         % (k, _sv(g[k], quote=isinstance(g[k], str))))
    lines += [
        "",
        "# Every `skipped` requires a skip_reasons entry.",
    ]
    if sk:
        lines.append("skip_reasons:")
        for k in sorted(sk):
            lines.append("  %s: %s" % (k, _sv(sk[k], quote=True)))
    else:
        lines.append("skip_reasons: {}")
    wa = state.get("waiver_approvers") or {}
    lines += [
        "",
        "# Every `skipped` gate also records the HUMAN who waived it",
        "# (update-state --approver; protocol: docs/runbooks/break-glass.md).",
    ]
    if isinstance(wa, dict) and wa:
        lines.append("waiver_approvers:")
        for k in sorted(wa):
            lines.append("  %s: %s" % (k, _sv(wa[k], quote=True)))
    else:
        lines.append("waiver_approvers: {}")
    extras = [k for k in state if k not in KNOWN_STATE_KEYS]
    if extras:
        lines.append("")
        lines.append("# Unknown keys — preserved verbatim (additive schema tolerance).")
        for k in sorted(extras, key=str):
            lines.extend(_dump_extra(k, state[k]))
    return "\n".join(lines) + "\n"


def _roundtrip_check(state, text):
    """Parse dump_state output back and verify every writable field survived.

    Called by write_state BEFORE anything touches disk: a serializer/parser
    disagreement (embedded newlines, escape handling, dropped keys) dies loudly
    instead of corrupting or silently truncating state.yaml.
    """
    def bad(detail):
        die("internal: state.yaml serialization fails round-trip (%s) — refusing "
            "to write. This is a tools/agent defect; fix the offending value or "
            "report the bug." % detail)

    try:
        parsed = parse_yaml(text)
    except ValueError as e:
        bad("output does not parse back: %s" % e)
    if not isinstance(parsed, dict):
        bad("output parses back as %s, not a mapping" % type(parsed).__name__)

    def check(label, want, got):
        if want != got:
            bad("field %s wrote %r but parses back as %r" % (label, want, got))

    for key, want in state.items():
        if key in ("gates", "skip_reasons"):
            sub = parsed.get(key)
            want_map = want or {}
            if not isinstance(want_map, dict):
                continue
            for k, v in want_map.items():
                check("%s.%s" % (key, k), v,
                      sub.get(k) if isinstance(sub, dict) else None)
        else:
            check(key, want, parsed.get(key))


def write_state(wo_id, state, cfg=None):
    """Atomically write state.yaml (temp file + os.replace) after verifying the
    serialization round-trips — a crash mid-write can never leave a truncated
    resume point, and a bad value can never corrupt the file."""
    path = state_path(wo_id, cfg)
    text = dump_state(state)
    _roundtrip_check(state, text)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def require_intact_state(state, wo_id):
    """Refuse to operate on a corrupted state.yaml: rewriting it would launder
    the corruption into a healthy-looking file and erase the forensic signal."""
    if state.get("work_order") != wo_id or state.get("status") not in ALL_STATUSES:
        die(".factory/work-orders/%s/state.yaml is missing or has an invalid "
            "work_order/status — it is likely corrupted. Repair it to match "
            ".factory/templates/state.yaml (reconstruct the last checkpoint from "
            "events.jsonl) before recording new checkpoints." % wo_id)


def default_actor():
    """Default actor identity recorded on every event: $USER + '/agent'."""
    return "%s/agent" % os.environ.get("USER", "unknown")


def append_event(wo_id, payload, cfg=None, actor=None):
    """Append one JSON event line to events.jsonl.

    Event taxonomy (authoritative). Tools are the ONLY writers of events.jsonl —
    a hand-written event line is a defect, and validate-work-order's events
    check enforces the schema: valid JSON per line, required keys ts/wo/event,
    wo matching the directory, and non-decreasing timestamps.

      wo.initialized    emitted by init-work-order when the execution dir is created
      state.updated     emitted by update-state at every checkpoint
                        (payload: changes: {field: {from, to}})
      risk_tier.raised  emitted by risk-tier --write when it raises state.yaml's
                        risk_tier, or by risk-tier --set when a human raises/
                        re-affirms it (payload: from, to [, approver])
      risk_tier.lowered emitted by risk-tier --set when a HUMAN lowers the tier
                        (payload: from, to, approver — approver is mandatory;
                        agents may never lower a tier)

    Every line also records `actor` (default: $USER + '/agent'; update-state
    accepts --actor to override).
    """
    path = os.path.join(wo_dir(wo_id, cfg), "events.jsonl")
    event = {"ts": utcnow_iso(), "wo": wo_id, "actor": actor or default_actor()}
    event.update(payload)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def strip_html_comments(text):
    """Remove HTML comments, preserving line count so line numbers stay valid."""
    def blank(m):
        return "\n" * m.group(0).count("\n")
    return _HTML_COMMENT.sub(blank, text)


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Path glob matching (supports **)
# ---------------------------------------------------------------------------

def glob_to_regex(pat):
    i, out = 0, ""
    while i < len(pat):
        c = pat[i]
        if c == "*":
            if pat[i:i + 3] == "**/":
                out += "(?:.*/)?"
                i += 3
            elif pat[i:i + 2] == "**":
                out += ".*"
                i += 2
            else:
                out += "[^/]*"
                i += 1
        elif c == "?":
            out += "[^/]"
            i += 1
        else:
            out += re.escape(c)
            i += 1
    return re.compile("^" + out + "$")


def path_matches(path, pattern):
    return bool(glob_to_regex(pattern).match(path))


# ---------------------------------------------------------------------------
# IDs
# ---------------------------------------------------------------------------

def id_regexes(cfg):
    ids = cfg.get("ids", {})
    out = {}
    for key, pat in ids.items():
        if isinstance(pat, str):  # non-string entries (e.g. scratch_min) are not grammars
            out[key] = re.compile(pat)
    return out


def scratch_min(cfg):
    """ids.scratch_min from config: WO numbers >= this are scratch/testing WOs."""
    v = (cfg or {}).get("ids", {}).get("scratch_min")
    return v if isinstance(v, int) else None


def is_scratch_wo(wo_id, cfg):
    """True when wo_id falls in the reserved scratch/testing range (ids.scratch_min).
    Scratch WOs are excluded from indexes, traceability, and validate --all;
    init-work-order/update-state still operate on them."""
    smin = scratch_min(cfg)
    if smin is None:
        return False
    m = re.search(r"([0-9]+)$", wo_id or "")
    return bool(m) and int(m.group(1)) >= smin


def check_wo_id(wo_id, cfg):
    pat = cfg.get("ids", {}).get("work_order", r"WO-[0-9]{4}")
    if not re.fullmatch(pat, wo_id or ""):
        die("'%s' is not a valid work order ID (must match %s) — pass e.g. "
            "--wo WO-1042." % (wo_id, pat))


def list_wo_dirs(cfg=None, include_scratch=False):
    """All WO execution dirs. Scratch WOs (ids.scratch_min and above) are
    excluded by default — pass include_scratch=True to see them."""
    cfg = cfg or load_config()
    base = os.path.join(repo_root(),
                        cfg.get("paths", {}).get("work_orders", ".factory/work-orders"))
    if not os.path.isdir(base):
        return []
    pat = cfg.get("ids", {}).get("work_order", r"WO-[0-9]{4}")
    out = []
    for name in sorted(os.listdir(base)):
        full = os.path.join(base, name)
        if os.path.isdir(full) and re.fullmatch(pat, name):
            if not include_scratch and is_scratch_wo(name, cfg):
                continue
            out.append((name, full))
    return out
