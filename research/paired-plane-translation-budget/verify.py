#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact conditional translation tariff screen for PR1825's paired-plane decoder.

Only the mixed query ranks and plane count are transcribed from PR1825 at head
d16fb893 (its RESULT.json copy_rank_histogram and plane_translation_labels,
checked against the live PR on 2026-10-14). That branch is not on main, so it
is not hash-pinned here; the zero-tariff ceiling is instead checked against
PR1825's reported a_hi. This is an optimistic moment screen, not an endpoint
or hosting verifier.
"""
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCES = json.loads((HERE / "SOURCES.json").read_text())


def need(ok, why):
    if not ok:
        raise ValueError(why)


def source(path):
    entries = [x for x in SOURCES["files"] if x["path"] == path]
    need(len(entries) == 1, "missing source pin: " + path)
    data = (ROOT / path).read_bytes()
    need(hashlib.sha256(data).hexdigest() == entries[0]["sha256"], "source drift: " + path)
    return data


spec = importlib.util.spec_from_file_location("pinned_ceiling", ROOT / "research/complex-local-word-ceiling/ceiling.py")
C = importlib.util.module_from_spec(spec)
source("research/complex-local-word-ceiling/ceiling.py")
spec.loader.exec_module(C)

M, FAMILIES, STAGES = 73, 896, 9
LINE_WORD = {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8}
QUERY_RANKS = {7: 9, 9: 7}  # PR1825: 9*7 + 7*9 = 126
PLANES = 56
DATA_DROP = 224  # two selected data incidences per 112 ports, one shorter climb
GRID = Q(1, 10**15)


def profile(shrink, extra):
    """Replace old copies, optionally take maximum favorable data shrink."""
    w = dict(LINE_WORD)
    w.pop(8)
    for r, n in QUERY_RANKS.items():
        w[r] = w.get(r, 0) + n
    if shrink:
        w[1] -= DATA_DROP
    w[1] += extra
    need(w[1] >= 0 and 0 <= extra <= PLANES, "profile range")
    return w


def moment(shrink, extra, a):
    w = profile(shrink, extra)
    centre = 126 + extra
    q = C.model(w, M, FAMILIES, STAGES, centre, unpaid=2)
    return q, C.relax(w, M, FAMILIES, STAGES, centre, a, unpaid=2)


def verdict(shrink, extra, a):
    _, (lo, hi) = moment(shrink, extra, a)
    need(hi < 1 or lo > 1, "undecided interval at %s %s %s" % (shrink, extra, a))
    return "pass" if hi < 1 else "fail"


def budget(shrink, a):
    need(verdict(shrink, 0, a) == "pass", "zero-tariff control")
    need(verdict(shrink, PLANES, a) == "fail", "56-tariff control")
    lo, hi = 0, PLANES
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (mid, hi) if verdict(shrink, mid, a) == "pass" else (lo, mid)
    need(verdict(shrink, lo, a) == "pass", "threshold passes")
    need(verdict(shrink, lo + 1, a) == "fail", "threshold+1 fails")
    return lo


def rank1_copy_budget(shrink, a):
    """PR1808-style comparison: largest C with all copy charge in rank-1 children."""
    def ok(c):
        w = {r: n for r, n in LINE_WORD.items() if r != 8}
        w[1] += c - (DATA_DROP if shrink else 0)
        lo, hi = C.relax(w, M, FAMILIES, STAGES, c, a, unpaid=2)
        need(hi < 1 or lo > 1, "undecided rank-1 comparison")
        return hi < 1
    lo, hi = 0, 250
    need(ok(lo) and not ok(hi), "rank-1 comparison window")
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (mid, hi) if ok(mid) else (lo, mid)
    return lo


def main(write):
    selected = json.loads(source("certificates/selected-result.json"))
    source("docs/research/agent-task-catalog.json")
    k = Q(selected["kappa"])
    need(k == Q(836330098538459, 500000000000000000), "selected record changed")
    a_selected = k / (1 - k)
    k10 = Q(11, 10) * k
    a10 = k10 / (1 - k10)

    need(sum(r * n for r, n in QUERY_RANKS.items()) == 126, "query bill")
    need(sum(QUERY_RANKS.values()) == 16, "active query count")
    need(C.max_idle_rank(M) == 51, "idle cap")
    old = C.ceiling(LINE_WORD, M, FAMILIES, STAGES, 64, grid=GRID)[1]
    need(old == Q(1690054109089, 10**15), "incumbent packing cap")
    need(sum(r * n for r, n in LINE_WORD.items()) == 5586, "selected paid local mass")
    # Anchor the transcribed profile: PR1825 reports a_hi = 0.003447203501 at
    # unpaid=2, centre=126, grid 1e-12 for exactly this zero-tariff profile.
    pr1825 = C.ceiling(profile(False, 0), M, FAMILIES, STAGES, 126, grid=Q(1, 10**12), unpaid=2)[1]
    need(pr1825 == Q(3447203501, 10**12), "PR1825 zero-tariff ceiling not reproduced")
    need(sum(r * n for r, n in profile(False, 0).items()) == 5648, "PR1825 local mass")

    targets = {"selected_endpoint": a_selected, "selected_word_ceiling": old, "kappa_plus_10pct": a10}
    rows = {}
    for name, shrink in (("word_unchanged", False), ("data_shrink_as_rank1", True)):
        q0, _ = moment(shrink, 0, a_selected)
        q56, _ = moment(shrink, PLANES, a_selected)
        need(q0["idle_mass"] == q56["idle_mass"], "extra calls displaced idle mass")
        need(q56["local_mass"] - q0["local_mass"] == PLANES, "extra rank-one mass")
        need(q56["total_mass"] - q0["total_mass"] == PLANES, "centre charge bookkeeping")
        rows[name] = {
            "idle_mass_per_call": str(q0["idle_mass"]),
            "base_query_charge": 126,
            "direct_translation_calls": PLANES,
            "targets": {},
        }
        for target, a in targets.items():
            n = budget(shrink, a)
            c1 = rank1_copy_budget(shrink, a)
            # Relationship to PR1808: higher-rank queries are cheaper per unit
            # mass, so the mixed total 126+n sits at or just above the all-rank-1
            # copy budget.
            need(c1 <= 126 + n <= c1 + 1, "unexpected gap to rank-1 copy budget")
            _, (lo, hi) = moment(shrink, PLANES, a)
            need(lo > 1, "direct 56-child tariff must fail")
            rows[name]["targets"][target] = {
                "maximum_extra_rank1_calls": n,
                "minimum_56_translations_absorbed_or_shared": PLANES - n,
                "direct_56_moment_interval": [str(lo), str(hi)],
                "all_rank1_copy_budget_for_comparison": c1,
            }
    need(rows["data_shrink_as_rank1"]["targets"]["kappa_plus_10pct"]["maximum_extra_rank1_calls"] >=
         rows["word_unchanged"]["targets"]["kappa_plus_10pct"]["maximum_extra_rank1_calls"],
         "favorable bracket reversed")

    out = {
        "status": "PASS_PAIRED_PLANE_TRANSLATION_BUDGET",
        "model": "PR1825 mixed query profile, two unpaid coordinates, ideal rank-51 idle packing; n extra rank-one children and matching centre charge per call",
        "pr1825_head": "d16fb8936795ff101e4d2f63cfdc6a25066ebabf",
        "pr1825_zero_tariff_a_hi": str(pr1825),
        "targets": {key: str(value) for key, value in targets.items()},
        "rows": rows,
    }
    artifact = HERE / "RESULT.json"
    rendered = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if write:
        artifact.write_text(rendered)
    else:
        need(artifact.read_text() == rendered, "RESULT.json drift")
    print(out["status"])
    for name, row in rows.items():
        print(name, "idle", row["idle_mass_per_call"])
        for target, result in row["targets"].items():
            print(" ", target, "max extra", result["maximum_extra_rank1_calls"],
                  "minimum absorbed", result["minimum_56_translations_absorbed_or_shared"],
                  "all-rank-1 C", result["all_rank1_copy_budget_for_comparison"])


if __name__ == "__main__":
    need(sys.version_info >= (3, 10), "Python 3.10+")
    main("--write" in sys.argv[1:])
