"""End-to-end pipeline runner.

Usage:
  python -m handbook_rs.pipeline                # run all stages, skipping cached ones
  python -m handbook_rs.pipeline --force        # force every stage
  python -m handbook_rs.pipeline --from 4       # force stage 4 onward
  python -m handbook_rs.pipeline --only 7       # run just stage 7
"""

from __future__ import annotations

import argparse

from . import (stage0_fetch, stage1_clean, stage2_mine, stage3_canonicalize,
               stage4_define_close, stage5_graph, stage5b_lineage, stage6_translate,
               stage7_emit, stage8_validate, stage10_clusters, stage9_app)

STAGES = [
    (0, "fetch", stage0_fetch.run),
    (1, "clean", stage1_clean.run),
    (2, "mine", stage2_mine.run),
    (3, "canonicalize", stage3_canonicalize.run),
    (4, "define+close", stage4_define_close.run),
    (5, "graph", stage5_graph.run),
    (55, "lineage", stage5b_lineage.run),
    (6, "translate", stage6_translate.run),
    (7, "emit", stage7_emit.run),
    (8, "validate", stage8_validate.run),
    (85, "clusters", stage10_clusters.run),
    (9, "app", stage9_app.run),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="force all stages")
    ap.add_argument("--from", dest="from_stage", type=int, default=None)
    ap.add_argument("--only", type=int, default=None)
    args = ap.parse_args()

    for num, name, fn in STAGES:
        if args.only is not None and num != args.only:
            continue
        force = args.force or (args.from_stage is not None and num >= args.from_stage)
        print(f"\n=== Stage {num}: {name} ===")
        fn(force=force)
    print("\nPipeline complete. Deliverables in out/: ontology.json, glossary.md, vault/, graph.html")


if __name__ == "__main__":
    main()
