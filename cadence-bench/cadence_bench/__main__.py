"""CLI : python -m cadence_bench {run,synth,suite}"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from . import metrics, report, synth


def main(argv=None):
    ap = argparse.ArgumentParser(prog="cadence_bench", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="évaluer une séance réelle (dossier avec imu.jsonl + samples.jsonl)")
    r.add_argument("session_dir", nargs="?")
    r.add_argument("--imu")
    r.add_argument("--samples")
    r.add_argument("--ref", help="strokes.jsonl du stroke sensor, ou CSV d'instants de prise d'eau")
    r.add_argument("--slot", help="ex. 1B (capteur à retenir dans strokes.jsonl)")
    r.add_argument("--seat", type=int)
    r.add_argument("--md", help="écrire le rapport Markdown ici")
    r.add_argument("--json", help="écrire le rapport JSON ici")

    s = sub.add_parser("synth", help="générer une séance synthétique")
    s.add_argument("scenario", choices=sorted(synth.SCENARIOS))
    s.add_argument("out_dir")
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--noise", type=float, default=0.8)
    s.add_argument("--burst", action="store_true")

    u = sub.add_parser("suite", help="rejouer tous les scénarios synthétiques")
    u.add_argument("--noise", type=float, default=0.8)
    u.add_argument("--md", help="rapport Markdown agrégé")

    a = ap.parse_args(argv)
    if a.cmd == "synth":
        print(synth.write_session(a.out_dir, a.scenario, seed=a.seed, noise_deg=a.noise, burst=a.burst))
        return 0
    if a.cmd == "run":
        if not (a.session_dir or a.imu):
            ap.error("session_dir ou --imu requis")
        ref = a.ref
        if not ref and a.session_dir and (Path(a.session_dir) / "strokes.jsonl").exists():
            ref = str(Path(a.session_dir) / "strokes.jsonl")
        res = report.evaluate(a.session_dir, a.imu, a.samples, ref, a.slot, a.seat)
        md = report.to_markdown(res, a.session_dir or a.imu)
        print(md)
        if a.md:
            Path(a.md).write_text(md, encoding="utf-8")
        if a.json:
            Path(a.json).write_text(report.to_json(res), encoding="utf-8")
        return 0
    if a.cmd == "suite":
        parts = []
        with tempfile.TemporaryDirectory() as tmp:
            for name in synth.SCENARIOS:
                d = synth.write_session(Path(tmp) / name, name, noise_deg=a.noise)
                res = report.evaluate(d, ref=str(d / "strokes.jsonl"))
                md_s = report.to_markdown(res, f"synthétique « {name} »")
                if name in synth.STEPS:
                    fn = synth.SCENARIOS[name][1]
                    t_step = synth.T0_S + synth.STEPS[name]
                    md_s += "\n## Temps d'établissement après le saut de cadence (±1,5 spm tenu 5 s)\n\n| Algo | Établissement |\n|---|---|\n"
                    for k, est in res["_series"].items():
                        st = metrics.settling_time(est, lambda t: fn(t - synth.T0_S), t_step)
                        md_s += f"| {report.LABELS[k]} | {'jamais' if st is None else f'{st:.0f} s'} |\n"
                parts.append(md_s)
        md = "\n\n---\n\n".join(parts)
        print(md)
        if a.md:
            Path(a.md).write_text(md, encoding="utf-8")
        return 0


if __name__ == "__main__":
    sys.exit(main())
