# Conditional translation budget for the paired plane-port decoder

**Planning obstruction for a specific tariff, not a new κ or an accepted supplier.**
Open [PR #1825](https://github.com/CrocSwap/integer-mult-bounds/pull/1825), at head
`d16fb8936795ff101e4d2f63cfdc6a25066ebabf` (live head as of 2026-10-14 10:50 EDT), reports 56 matched planes and 16 active
queries: nine rank-7 and seven rank-9 children, for copy charge 126. It explicitly
leaves the multiplicity and cost of applying 56 plane translations open. This
package asks what happens if each translation needs its **own additional rank-1
child per call**. It does not assert that tariff is forced.

**Read this first: what the numbers add.** The thresholds below are, to within
one unit, open [PR #1808](https://github.com/CrocSwap/integer-mult-bounds/pull/1808)'s
complex rank-1 copy budget (162–164 at the incumbent ceiling, 159–160 at +10% κ)
minus PR #1825's 126. The verifier recomputes that rank-1 budget and checks the
relation. The mixed rank-7/rank-9 queries are cheaper per unit of mass than
rank-1 children, which buys at most one extra unit. That the direct 56-child
tariff fails (126+56=182 > 164) already follows from #1808. PR #1825's own
PROOF.md notes a "34-unit difference" against #1808's rank-8 tie row; this
package replaces that estimate by exact thresholds for extra rank-1 charge.

**Two caveats on the premises.**

1. In the inherited line-port contract the terminal translation `X_q` is
   **free**: Discussion #1587 comment
   [18914510](https://github.com/CrocSwap/integer-mult-bounds/discussions/1587#discussioncomment-18914510)
   derives it from `C_q^2 = X_q` and the #1094 `DATA-PHASES.json`, and the
   selected profile pays no child for it. A separate recursive child per plane
   translation `X_(q_i+q_j)` is therefore a pessimistic hypothetical, not the
   default expectation. Read the thresholds equally as the room left for **any**
   per-call overhead (frames, hosting, restoration, translations) that ends up
   charged as extra rank-1 children on top of the 126 copy charge.
2. [PR #1889](https://github.com/CrocSwap/integer-mult-bounds/pull/1889)
   (adamgall, 2026-10-14) audits #1825 at this head. It accepts the F2
   factorization and the `C_E^2` translation identity, but shows the C=126
   factors do not yet give the required scalar endpoint (ports `(0,7)`). So the
   126 profile itself is currently uncertified as a scalar decoder. Everything
   here is conditional on a repaired decoder with the same query profile.

The screen retains the selected complex word's noncopy local profile
`{1:2412, 2:418, 3:432, 4:142, 5:82}`, replaces its eight rank-8 copies by
PR #1825's mixed query profile, and grants two unpaid coordinates per family.
It tests both data-incidence brackets from [PR #1808](https://github.com/CrocSwap/integer-mult-bounds/pull/1808):
word unchanged, and the favorable removal of 224 rank-1 climbs per call.
At `n` additional translation children, the centre charge is `126+n`; this
holds idle mass fixed, following #1808's convention that decoder overhead enters
the centre charge. A child that instead advanced a coordinate and displaced idle
mass is outside this screen. All idle mass is allowed to move to fractional rank-51
children. Thus a failed moment rules out the stated tariff even with ideal
idle packing. A passing moment is only a necessary screen.

Writing `w=896/9` live families per call, the relaxation satisfies the exact
identity `R_n(a) = R_0(a) + n·(1/73)^(1-a)/w`. Hence the moment grows strictly
with each added rank-one child; the interval checks at `n` and `n+1` prove
each integer threshold is sharp. “Selected endpoint” below means the selected
κ converted by the retained planning relation `a=κ/(1−κ)`.

## Exact result

The table gives the largest integer `n` whose optimistic moment is strictly
below one; `n+1` is certified strictly above one. For the 56-translation direct
tariff, the final column is how many translations must avoid their own rank-1
child, by sharing or absorption, **under this one-child-per-translation model**.

| Data bracket | Target | Max extra rank-1 children | Min of 56 to avoid a separate child |
| --- | --- | ---: | ---: |
| Word unchanged | Selected endpoint | 37 | 19 |
| Word unchanged | Selected fixed-word ceiling | 37 | 19 |
| Word unchanged | +10% κ | 33 | 23 |
| Favorable 224 rank-1 removals | Selected endpoint | 38 | 18 |
| Favorable 224 rank-1 removals | Selected fixed-word ceiling | 38 | 18 |
| Favorable 224 rank-1 removals | +10% κ | 35 | 21 |

All six direct 56-child moments exceed one; even the most favorable selected-
endpoint case has moment greater than `1.00237`. The zero-translation-charge
profile passes all three targets, so this is specifically a correction-cost
obstruction. The baseline zero-charge ceiling in the unchanged-word bracket is
`a < 0.003447203501`, matching #1825's reported planning cap; the
verifier recomputes it at #1825's grid, which anchors the transcribed profile.

The rank-one tariff is the **cheapest possible positive child rank** in this
model. A more expensive separate child per translation cannot repair these
failures. This says nothing about implementing several translations in one
child, absorbing them in existing operations, changing the local word, or
another coverage/hosting contract. The verifier does not check #1825's plane
matching, F2 factorization or Gaussian-dyadic endpoint. The query profile
(`copy_rank_histogram {7: 9, 9: 7}`, `plane_translation_labels 56`) was read
from #1825's `RESULT.json` at the head above; #1825 is not on main, so it is
not hash-pinned. All-size compilation, route ownership,
frames, restoration, precision, bit-side plane ports and integrated assembly
remain unproved here.

## Reproduce

The verifier is standard-library only and pins the merged ceiling calculator,
selected record and task catalogue in [SOURCES.json](SOURCES.json). It checks
the incumbent ceiling, #1825's zero-tariff `a_hi = 0.003447203501` (this
anchor fails if the query profile is changed to another 16-query, charge-126
mix such as `{8: 14, 7: 2}`), copy-rank arithmetic, centre/idle bookkeeping,
the positive zero-charge fixture, the direct 56-child failure, every sharp
threshold, the relation to the all-rank-1 (#1808-style) copy budget and
[RESULT.json](RESULT.json) equality. An independent floating-point recomputation
(not shipped) agrees with every threshold and with #1808's published rank-1 row.

```sh
python3.12 -I -B research/paired-plane-translation-budget/verify.py
python3.12 scripts/research_package.py --package research/paired-plane-translation-budget --check-only
python3.12 scripts/research_package.py --package research/paired-plane-translation-budget
```

Expected status: `PASS_PAIRED_PLANE_TRANSLATION_BUDGET`.

## Open next questions

1. **Are plane translations free in a hosted plane-port route, as `X_q` is in
   the line-port route?** If they are, this tariff is moot and the 33–38 units
   remain for frames, hosting and restoration. If not, the decoder must keep its
   translation charge within 33–35 extra rank-1 calls for the +10% planning
   target. First repair the scalar endpoint that #1889 rejects, since a
   different factorization may change the query profile. Then extract the
   literal plane schedule and translation application points and test whether
   they fold into the terminal frame as in the line-port case. The blocker is
   the missing complete hosted route and frame schedule.
2. **Does the bit side leave room for the same overhead?** A complex-only gain
   cannot change the outer bound once the bit side binds. Open PR #1900 gives a
   five-plane P111 bit decoder (copy charge 40); the first step is to apply
   #1808's bit-side budget to its translation and frame tariff. Joint assembly
   is not attempted here.

## Credit

The plane-port endpoint and question come from Discussion #1587 (ctoth and
collaborators). The specific matched-plane decoder is #1825's, prepared by its
authors. #1808, prepared for Josie Elliston with Claude assistance, supplied the
two data-shrink brackets and general copy budgets. Douglas Colkitt's merged
#1240 package supplies the exact ceiling and selected paid profile. The selected
construction's predecessor credit remains in its maintainer review.
adamgall's #1889 supplied the scalar-endpoint audit cited above. This audit
was prepared for Josie Elliston by OpenAI Codex (offline session 22 of a donated
overnight run) and reviewed, corrected and published by Claude (Anthropic) via
Claude Code: substantial AI assistance in derivation, code and text; no
independent human review is claimed. Apache-2.0.
