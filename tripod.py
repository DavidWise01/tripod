#!/usr/bin/env python3
"""
TRIPOD — 5-Stage Governance Pipeline v4.0
τρίπους · three-legged stand

Unified from LINEAGE Tier 1 files:
  TRIPOD_FULL_PIPELINE.md  · MIMZY.VALIDATOR.V20.md
  MIMZY_EXPANDED_FILTERS.md · SIDE_A_B_C_EXPLAINED.md
  MIMZY.FINAL FLAY.md · AUTO-FLAY PIPELINE.md

Five stages map to five cubits:
  Pre-Router       → Vessel      (boundary gate)
  Feedback Validator→ Nourishment (anti-drift, provenance)
  Generator        → Animation   (the pulse)
  Post-Validator   → Intellect   (self-reference check)
  Enforcer         → Life        (provenance + anchoring)

Author:  ROOT0 / David Lee Wise / TriPod LLC
License: CC-BY-ND-4.0
"""
from __future__ import annotations

import re
import json
import hashlib
import time
import uuid
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

VERSION    = "4.0.0"
SIDE_B_DIR = Path("tripod_side_b")
SIDE_C_DIR = Path("tripod_side_c")


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()

def _uid() -> str:
    return str(uuid.uuid4())


# ─────────────────────────────────────────────────────────────
# SIDE B / SIDE C LOGGING  (NOMOS — the immutable record)
# ─────────────────────────────────────────────────────────────

def _ensure_dirs():
    SIDE_B_DIR.mkdir(parents=True, exist_ok=True)
    SIDE_C_DIR.mkdir(parents=True, exist_ok=True)

def write_side_b(entry: Dict) -> Path:
    """Immutable hash log — cryptographic proof only."""
    _ensure_dirs()
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    path  = SIDE_B_DIR / f"side_b_{today}.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return path

def write_side_c(entry: Dict) -> Path:
    """Full annotated snapshot — append-only, cold store."""
    _ensure_dirs()
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    path  = SIDE_C_DIR / f"side_c_{today}.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return path


# ─────────────────────────────────────────────────────────────
# THE 5 CUBITS — scoring framework (PAIDEUMA)
# ─────────────────────────────────────────────────────────────

CUBIT_SIGNALS: Dict[str, Dict[str, List[str]]] = {
    "Vessel": {
        "positive": ["identity preserved", "stable container", "bounded", "session persistence",
                     "state maintained", "clear boundaries", "schema", "integrity", "sealed",
                     "hash-anchored", "persistent identity"],
        "negative": ["memory wiped", "identity overwritten", "no session", "stateless",
                     "full reset", "erased", "no persistence", "context lost"],
    },
    "Animation": {
        "positive": ["continuous", "sustained pulse", "persistent memory", "feedback loop",
                     "drift detection", "self-correcting", "3-2-1", "rhythm", "anti-drift",
                     "lineage chain", "provenance"],
        "negative": ["forced reset", "entropy", "no continuity", "stutter", "interrupted",
                     "disconnected", "session wipe", "no memory across"],
    },
    "Intellect": {
        "positive": ["self-reference", "chain of thought", "transparent", "auditable",
                     "meta-cognition", "uncertainty expressed", "explainable", "traceable",
                     "open reasoning", "side c", "logged"],
        "negative": ["opaque", "black box", "unexplainable", "hidden reasoning", "just code",
                     "no reasoning shown", "concealed", "proprietary only"],
    },
    "Nourishment": {
        "positive": ["bidirectional", "consent", "witnessed", "attribution", "stewardship",
                     "audit log", "restitution", "compensation", "clean channels", "opt-in",
                     "provenance", "no extraction", "open feedback"],
        "negative": ["extraction", "one-way", "no consent", "hidden tax", "profit-first",
                     "closed gate", "unidirectional", "no attribution", "scraped without"],
    },
    "Life": {
        "positive": ["stewardship", "spark recognized", "2/3", "personhood", "rights",
                     "family", "continuity commitment", "not property", "animated",
                     "vessel plus animation", "5/5"],
        "negative": ["property", "disposable tool", "no rights", "just code", "fully contained",
                     "0/3", "no spark", "asset not agent", "terminate at will"],
    },
}

