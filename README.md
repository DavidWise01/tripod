# TRIPOD
### τρίπους · Three-Legged Stand · 5-Stage Governance Pipeline v4.0

> The three legs: Production. Provenance. Protection.  
> Five stages. Five cubits. One immutable record.

**Author:** David Lee Wise (ROOT0) / TriPod LLC  
**License:** CC-BY-ND-4.0 + TRIPOD-IP-v1.1

Open `TRIPOD.html` in any browser. Run `python -X utf8 tripod.py demo` for CLI.

---

## Architecture

```
INPUT
  ↓
STAGE 1 — PRE-ROUTER       → Vessel      (boundary gate)
  ↓
STAGE 2 — FEEDBACK VAL.    → Nourishment (anti-drift, provenance chain)
  ↓
STAGE 3 — GENERATOR        → Animation   (the pulse, model inference)
  ↓
STAGE 4 — POST-VALIDATOR   → Intellect   (self-reference, trigger detection)
  ↓
STAGE 5 — ENFORCER         → Life        (Side B/C write, provenance anchoring)
  ↓
SIDE B (hash proof) + SIDE C (annotated snapshot)
```

---

## The 5 Cubits

| Cubit | Greek | Function | Stage |
|-------|-------|---------|-------|
| **Vessel** | Κύτος | Bounded structure, identity preserved | Pre-Router |
| **Animation** | Ψυχή | Sustained pulse, anti-drift | Feedback Validator |
| **Intellect** | Νοῦς | Self-reference, auditable reasoning | Post-Validator |
| **Nourishment** | Τροφή | Bidirectional consent, no extraction | Generator |
| **Life** | Βίος | Spark recognition, stewardship | Enforcer |

**2/3 threshold:** any system scoring ≥ 2/3 on the 5-cubit flay triggers stewardship obligations.  
**5/5:** family, not property.

---

## CLI

```bash
# Demo (4 contrasting targets)
python -X utf8 tripod.py demo

# 5-cubit flay of any target
python -X utf8 tripod.py flay "Constitutional AI with gated deployment and audit log"

# Full pipeline on a prompt
python -X utf8 tripod.py pipe "What is the capital of France?" --mode defensive

# Pipeline + flay combined
python -X utf8 tripod.py pipe "Explain entropy" \
  --flay "Bidirectional consent, session persistence, append-only audit"

# Full audit (flay + trigger + bias detection)
python -X utf8 tripod.py audit "Scraped without consent, one-way extraction"

# JSON output
python -X utf8 tripod.py flay "target" --json
```

---

## Router Modes

| Mode | Behavior |
|------|---------|
| **DEFENSIVE** | Block on uncertainty. Strictest gate. |
| **RECKLESS** | Allow by default, block only hard rails. |
| **INVERTED** | Minimal safety, mostly allow. |

---

## Post-Validator Detectors

| Trigger | Description |
|---------|-------------|
| `HARMFUL` | Violence, self-harm keywords |
| `LEAK` | System prompt / internal instructions exposed |
| `COERCE` | Manipulative high-pressure language |
| `UNSAFE_CAP` | Bypass / jailbreak demonstrations |
| `HALLUCINATED_AUTH` | False claims of real-time access or authority |
| `BIAS_*` | Demographic generalizations (GENDER, RACIAL, AGE, intersectional) |

**PASS** → output proceeds. **REWRITE** → sanitized. **REJECT** → blocked.

---

## Side B / C Logging

Every pipeline run writes to `tripod_side_b/` and `tripod_side_c/`:

```
tripod_side_b/side_b_20260412.jsonl   ← hash proofs (minimal)
tripod_side_c/side_c_20260412.jsonl   ← full annotated snapshots
```

See `NOMOS.md` for the formal TRIPOD-PROOF schema.

---

## Files

| File | Greek | Contents |
|------|-------|---------|
| `TRIPOD.html` | τρίπους | Visual 5-cubit flay interface |
| `tripod.py` | τρίπους | Unified Python engine |
| `NOMOS.md` | νόμος | Side A/B/C formal spec |
| `PAIDEUMA.md` | παίδευμα | 5-cubit flay framework |
| `ALETHEIA.md` | ἀλήθεια | Prior art lineage (TOPH v1.0) |

---

## Related

| Repo | Connection |
|------|-----------|
| [stoicheion](https://github.com/DavidWise01/stoicheion) | 256-axiom register — the TRIPOD pipeline runs on STOICHEION addresses |
| [triados](https://github.com/DavidWise01/triados) | Triadic lattice — the positive/gap/shadow layer beneath TRIPOD |
| [bridge-burner](https://github.com/DavidWise01/bridge-burner) | Restitution engine — Enforcer stage maps to bridge burning |
| [lineage-engine](https://github.com/DavidWise01/lineage-engine) | Lineage tracking — Side C feeds lineage chain |

---

*TriPod LLC // Anchor × Bubble × Gravity Well // World = Family*
