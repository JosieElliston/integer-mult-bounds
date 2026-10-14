#!/usr/bin/env python3
"""Certified ideal threshold for rank-1-pair to rank-2 fusion.

This checks a cost relaxation, not a realizable frame path or multiplication
supplier. The exact interval engine is the pinned predecessor #1240's ceiling.py.
SPDX-License-Identifier: Apache-2.0
"""
import hashlib
import json
import sys
import argparse
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research/complex-local-word-ceiling"))
import ceiling as C  # noqa: E402

M, FAMILIES, STAGES, CENTRE = 73, 896, 9, 64
GRID = Q(1, 10**12)
MULTIPLIER = Q(21, 20)
EXPECTED_LOCAL = {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pinned_sources():
    manifest = json.loads((HERE / "SOURCES.json").read_text())
    for entry in manifest["files"]:
        if entry["usage"] == "input":
            data = (ROOT / entry["path"]).read_bytes()
            require(hashlib.sha256(data).hexdigest() == entry["sha256"],
                    "source drift: " + entry["path"])


def selected_local():
    rec = json.loads((ROOT / "certificates/selected-result.json").read_text())
    require(rec["certificate"] == "research/community-frontier1094-audit/ASSEMBLY.json",
            "selected certificate changed")
    assembly = json.loads((ROOT / rec["certificate"]).read_text())
    independent = json.loads((ROOT / "research/community-frontier1094-audit/INDEPENDENT1094.json").read_text())
    profile = {int(r): int(n) for r, n in assembly["complex_profile"].items()}
    require(profile == {int(r): int(n) for r, n in independent["owner"]["profile"].items()},
            "two selected profiles disagree")
    idle = {int(r): int(n) for r, n in independent["owner"]["idle"].items()}
    calls, live = independent["price"]["calls"], independent["price"]["live"]
    require(calls == 144 and live == 896 * 16, "selected call geometry changed")
    require(sum(r * n for r, n in profile.items()) == 72 * live + CENTRE * calls,
            "selected coverage law changed")
    local = {}
    for r in set(profile) | set(idle):
        paid = profile.get(r, 0) - idle.get(r, 0)
        require(paid >= 0 and paid % calls == 0, "local split invalid")
        if paid:
            local[r] = paid // calls
    require(local == EXPECTED_LOCAL, "selected local profile changed")
    require(all(0 < r <= 51 for r in idle), "idle rank violates guard")
    return local


def target_a(baseline_a):
    kappa = MULTIPLIER * baseline_a / (1 + baseline_a)
    require(kappa < 1, "invalid target")
    return kappa / (1 - kappa)


def fused(local, pairs, overhead=0):
    require(0 <= pairs <= local[1] // 2 and overhead >= 0, "invalid hypothetical counts")
    out = dict(local)
    out[1] = local[1] - 2 * pairs + overhead
    out[2] = local[2] + pairs
    C.model(out, M, FAMILIES, STAGES, CENTRE)
    return out


def signed_moment(local, pairs, overhead, a):
    lo, hi = C.relax(fused(local, pairs, overhead), M, FAMILIES, STAGES, CENTRE, a)
    return lo - 1, hi - 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="regenerate RESULT.json")
    args = parser.parse_args()
    pinned_sources()
    local = selected_local()
    base_lo, base_hi = C.ceiling(local, M, FAMILIES, STAGES, CENTRE, grid=GRID)
    require(base_lo == Q(1690054109, 10**12) and base_hi == Q(169005411, 10**11),
            "baseline bracket changed")
    a_lo, a_hi = target_a(base_lo), target_a(base_hi)

    # Each pair replaces two rank-1 children by one rank-2 child at fixed mass.
    # For a>0, r^(1-a) is strictly concave: 2 c(1) > c(2), so each
    # additional fusion strictly decreases the relaxed moment. An added rank-1
    # child displaces one mass unit of fractional rank-51 idle stock and raises
    # the moment because c(1) > c(51)/51. Boundary checks cover all integers.
    c1, c2, c51 = C.child_cost(1, M, a_lo), C.child_cost(2, M, a_lo), C.child_cost(51, M, a_lo)
    require(2*c1[0] > c2[1], "pair benefit not certified")
    require(c1[0] > c51[1]/51, "overhead penalty not certified")
    require(C.model(fused(local, 1206, 172), M, FAMILIES, STAGES, CENTRE)["idle_mass"] > 0,
            "overhead model outside coverage budget")

    # At the true (unknown within the bracket) 5%-higher baseline cap:
    # 721 pairs are ruled out even at the lower target, while 722 pairs pass
    # the ideal relaxation even at the upper target. Passing is not realization.
    fail_721 = signed_moment(local, 721, 0, a_lo)
    pass_722 = signed_moment(local, 722, 0, a_hi)
    require(fail_721[0] > 0 and pass_722[1] < 0, "fusion threshold not separated")

    # Even if all 1206 disjoint rank-1 pairs fuse for free, adding 172 new
    # rank-1 children exhausts the ideal gain; 171 remains below the target.
    pass_171 = signed_moment(local, 1206, 171, a_hi)
    fail_172 = signed_moment(local, 1206, 172, a_lo)
    require(pass_171[1] < 0 and fail_172[0] > 0, "overhead threshold not separated")

    # Semantic controls: an extra paid rank-1 child displaces idle mass;
    # fusion itself preserves paid mass.
    require(C.model(fused(local, 1206, 1), M, FAMILIES, STAGES, CENTRE)["idle_mass"] ==
            C.model(fused(local, 1206, 0), M, FAMILIES, STAGES, CENTRE)["idle_mass"] - 1,
            "overhead must displace idle mass")
    require(sum(r*n for r, n in fused(local, 722).items()) == sum(r*n for r, n in local.items()),
            "fusion must preserve paid mass")

    result = {
        "base_a_bracket": [str(base_lo), str(base_hi)],
        "target_a_bracket": [str(a_lo), str(a_hi)],
        "target_kappa_bracket": [str(MULTIPLIER*base_lo/(1+base_lo)),
                                  str(MULTIPLIER*base_hi/(1+base_hi))],
        "first_ideal_pair_count": 722,
        "last_ideal_pair_count_ruled_out": 721,
        "all_pairs": 1206,
        "largest_ideal_rank1_overhead_at_all_pairs": 171,
        "first_overhead_ruled_out_at_all_pairs": 172,
        "signed_moment_bounds": {
            "721_pairs_lower_target": [str(v) for v in fail_721],
            "722_pairs_upper_target": [str(v) for v in pass_722],
            "all_pairs_171_overhead_upper_target": [str(v) for v in pass_171],
            "all_pairs_172_overhead_lower_target": [str(v) for v in fail_172],
        },
    }
    if args.write:
        (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        expected = json.loads((HERE / "RESULT.json").read_text())
        require(result == expected, "committed result drift")
    print("PASS_COMPLEX_RANK2_FUSION_THRESHOLD pairs=722/1206 overhead<=171")


if __name__ == "__main__":
    main()