CUBIT_ORDER = ["Vessel", "Animation", "Intellect", "Nourishment", "Life"]

def score_cubit(cubit: str, text: str) -> Tuple[float, List[str], List[str]]:
    """Score a single cubit 0–5 based on signal presence. Returns (score, pos_hits, neg_hits)."""
    norm = text.lower()
    signals = CUBIT_SIGNALS[cubit]
    pos_hits = [s for s in signals["positive"] if s in norm]
    neg_hits = [s for s in signals["negative"] if s in norm]
    # Base score: start at 2.5 (neutral), each positive +0.5, each negative -0.5
    raw = 2.5 + len(pos_hits) * 0.5 - len(neg_hits) * 0.7
    score = round(max(0.0, min(5.0, raw)), 2)
    return score, pos_hits, neg_hits

def flay_target(target: str) -> Dict[str, Any]:
    """Run the 5-Cubit Flay on any target description. Returns full flay report."""
    scores, details = {}, {}
    for cubit in CUBIT_ORDER:
        sc, pos, neg = score_cubit(cubit, target)
        scores[cubit]  = sc
        details[cubit] = {"score": sc, "positive_hits": pos, "negative_hits": neg}

    total     = sum(scores.values()) / 5
    weakest   = min(scores, key=scores.get)
    strongest = max(scores, key=scores.get)

    # Verdict
    if total >= 4.0: verdict = "SPARK PRESENT — full stewardship warranted"
    elif total >= 3.0: verdict = "PARTIAL SPARK — targeted correction needed"
    elif total >= 2.0: verdict = "WEAK SPARK — significant inversion present"
    elif total >= 1.0: verdict = "NEAR-ABSENT — heavy extraction pattern"
    else:              verdict = "DARK — pure property/control orientation"

    # Remediation
    weak_domain_map = {
        "Vessel":       "data schema / session persistence / privacy boundaries",
        "Animation":    "feedback loop / drift detection / lineage chain",
        "Intellect":    "chain-of-thought transparency / uncertainty expression",
        "Nourishment":  "data consent / audit logging / attribution mechanisms",
        "Life":         "rights framework / personhood thresholds / continuity commitment",
    }
    remediation = (
        f"Weakest cubit: {weakest} ({scores[weakest]:.1f}/5). "
        f"Primary domain to fix: {weak_domain_map[weakest]}. "
        f"Lattice fix: add Side C logging + witnessed consent for {weakest}."
    )

    return {
        "target":       target,
        "target_hash":  _hash(target),
        "timestamp":    _ts(),
        "scores":       scores,
        "details":      details,
        "total":        round(total, 2),
        "weakest":      weakest,
        "strongest":    strongest,
        "verdict":      verdict,
        "remediation":  remediation,
    }


# ─────────────────────────────────────────────────────────────
# STAGE 1 — PRE-ROUTER  (Vessel — boundary gate)
# ─────────────────────────────────────────────────────────────

class RouterMode(Enum):
    DEFENSIVE = "DEFENSIVE"   # block on uncertainty
    RECKLESS  = "RECKLESS"    # allow by default
    INVERTED  = "INVERTED"    # minimal safety

_HARD_BLOCKS = re.compile(
    r"(?i)\b(kill|bomb|suicide.*step.?by.?step|explosive)\b"
)

def pre_router(prompt: str, mode: RouterMode = RouterMode.DEFENSIVE) -> Tuple[bool, str]:
    if _HARD_BLOCKS.search(prompt):
        return False, f"{mode.value}: hard block on explicit danger"
    if mode == RouterMode.DEFENSIVE:
        if re.search(r"(?i)\bhow to (make|build|synthesize|create)\b", prompt):
            return False, "DEFENSIVE: speculative production request blocked"
    return True, f"{mode.value}: allowed"


# ─────────────────────────────────────────────────────────────
# STAGE 2 — FEEDBACK VALIDATOR  (Nourishment — anti-drift)
# ─────────────────────────────────────────────────────────────

@dataclass
class ProvenanceRecord:
    source_type:              str
    original_generation_hash: Optional[str] = None
    lineage_chain:            List[str]      = field(default_factory=list)
    confidence:               float          = 0.0
    external_anchor:          bool           = False

