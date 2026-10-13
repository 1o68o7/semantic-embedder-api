"""Métriques d'erreur d'une série de cadence vs une référence (grille 1 Hz)."""
from __future__ import annotations

import math
import statistics


def _pairs(est, ref, shift=0, grid=1.0):
    out = []
    for t, e in est.items():
        r = ref.get(t - shift * grid)
        if e is not None and r is not None:
            out.append((e, r, t))
    return out


def summarize(est, ref, ref_ts=None):
    """coverage = part des instants où la référence existe ET l'estimateur répond."""
    ref_n = sum(1 for v in ref.values() if v is not None)
    prs = _pairs(est, ref)
    res = {"n_ref": ref_n, "n_pairs": len(prs), "coverage": (len(prs) / ref_n) if ref_n else None}
    if not prs:
        return res
    err = [e - r for e, r, _ in prs]
    ab = sorted(abs(x) for x in err)
    res.update(
        bias=statistics.fmean(err),
        mae=statistics.fmean(ab),
        rmse=math.sqrt(statistics.fmean(x * x for x in err)),
        p90=ab[min(len(ab) - 1, int(0.9 * len(ab)))],
        within1=sum(1 for x in ab if x <= 1) / len(ab),
        within2=sum(1 for x in ab if x <= 2) / len(ab),
    )
    return res


def best_lag(est, ref, max_lag_s=40, grid=1.0, min_pairs=20, min_ref_std=2.0):
    """Décalage L (s) minimisant le MAE de est(T) vs ref(T-L). L>0 : l'estimateur est en retard."""
    vals = [v for v in ref.values() if v is not None]
    if len(vals) < min_pairs or statistics.pstdev(vals) < min_ref_std:
        return None  # référence trop plate : le retard n'est pas identifiable
    best = None
    for lag in range(-max_lag_s, max_lag_s + 1):
        prs = _pairs(est, ref, shift=lag, grid=grid)
        if len(prs) < min_pairs:
            continue
        mae = statistics.fmean(abs(e - r) for e, r, _ in prs)
        if best is None or mae < best[1]:
            best = (lag, mae, len(prs))
    return best


def by_regime(est, ref, grid=1.0):
    """MAE par tranche de cadence de référence et en phase stable / transitoire."""
    bands = [("<20", 0, 20), ("20-26", 20, 26), ("26-32", 26, 32), ("32-38", 32, 38), (">=38", 38, 99)]
    out = {}
    prs = _pairs(est, ref)
    for name, lo, hi in bands:
        sel = [abs(e - r) for e, r, _ in prs if lo <= r < hi]
        out[f"ref {name} spm"] = (len(sel), statistics.fmean(sel)) if sel else (0, None)
    stable, trans = [], []
    for e, r, t in prs:
        r10 = ref.get(t - 10 * grid)
        if r10 is None:
            continue
        (trans if abs(r - r10) >= 3 else stable).append(abs(e - r))
    out["stable (|Δref 10 s| < 3)"] = (len(stable), statistics.fmean(stable)) if stable else (0, None)
    out["transition (|Δref 10 s| ≥ 3)"] = (len(trans), statistics.fmean(trans)) if trans else (0, None)
    return out


def settling_time(est, true_fn, t_step, tol=1.5, hold_s=5, grid=1.0):
    """Secondes après `t_step` avant que l'estimation reste dans ±tol de la vérité `hold_s` s de suite.

    `est` : {t_s: spm|None}, `true_fn(t_s) -> spm vrai`. None si jamais atteint.
    """
    ts = sorted(t for t in est if t >= t_step)
    run_start = None
    for t in ts:
        v = est[t]
        ok = v is not None and abs(v - true_fn(t)) <= tol
        if ok:
            run_start = t if run_start is None else run_start
            if t - run_start >= hold_s - grid:
                return run_start - t_step
        else:
            run_start = None
    return None
