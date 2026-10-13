"""Rejoue un imu.jsonl dans chaque estimateur et produit des séries sur grille 1 Hz."""
from __future__ import annotations

import bisect
import statistics

from .dart_port import HIGH, MEDIUM, TelCadenceDetector
from .stroke_detector import StrokeDetector


def _sog_at(sog_series, t_ms):
    """Dernière valeur de vitesse dont l'horodatage <= t (comme estimateSeries du Dart)."""
    keys = [s[0] for s in sog_series]
    i = bisect.bisect_right(keys, t_ms) - 1
    return sog_series[i][1] if i >= 0 else None


def run_all(imu, sog_series, grid_s: float = 1.0, band=(0.25, 1.2), min_sog=1.1):
    """Retourne {nom: {t_s: spm|None}} + {'_conf': {t_s: confiance Dart}} + détails du détecteur."""
    if not imu:
        return {}, {}, None
    imu = sorted(imu, key=lambda p: p.t_ms)
    dart = TelCadenceDetector()
    cand = StrokeDetector(hp_hz=band[0], lp_hz=band[1], min_sog=min_sog)
    cand_wide_nogate = StrokeDetector(hp_hz=band[0], lp_hz=band[1], min_sog=None)
    dart_only_band = StrokeDetector(hp_hz=dart.hp_hz, lp_hz=dart.lp_hz, min_sog=min_sog)

    series = {"dart_ac": {}, "stroke_median6": {}, "stroke_last": {},
              "stroke_median6_nogate": {}, "stroke_dartband": {}}
    conf = {}
    sog_keys = [s[0] for s in sog_series]
    sj = 0
    sog = None
    t_first = imu[0].t_ms / 1000.0
    next_grid = t_first + grid_s

    def snapshot(tg):
        e = dart.recompute()
        series["dart_ac"][tg] = e.spm
        conf[tg] = e.confidence
        series["stroke_median6"][tg] = cand.spm_median(tg)
        series["stroke_last"][tg] = cand.spm_last(tg)
        series["stroke_median6_nogate"][tg] = cand_wide_nogate.spm_median(tg)
        series["stroke_dartband"][tg] = dart_only_band.spm_median(tg)

    for p in imu:
        t = p.t_ms / 1000.0
        while t >= next_grid:
            snapshot(next_grid)
            next_grid += grid_s
        while sj < len(sog_keys) and sog_keys[sj] <= p.t_ms:
            sog = sog_series[sj][1]
            sj += 1
        dart.add(p.pitch, t, gy=p.gy, sog=sog, recompute=False)
        cand.add(p.pitch, t, sog=sog)
        cand_wide_nogate.add(p.pitch, t, sog=sog)
        dart_only_band.add(p.pitch, t, sog=sog)
    return series, conf, cand


def reference_series(catches, grid_times, window_s=24.0, stale_s=6.0):
    """Deux références sur la grille : cadence instantanée et cadence moyenne sur 24 s."""
    inst, win = {}, {}
    for tg in grid_times:
        i = bisect.bisect_right(catches, tg)
        if i >= 2 and tg - catches[i - 1] <= stale_s and catches[i - 1] - catches[i - 2] > 0:
            inst[tg] = 60.0 / (catches[i - 1] - catches[i - 2])
        else:
            inst[tg] = None
        j = bisect.bisect_right(catches, tg - window_s)
        w = catches[j:i]
        if len(w) >= 4 and tg - w[-1] <= stale_s:
            win[tg] = 60.0 * (len(w) - 1) / (w[-1] - w[0])
        else:
            win[tg] = None
    return inst, win


def match_strokes(detected, catches, tol_frac=0.4):
    """Appariement des instants détectés (pics de pitch) aux prises d'eau de référence.

    Le pic de pitch n'est pas la prise d'eau : on estime d'abord le décalage de phase
    médian, puis on compte les appariements dans ±tol_frac × cycle médian.
    """
    if len(detected) < 3 or len(catches) < 3:
        return None
    ci = sorted(catches)
    offs = []
    for d in detected:
        k = bisect.bisect_left(ci, d)
        near = [ci[x] for x in (k - 1, k) if 0 <= x < len(ci)]
        if near:
            offs.append(min((d - c for c in near), key=abs))
    off = statistics.median(offs)
    cyc = statistics.median(b - a for a, b in zip(ci, ci[1:]))
    tol = tol_frac * cyc
    used, hits = set(), 0
    for d in detected:
        k = bisect.bisect_left(ci, d - off)
        best = None
        for x in (k - 1, k):
            if 0 <= x < len(ci) and x not in used and abs(ci[x] + off - d) <= tol:
                if best is None or abs(ci[x] + off - d) < abs(ci[best] + off - d):
                    best = x
        if best is not None:
            used.add(best)
            hits += 1
    return {"phase_offset_s": off, "recall": hits / len(ci), "precision": hits / len(detected),
            "n_ref": len(ci), "n_detected": len(detected)}