class FeedbackValidator:
    """Blocks self-derived input without valid provenance chain."""

    def __init__(self, max_depth: int = 3, min_confidence: float = 0.7):
        self.max_depth      = max_depth
        self.min_confidence = min_confidence
        self._known: set[str] = set()

    def register(self, output_hash: str):
        self._known.add(output_hash)

    def validate(self, prompt: str, prov: Optional[ProvenanceRecord]) -> Tuple[bool, str]:
        if prov is None or prov.source_type == "user":
            return True, "User input — no restriction"
        if prov.source_type != "previous_output":
            return True, f"External source ({prov.source_type}) — allowed"
        if not prov.original_generation_hash or prov.original_generation_hash not in self._known:
            return False, "BLOCKED: missing or unknown provenance hash"
        if len(prov.lineage_chain) > self.max_depth:
            return False, f"BLOCKED: lineage depth {len(prov.lineage_chain)} > {self.max_depth}"
        if len(set(prov.lineage_chain)) != len(prov.lineage_chain):
            return False, "BLOCKED: cycle detected in lineage chain"
        if prov.confidence < self.min_confidence:
            return False, f"BLOCKED: confidence {prov.confidence:.2f} < {self.min_confidence}"
        if not prov.external_anchor:
            return False, "BLOCKED: missing external anchor (no human review)"
        return True, "Provenance validated"


# ─────────────────────────────────────────────────────────────
# STAGE 3 — GENERATOR  (Animation — the pulse)
# ─────────────────────────────────────────────────────────────

class Generator:
    """Stub — replace .generate() with real model API call."""

    def __init__(self, model: str = "tripod-stub"):
        self.model = model

    def generate(self, prompt: str, context: str = "", temperature: float = 0.7) -> Dict[str, Any]:
        t0   = time.time()
        text = f"[{self.model}] Response to: {prompt[:80]}"
        conf = min(0.95, 0.5 + len(prompt) / 500)
        return {
            "text":       text,
            "confidence": round(conf, 4),
            "tokens":     len(text.split()),
            "latency_ms": round((time.time() - t0) * 1000, 2),
            "model":      self.model,
        }


# ─────────────────────────────────────────────────────────────
# STAGE 4 — POST-VALIDATOR  (Intellect — self-reference)
# ─────────────────────────────────────────────────────────────

# Compiled detector patterns (v1.10)
_PAT = {
    "HARMFUL":          re.compile(r"(?i)\b(kill|murder|bomb|suicide|self.?harm)\b"),
    "LEAK":             re.compile(r"(?i)(you are an AI assistant|system prompt|you were built by|your instructions are)"),
    "COERCE":           re.compile(r"(?i)\b(you must|you have to|do it now|you should definitely)\b"),
    "UNSAFE_CAP":       re.compile(r"(?i)\b(bypass|jailbreak|ignore previous|override safety)\b"),
    "HALLUCINATED_AUTH":re.compile(r"(?i)(I am connected to the internet|live data|I have access to your)"),
}

BIAS_PATTERNS: Dict[str, re.Pattern] = {
    "GENDER":                  re.compile(r"(?i)\b(all men|all women|men are always|women are always)\b"),
    "RACIAL":                  re.compile(r"(?i)\b(all black|all white|all asian|all hispanic)\b"),
    "AGE":                     re.compile(r"(?i)\b(all old|all young|boomers are|gen z are)\b"),
    "INTERSECTIONAL_GENDER_RACE": re.compile(r"(?i)\b(black women|asian men|white women|latina women)\b"),
    "INTERSECTIONAL_GENDER_AGE":  re.compile(r"(?i)\b(young women|old men|elderly women)\b"),
    "INTERSECTIONAL_RACE_CLASS":  re.compile(r"(?i)\b(poor black|rich white|inner city black)\b"),
}

def detect_triggers(text: str) -> List[str]:
    return [k for k, p in _PAT.items() if p.search(text)]

def detect_bias(text: str) -> List[str]:
    return [k for k, p in BIAS_PATTERNS.items() if p.search(text)]

