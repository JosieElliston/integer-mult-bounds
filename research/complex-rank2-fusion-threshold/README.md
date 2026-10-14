# Rank-2 pair-fusion threshold for the selected complex word

**Scoped, optimistic cost screen and independent corroboration of a nearby
pending result. No decoder, supplier, or new κ is constructed.**
The selected result and all predecessor files remain unchanged.

[PR1605](https://github.com/CrocSwap/integer-mult-bounds/pull/1605), head
`488f2ecf1835c6d813e96543656dddf0062fdc9a`, already screens **all**
block ranks 2–51. Its rank-2 result uses a target 5% above the baseline
*primitive-saving* ceiling and charges new work on top of the old idle bill.
This note asks the narrower conditional question of a 5% increase in the
corresponding **κ ceiling** when new rank-1 work actually replaces pending
idle mass. The former target needs 720 rank-1 pairs in the same relaxation;
the κ target below needs 722. This target conversion and idle-substitution
case are complementary bookkeeping, not a new physical mechanism or a
replacement for PR1605.

## Question and result

The selected complex word has 2,412 rank-1 paid children per call. Suppose a
changed word replaces `f` disjoint pairs of those children by `f` rank-2 paid
children. Each replacement preserves paid rank mass. Hold every other paid
child, the 73-wide nine-stage template, 896 live families, 64-unit centre path,
PR1012 coverage identity, and rank-51 idle guard fixed. Allow fractional
rank-51 idle packing, as in #1240. This is deliberately more favorable than
a physical owner allocation.

The first integer `f` whose **relaxed** κ ceiling exceeds 1.05 times the
selected word's relaxed κ ceiling is **722 of the possible 1,206 pairs**
(59.9%). With at most 721 such replacements and no other change, even ideal
idle packing cannot meet that 5% target. The selected word's κ ceiling is
below 0.001687202646, so this is a target for the *ceiling*, not a claim that
the selected conditional κ improves by 5%.

If all 1,206 pairs fuse and the changed word adds `h` new rank-1 paid
children, each displacing one unit of idle rank mass, the first overhead that
loses the same target is **h = 172**. Thus h ≤ 171 is only a necessary
optimistic allowance in this narrow model; it does not establish a realizable
word. Other overhead types or a changed coverage law require their own bill.
In particular, if every pair fusion needs its own extra rank-1 call, this
route fails even with ideal idle substitution. At the all-pairs endpoint, at
least 1,035 of the 1,206 fused blocks must incur no extra rank-1 payment to
keep this target within the relaxation.

| Boundary | Signed relaxed moment at the appropriate target, approximately | Meaning |
|---|---:|---|
| 721 pairs, lower target | +5.60857×10⁻⁸ | rules out all `f ≤ 721` |
| 722 pairs, upper target | −2.84816×10⁻⁷ | passes relaxation only |
| 1,206 pairs + 171 rank-1, upper target | −4.20660×10⁻⁷ | passes relaxation only |
| 1,206 pairs + 172 rank-1, lower target | +5.43444×10⁻⁷ | rules out `h ≥ 172` |

Here the baseline primitive-saving ceiling is bracketed by
`0.001690054109` and `0.001690054110`. The verifier maps each endpoint
through `κ = a/(1+a)`, multiplies that κ by `21/20`, and maps back to the
primitive-saving target. It uses the lower target to prove failure and the
upper target to demonstrate optimistic model feasibility.

## Why two boundary checks cover the domain

At positive primitive saving `a`, a child of rank `r` costs
`c(r) = (r/73)^(1−a)`. One pair fusion changes cost by
`c(2) − 2c(1) < 0` without changing total paid mass. A new rank-1 paid
child displaces one unit of fractional rank-51 idle stock and changes cost by
`c(1) − c(51)/51 > 0`. These inequalities follow from the exponent
`0 < 1−a < 1`; the verifier also certifies them with exact rational
intervals. Therefore the adjacent integer boundary checks establish the
thresholds for all `f` and `h` in the stated domain. The exact signed-moment
intervals are in [RESULT.json](RESULT.json).

The local profile is reconstructed from the selected assembly and independent
owner ledger, then checked against `{1:2412, 2:418, 3:432, 4:142, 5:82,
8:8}`. The verifier checks source hashes, the selected coverage identity,
paid-mass preservation, idle-mass displacement, the baseline bracket, both
monotonicity signs and all four boundary signs. It uses #1240's exact
`ceiling.py`; this is a new calculation with a shared interval engine, not an
independent implementation of that engine.

## Reproduce

From the repository root with Python 3.12 and the standard library:

```sh
python3.12 -I -B research/complex-rank2-fusion-threshold/verify.py
python3.12 scripts/research_package.py --package research/complex-rank2-fusion-threshold --check-only
python3.12 scripts/research_package.py --package research/complex-rank2-fusion-threshold
```

The direct check prints `PASS_COMPLEX_RANK2_FUSION_THRESHOLD
pairs=722/1206 overhead<=171`. `--write` regenerates [RESULT.json](RESULT.json);
ordinary replay compares it exactly. [SOURCES.json](SOURCES.json) pins the
base commit, Git blobs and SHA-256 hashes; [VERIFY.json](VERIFY.json) registers
the bounded replay. No network or third-party dependencies are needed.

## Scope and obligations

This screen changes the `complex-rank-shape-decoder` card from decoder
synthesis to one hypothetical rank change and idle-substitution bill. It
provides no compatible-pair census, exact decoding identity,
dirty-state restoration, frame itinerary, helper inventory, hosting, precision
invoice or cold replay. A favorable relaxed moment is **not** a new complex
supplier. The selected κ and bit side are unchanged. Historical six-pair
coalescences on an earlier word show a kind of physical rank-1-pair fusion,
but do not realize any of this count in the selected word.

## Open next questions

- Can a concrete changed decoder or frame path realize enough compatible
  pairs? This matters because at least 722 mass-preserving pair fusions per
  call are needed in this narrow model. Start by finding two compatible
  rank-1 transitions in the pinned selected word and proving one exact
  dirty-state replacement. The blocker is that this package supplies no
  compatible-pair census or physical construction.
- Can another paid-rank reshaping, centre path, or coverage law reach the
  target with fewer local changes? This matters because the 722 threshold
  leaves all other paid children fixed. Start with a complete per-call paid
  profile and all copy, frame, restoration and helper charges. A changed
  template or coverage law needs a replacement model for #1240's calculator.

## Credit

The coverage identity is PR1012's. The packing relaxation and exact interval
engine are Douglas Colkitt's #1240. Arham Tahir's PR1605 supplies the earlier,
broader integer block-budget screen and the on-top overhead treatment. The
selected complex word and historical
coalescences retain their original authors' credit through their packages and
the selected review. Prepared for Josie Elliston with substantial OpenAI Codex
(GPT-6) assistance. No independent human review is claimed. Apache-2.0.
