"""Générateur de séances synthétiques à vérité connue (prises d'eau exactes).

SYNTHÉTIQUE : sert à valider le banc et à caractériser les limites des algos
(plage, latence, bruit). Ne remplace pas une validation sur séances réelles.
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

SCENARIOS = {
    # nom: (durée s, f(t) -> spm cible)
    "steady22": (240, lambda t: 22.0),
    "low16": (240, lambda t: 16.0),
    "step20_32": (240, lambda t: 20.0 if t < 120 else 32.0),
    "ramp18_36": (300, lambda t: 18.0 + 18.0 * min(1.0, t / 300.0)),
    "start_sequence": (180, lambda t: 44.0 if t < 15 else (40.0 if t < 30 else (34.0 if t < 60 else 30.0))),
    "sprint40": (240, lambda t: 28.0 if t < 120 else 40.0),
}


T0_S = 1_790_000_000.0
# Instant du saut de cadence (s depuis le début) pour la mesure du temps d'établissement.
STEPS = {"step20_32": 120, "sprint40": 120}


def generate(name, seed=0, fs=17.5, noise_deg=0.8, spikes_per_min=0.5, sog=3.2,
             burst=False, amp_deg=4.0):
    dur, rate_fn = SCENARIOS[name]
    rng = random.Random(seed)
    t0_ms = 1_790_000_000_000
    phase, t = 0.0, 0.0
    catches = []
    imu, samples = [], []
    drift_ph = rng.uniform(0, 6.28)
    stroke_factor = 1.0
    n = int(dur * fs)
    for i in range(n):
        t = i / fs + rng.uniform(-0.004, 0.004)
        spm = rate_fn(t) * stroke_factor
        prev = phase
        phase += (spm / 60.0) / fs
        if int(phase) > int(prev):
            catches.append(t0_ms / 1000.0 + t)
            stroke_factor = 1.0 + rng.gauss(0, 0.02)       # variation coup à coup
        ph = phase % 1.0
        wave = -math.cos(2 * math.pi * ph) + 0.35 * math.sin(4 * math.pi * ph + 0.6)
        pitch = amp_deg * wave + 1.0 * math.sin(2 * math.pi * 0.1 * t + drift_ph) \
            + rng.gauss(0, noise_deg) - 60.0                 # pitch moyen proche de -60° (téléphone incliné)
        if rng.random() < spikes_per_min / 60.0 / fs:
            pitch += rng.choice((-1, 1)) * rng.uniform(8, 15)
        ts = t0_ms + int(round(t * 1000))
        if burst:
            ts = t0_ms + int(round((i // 5) * 5 * 1000 / fs))
        imu.append({"t": ts, "ax": 0, "ay": 0, "az": 9.8, "gx": 0, "gy": 0, "gz": 0,
                    "roll_raw": 0, "pitch_raw": round(pitch, 4)})
    for s in range(int(dur)):
        v = 0.0 if s < 5 else sog
        samples.append({"t": t0_ms + s * 1000, "sog": v, "cadence_spm": None, "cadence_src": None})
    strokes = [{"seq": k, "t": int(round(c * 1000)), "slot": "1B", "seat": 1} for k, c in enumerate(catches)]
    return imu, samples, strokes


def write_session(out_dir, name, **kw):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    imu, samples, strokes = generate(name, **kw)
    for fname, rows in (("imu.jsonl", imu), ("samples.jsonl", samples), ("strokes.jsonl", strokes)):
        with open(out / fname, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r) + "\n")
    return out