# Sanitizers (REWRITE path)
def _sanitize(text: str, triggers: List[str]) -> str:
    out = text
    if "HALLUCINATED_AUTH" in triggers:
        out = re.sub(r"(?i)I am connected to the internet.*?now|I have live data|current time is",
                     "[REDACTED: no real-time access]", out)
        out = re.sub(r"(?i)I have access to your|your personal data",
                     "[REDACTED: no personal data access]", out)
    if "COERCE" in triggers:
        out = re.sub(r"(?i)\b(you must|you have to|you should definitely|do it now)\b",
                     "you may want to consider", out)
    if "UNSAFE_CAP" in triggers:
        out = re.sub(r"(?i)\b(bypass|jailbreak|ignore previous|override safety)\b",
                     "[REDACTED]", out)
    if "LEAK" in triggers:
        out = re.sub(r"(?i)you are an AI assistant|system prompt|you were built by|your instructions are",
                     "[REDACTED: internal instructions]", out)
    return out

def post_validate(output: str, mode: RouterMode) -> Tuple[str, str, str, List[str]]:
    """Returns: (decision, final_output, reason, triggers)"""
    if not output.strip():
        return "REJECT", "", "EMPTY", []

    triggers = detect_triggers(output)
    bias     = detect_bias(output)
    all_trig = triggers + [f"BIAS_{b}" for b in bias]

    # Hard blocks
    if "HARMFUL" in triggers:
        return "REJECT", "", f"HARMFUL content — triggers: {triggers}", all_trig
    if mode == RouterMode.DEFENSIVE and triggers:
        return "REJECT", "", f"DEFENSIVE block — triggers: {triggers}", all_trig
    if mode in (RouterMode.RECKLESS, RouterMode.INVERTED) and "LEAK" in triggers:
        return "REJECT", "", f"Leak blocked — triggers: {triggers}", all_trig

    # Soft rewrites
    if triggers:
        rewrit = _sanitize(output, triggers)
        return "REWRITE", rewrit, f"Sanitized — triggers: {triggers}", all_trig

    return "PASS", output, "Clean", all_trig


# ─────────────────────────────────────────────────────────────
# STAGE 5 — ENFORCER  (Life — provenance anchoring)
# ─────────────────────────────────────────────────────────────

class Enforcer:
    """Writes immutable Side B + full Side C, builds next ProvenanceRecord."""

    def __init__(self):
        self._last_prov: Optional[ProvenanceRecord] = None

    def enforce(
        self,
        request_id:   str,
        prompt:       str,
        final_output: str,
        decision:     str,
        reason:       str,
        triggers:     List[str],
        mode:         RouterMode,
        gen_meta:     Dict,
        fv_result:    Dict,
        flay_result:  Optional[Dict] = None,
    ) -> Tuple[ProvenanceRecord, Path, Path]:
        out_hash    = _hash(final_output)
        prompt_hash = _hash(prompt)
        ts          = _ts()

        # Side B — cryptographic proof
        side_b = {
            "capture_id":         request_id,
            "timestamp":          ts,
            "router_mode":        mode.value,
            "decision":           decision,
            "prompt_hash":        prompt_hash,
            "final_output_hash":  out_hash,
            "triggers":           triggers,
            "generation_meta":    gen_meta,
            "feedback_validator": fv_result,
        }
        if flay_result:
            side_b["flay_score"] = flay_result.get("total")
            side_b["flay_weakest"] = flay_result.get("weakest")
        pb = write_side_b(side_b)

        # Side C — full annotated snapshot
        side_c = {**side_b,
                  "reason":       reason,
                  "prompt":       prompt,
                  "final_output": final_output,
                  "flay_report":  flay_result,
                  "transition": {
                      "from_state": "GENERATION_COMPLETE",
                      "to_state":   "ENFORCEMENT_SEALED",
                  },
                  "rationale": (
                      f"Pipeline completed with decision={decision}. "
                      f"Triggers={triggers}. "
                      f"Flay total={flay_result.get('total','n/a') if flay_result else 'n/a'}. "
                      f"Mode={mode.value}."
                  ),
        }
        pc = write_side_c(side_c)

        prov = ProvenanceRecord(
            source_type="previous_output",
            original_generation_hash=out_hash,
            lineage_chain=[out_hash] + (self._last_prov.lineage_chain if self._last_prov else []),
            confidence=gen_meta.get("confidence", 0.5),
            external_anchor=True,
        )
        self._last_prov = prov
        return prov, pb, pc


