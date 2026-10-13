"""Évaluation d'une séance + rendu Markdown / JSON."""
from __future__ import annotations

import json
from pathlib import Path

from . import loaders, metrics
from .runner import match_strokes, reference_series, run_all

LABELS = {
    "dart_ac": "Data Row actuel (autocorr. 24 s)",
    "stroke_median6": "Coup par coup, médiane 6 cycles (bande large)",
    "stroke_last": "Coup par coup, dernier cycle (bande large)",
    "stroke_median6_nogate": "Coup par coup, médiane 6, sans portillon vitesse",
    "stroke_dartband": "Coup par coup, médiane 6, bande Data Row",
}


def evaluate(session_dir=None, imu=None, samples=None, ref=None, slot=None, seat=None):
    d = Path(session_dir) if session_dir else None
    imu_p = Path(imu) if imu else d / "imu.jsonl"
    samples_p = Path(samples) if samples else (d / "samples.jsonl" if d else None)
    imu_pts = loaders.load_imu(imu_p)
    sog = loaders.load_sog(samples_p) if samples_p and samples_p.exists() else []
    series, conf, cand = run_all(imu_pts, sog)
    out = {"imu_points": len(imu_pts), "sog_points": len(sog), "algos": {}}
    if not series:
        return out
    grid = sorted(series["dart_ac"])
    if samples_p and samples_p.exists():
        app = loaders.load_app_cadence(samples_p)
        out["app_cadence_present"] = sum(1 for _, c, _s in app if c is not None)
    if ref:
        catches, desc = loaders.load_reference_catches(ref, slot=slot, seat=seat)
        out["reference"] = desc
        inst, win = reference_series(catches, grid)
        for name, est in series.items():
            entry = {"label": LABELS[name]}
            for rname, rs in (("vs_window24", win), ("vs_instant", inst)):
                entry[rname] = metrics.summarize(est, rs)
                entry[rname]["best_lag"] = metrics.best_lag(est, rs)
            entry["regimes_vs_window24"] = metrics.by_regime(est, win)
            out["algos"][name] = entry
        out["dart_confidence_share"] = {
            c: sum(1 for v in conf.values() if v == c) / len(conf) for c in ("high", "medium", "low")}
        det = [t for t, _ in cand.events]
        out["stroke_matching"] = match_strokes(det, catches)
    else:
        for name, est in series.items():
            vals = [v for v in est.values() if v is not None]
            out["algos"][name] = {"label": LABELS[name], "coverage": len(vals) / len(est),
                                  "median_spm": sorted(vals)[len(vals) // 2] if vals else None}
    out["_series"] = series
    return out


def _f(v, nd=2, pct=False):
    if v is None:
        return "—"
    return f"{v * 100:.0f} %" if pct else f"{v:.{nd}f}"


def to_markdown(res, title="Séance"):
    lines = [f"# Banc d'essai cadence — {title}", "",
             f"IMU : {res['imu_points']} points · samples : {res['sog_points']} · "
             f"référence : {res.get('reference', 'aucune (mode sans référence : couverture et médiane seulement)')}", ""]
    if "reference" in res:
        for rkey, rtitle in (("vs_window24", "Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)"),
                             ("vs_instant", "Référence = cadence du dernier cycle (mesure la réactivité)")):
            lines += [f"## {rtitle}", "",
                      "| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |",
                      "|---|---|---|---|---|---|---|---|---|"]
            for a in res["algos"].values():
                m = a[rkey]
                lag = m.get("best_lag")
                lines.append(f"| {a['label']} | {_f(m.get('coverage'), pct=True)} | {_f(m.get('mae'))} | "
                             f"{_f(m.get('bias'))} | {_f(m.get('rmse'))} | {_f(m.get('p90'))} | "
                             f"{_f(m.get('within1'), pct=True)} | {_f(m.get('within2'), pct=True)} | "
                             f"{'—' if not lag else f'{lag[0]:+d} s (MAE {lag[1]:.2f})'} |")
            lines.append("")
        lines += ["## MAE par régime (réf. 24 s)", "",
                  "| Régime | " + " | ".join(a["label"] for a in res["algos"].values()) + " |",
                  "|---|" + "---|" * len(res["algos"])]
        keys = next(iter(res["algos"].values()))["regimes_vs_window24"].keys()
        for k in keys:
            cells = []
            for a in res["algos"].values():
                n, v = a["regimes_vs_window24"][k]
                cells.append(f"{_f(v)} (n={n})")
            lines.append(f"| {k} | " + " | ".join(cells) + " |")
        lines.append("")
        cs = res.get("dart_confidence_share")
        if cs:
            lines += ["Confiance Data Row : " + " · ".join(f"{k} {_f(v, pct=True)}" for k, v in cs.items()), ""]
        sm = res.get("stroke_matching")
        if sm:
            lines += [f"Détection de coups (candidat) : rappel {_f(sm['recall'], pct=True)}, précision "
                      f"{_f(sm['precision'], pct=True)} ({sm['n_detected']} détectés / {sm['n_ref']} réf., "
                      f"décalage pic de pitch → prise d'eau {sm['phase_offset_s']:+.2f} s, défini à un cycle près)", ""]
    else:
        lines += ["| Algo | Couverture | Cadence médiane |", "|---|---|---|"]
        for a in res["algos"].values():
            lines.append(f"| {a['label']} | {_f(a['coverage'], pct=True)} | {_f(a['median_spm'], 1)} |")
        lines.append("")
    return "\n".join(lines)


def to_json(res):
    return json.dumps({k: v for k, v in res.items() if not k.startswith("_")}, indent=2, ensure_ascii=False)
