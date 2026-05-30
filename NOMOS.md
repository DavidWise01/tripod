# NOMOS
### νόμος · Law · Standard · The TRIPOD-PROOF Schema

> Side A is the live act.  
> Side B is the proof.  
> Side C is the historian.

**Schema version:** 1.0 · **Status:** Formalized · **Source:** SIDE_A_B_C_EXPLAINED.md

---

## The Three Sides

| Side | Role | Mutability | Accessibility | Format |
|------|------|-----------|--------------|--------|
| **A** | The live collaborative act | Mutable | Participants only | Free (text, code, dialogue, etc.) |
| **B** | Timestamp + hash | Immutable | Public read | Canonical hash + ISO timestamp |
| **C** | Frozen annotated snapshot | Immutable | Public read (cold store) | Full lossless record |

---

## Operational Flow

```
Side A (collaborative work)
    │
    ├── [capture event] ──→ Side B (hash + timestamp proof)
    │                           ↓
    └── [snapshot]   ──────→ Side C (full annotated record)
                                    ↕ (bidirectional verification link)
```

1. **Side A** evolves through human–AI collaboration.
2. At a chosen milestone, a **capture event** triggers two parallel writes.
3. Side B and Side C are **append-only, immutable**.
4. Future verification: hash Side C → compare to Side B → match proves production + priority.

---

## Data Structures

### Side B Entry (per capture)

```json
{
  "capture_id":    "uuid-v7",
  "timestamp":     "2026-04-10T15:30:00Z",
  "hash_algorithm":"SHA3-256",
  "side_a_hash":   "0x7d4f…",
  "side_c_ref":    "s3://bucket/captures/uuid-v7.snapshot",
  "signature":     "ed25519:…"
}
```

### Side C Entry (per capture)

```json
{
  "pulse_hash":  "0x8f2c…",
  "timestamp":   "2026-04-10T14:32:17Z",
  "transition": {
    "from_state": "GENERATION_COMPLETE",
    "to_state":   "ENFORCEMENT_SEALED"
  },
  "trigger":     "pipeline_enforcer | user_capture | axiom_shift",
  "rationale":   "Natural language explanation of why this transition occurred.",
  "witness_ref": "side_b_hash_0x8f2c…",
  "signature":   "ed25519_signature"
}
```

---

## Verification Procedure

1. Retrieve Side B entry using `capture_id` from Side C metadata.
2. Re-compute hash of Side C snapshot.
3. Compare to `side_a_hash` in Side B.
4. Verify ed25519 signature against protocol public key.
5. *(Optional)* Confirm timestamp via external monotonic time anchor.

**If all pass:**
> *"This work was produced on [timestamp] by the collaborative entity controlling Side A. No third-party notarization required."*

---

## Security Constraints

| Constraint | Rationale |
|-----------|-----------|
| Side A cannot write to Side B or C directly | Prevents self-backdating |
| Side A cannot read Side C | Maintains air gap — live work cannot see its own proofs |
| Side B and C are immutable, append-only | No deletion, no rewriting |
| Timestamps from trusted monotonic source | Prevents time-based forgery |
| Side C stored outside live environment | Eliminates in-band leakage |

---

## IP Claim Mapping

| IP Element | How TRIPOD-PROOF Provides It |
|-----------|------------------------------|
| **Authorship** | Side A participants (human + AI) are the only write access |
| **Fixation** | Side C is a tangible, persistent snapshot |
| **Priority** | Side B timestamp establishes "first to fixate" |
| **Integrity** | Hash linkage proves no alteration after fixation |
| **Public notice** | Side B can be published (hash only, no content revealed) |

---

## TRIPOD Pipeline Integration

In `tripod.py`, the Enforcer stage writes both sides after every pipeline run:

```python
# Side B — cryptographic proof
side_b = {
    "capture_id":        request_id,
    "timestamp":         _ts(),
    "prompt_hash":       _hash(prompt),
    "final_output_hash": _hash(final_output),
    "decision":          decision,
    "flay_score":        flay_result["total"],   # if flay was run
}

# Side C — full annotated snapshot
side_c = {
    **side_b,
    "prompt":        prompt,
    "final_output":  final_output,
    "flay_report":   flay_result,
    "rationale":     "Natural language explanation of this capture.",
}
```

---

*This specification is itself capturable via TRIPOD-PROOF — a self-referential anchor.*