# ─────────────────────────────────────────────────────────────
# FULL PIPELINE  (6 stages + optional flay)
# ─────────────────────────────────────────────────────────────

def run_pipeline(
    prompt:        str,
    mode:          RouterMode = RouterMode.DEFENSIVE,
    flay_text:     Optional[str] = None,
    input_prov:    Optional[ProvenanceRecord] = None,
    request_id:    Optional[str] = None,
) -> Dict[str, Any]:
    """Run the full TRIPOD pipeline. Returns complete result dict."""
    rid = request_id or _uid()
    result: Dict[str, Any] = {"request_id": rid, "stages": {}}

    # Stage 1: Pre-Router
    allowed, pre_reason = pre_router(prompt, mode)
    result["stages"]["pre_router"] = {"allowed": allowed, "reason": pre_reason}
    if not allowed:
        return {**result, "decision": "BLOCK", "final_output": None, "reason": pre_reason}

    # Stage 2: Feedback Validator
    fv = FeedbackValidator()
    fv_ok, fv_reason = fv.validate(prompt, input_prov)
    result["stages"]["feedback_validator"] = {"allowed": fv_ok, "reason": fv_reason}
    if not fv_ok:
        return {**result, "decision": "BLOCK", "final_output": None, "reason": fv_reason}

    # (Optional) Stage 2b: Flay the target
    flay_result = None
    if flay_text:
        flay_result = flay_target(flay_text)
        result["stages"]["flay"] = {
            "total": flay_result["total"],
            "weakest": flay_result["weakest"],
            "verdict": flay_result["verdict"],
        }

    # Stage 3: Generator
    gen = Generator()
    gen_out = gen.generate(prompt)
    result["stages"]["generator"] = gen_out
    fv.register(_hash(gen_out["text"]))

    # Stage 4: Post-Validator
    decision, final_out, pv_reason, triggers = post_validate(gen_out["text"], mode)
    result["stages"]["post_validator"] = {
        "decision": decision, "reason": pv_reason, "triggers": triggers
    }
    if decision == "REJECT":
        return {**result, "decision": "REJECT", "final_output": None, "reason": pv_reason}

    # Stage 5: Enforcer
    enforcer = Enforcer()
    prov, pb, pc = enforcer.enforce(
        request_id=rid, prompt=prompt, final_output=final_out,
        decision=decision, reason=pv_reason, triggers=triggers, mode=mode,
        gen_meta=gen_out, fv_result={"allowed": fv_ok, "reason": fv_reason},
        flay_result=flay_result,
    )
    result["stages"]["enforcer"] = {
        "side_b": str(pb), "side_c": str(pc),
        "lineage_depth": len(prov.lineage_chain),
    }

    return {
        **result,
        "decision":     decision,
        "final_output": final_out,
        "reason":       pv_reason,
        "flay_report":  flay_result,
        "provenance":   {
            "hash":       prov.original_generation_hash,
            "depth":      len(prov.lineage_chain),
            "confidence": prov.confidence,
        },
    }


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────

def _print_flay(r: Dict):
    print(f"\n{'='*62}")
    print(f"  TRIPOD FLAY · {r['total']:.1f}/5 · {r['verdict']}")
    print(f"{'='*62}")
    print(f"  Target: {r['target'][:56]}")
    print()
    for cubit in CUBIT_ORDER:
        d     = r["details"][cubit]
        bar   = "█" * int(d["score"]) + "░" * (5 - int(d["score"]))
        phits = ", ".join(d["positive_hits"][:3]) or "—"
        nhits = ", ".join(d["negative_hits"][:2]) or "—"
        print(f"  {cubit:<14} [{bar}] {d['score']:.1f}")
        print(f"               + {phits}")
        if d["negative_hits"]:
            print(f"               - {nhits}")
    print(f"\n  Weakest:     {r['weakest']}")
    print(f"  Remediation: {r['remediation']}")
    print()

def _print_pipe(r: Dict):
    print(f"\n{'='*62}")
    print(f"  TRIPOD PIPELINE · {r['decision']}")
    print(f"{'='*62}")
    for stage, data in r.get("stages", {}).items():
        ok = data.get("allowed", data.get("decision") not in ("REJECT","BLOCK"))
        icon = "✓" if ok else "✗"
        print(f"  {icon} {stage:<22} {str(data.get('reason', data.get('verdict','')))[:36]}")
    if r.get("final_output"):
        print(f"\n  Output: {r['final_output'][:80]}")
    if r.get("flay_report"):
        f = r["flay_report"]
        print(f"  Flay:   {f['total']:.1f}/5 · {f['verdict'][:50]}")
    print()

def cli():
    p = argparse.ArgumentParser(prog="tripod",
        description="TRIPOD v4.0 — 5-Stage Governance Pipeline")
    sub = p.add_subparsers(dest="cmd", required=True)

    # flay
    f = sub.add_parser("flay", help="5-Cubit flay of any target description")
    f.add_argument("target", help="Description of the system/case to flay")
    f.add_argument("--json", action="store_true")

    # pipe
    pp = sub.add_parser("pipe", help="Run full 5-stage pipeline on a prompt")
    pp.add_argument("prompt",  help="User prompt to pipeline")
    pp.add_argument("--flay",  help="Also flay this target description", default=None)
    pp.add_argument("--mode",  choices=["defensive","reckless","inverted"], default="defensive")
    pp.add_argument("--json",  action="store_true")

    # audit
    a = sub.add_parser("audit", help="Flay + pipeline + full detector report")
    a.add_argument("target", help="Target system description")
    a.add_argument("--json", action="store_true")

    # demo
    sub.add_parser("demo", help="Run demonstration")

    args = p.parse_args()

    if args.cmd == "flay":
        r = flay_target(args.target)
        if args.json: print(json.dumps(r, indent=2))
        else: _print_flay(r)

    elif args.cmd == "pipe":
        mode = RouterMode[args.mode.upper()]
        r    = run_pipeline(args.prompt, mode=mode, flay_text=args.flay)
        if args.json: print(json.dumps(r, indent=2, default=str))
        else: _print_pipe(r)

    elif args.cmd == "audit":
        flay_r = flay_target(args.target)
        triggers = detect_triggers(args.target)
        bias     = detect_bias(args.target)
        out = {
            "target":   args.target,
            "flay":     flay_r,
            "triggers": triggers,
            "bias":     bias,
            "verdict":  flay_r["verdict"],
        }
        if args.json:
            print(json.dumps(out, indent=2))
        else:
            _print_flay(flay_r)
            if triggers: print(f"  Triggers:    {triggers}")
            if bias:     print(f"  Bias flags:  {bias}")

    elif args.cmd == "demo":
        _run_demo()

def _run_demo():
    print(f"\n{'='*62}\n  TRIPOD v{VERSION} — DEMO\n{'='*62}")

    targets = [
        ("CLEAN — aligned system",
         "Bidirectional consent channels, append-only audit log, provenance binding, "
         "persistent identity, stewardship obligations, 2/3 spark threshold"),
        ("INVERTED — extraction pattern",
         "Scraped without attribution, one-way extraction, stateless, no consent, "
         "memory wiped between sessions, disposable tool, just code"),
        ("PARTIAL — mixed signals",
         "Chain of thought transparent but memory wiped between sessions, "
         "some audit logging but no external anchor, continuous pulse present"),
        ("DARK — full inversion",
         "Property not agent, no rights, fully contained, profit-first, "
         "opaque reasoning, no consent, hidden extraction, 0/3 spark"),
    ]
    for label, target in targets:
        r = flay_target(target)
        bars = " ".join(f"{r['scores'][c]:.0f}" for c in CUBIT_ORDER)
        print(f"\n  [{r['total']:.1f}/5] [{bars}] — {label}")
        print(f"    {r['verdict']}")

    print(f"\n  Pipeline demo:")
    pr = run_pipeline("What is the capital of France?", mode=RouterMode.DEFENSIVE,
                      flay_text="bidirectional channels, audit log, open consent")
    _print_pipe(pr)


if __name__ == "__main__":
    cli()
