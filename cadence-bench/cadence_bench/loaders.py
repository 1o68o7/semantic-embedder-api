"""Lecture des fichiers de séance Data Row et des références."""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImuPoint:
    t_ms: int
    pitch: float
    gy: float | None


def _jsonl(path):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                yield obj


def load_imu(path) -> list[ImuPoint]:
    """imu.jsonl : {"t": ms, "pitch_raw": deg, "gy": deg/s, ...} (cf. CadenceBackfill.loadImuPoints)."""
    out = []
    for m in _jsonl(path):
        t, p = m.get("t"), m.get("pitch_raw")
        if isinstance(t, (int, float)) and isinstance(p, (int, float)):
            gy = m.get("gy")
            out.append(ImuPoint(int(t), float(p), float(gy) if isinstance(gy, (int, float)) else None))
    return out


def load_sog(path) -> list[tuple[int, float | None]]:
    """samples.jsonl (1 Hz) -> [(t_ms, sog m/s)]."""
    out = []
    for m in _jsonl(path):
        t = m.get("t")
        if isinstance(t, (int, float)):
            s = m.get("sog")
            out.append((int(t), float(s) if isinstance(s, (int, float)) else None))
    return out


def load_app_cadence(path) -> list[tuple[int, float | None, str | None]]:
    """Cadence déjà calculée par l'app (champs cadence_spm / cadence_src de samples.jsonl)."""
    out = []
    for m in _jsonl(path):
        t = m.get("t")
        if isinstance(t, (int, float)):
            c = m.get("cadence_spm")
            out.append((int(t), float(c) if isinstance(c, (int, float)) else None, m.get("cadence_src")))
    return out


def load_reference_catches(path, slot: str | None = None, seat: int | None = None) -> tuple[list[float], str]:
    """Instants de prise d'eau de référence, en secondes (époque UTC).

    Formats acceptés :
      * strokes.jsonl du stroke sensor (champ `t` en ms ; lignes `kind: detail` ignorées).
        Plusieurs capteurs par siège (B/T) : on filtre sur `slot`/`seat`, sinon on garde
        le premier `slot` rencontré.
      * .csv / .txt : une colonne `t` (ms UTC), ou t_s (secondes), avec ou sans en-tête.
    Retourne (liste triée, description de ce qui a été retenu).
    """
    p = Path(path)
    if p.suffix.lower() in (".csv", ".txt"):
        vals = []
        with open(p, encoding="utf-8") as fh:
            for row in csv.reader(fh):
                if not row:
                    continue
                try:
                    vals.append(float(row[0]))
                except ValueError:
                    continue
        # ms si > 1e11, sinon secondes
        sec = [v / 1000.0 if v > 1e11 else v for v in vals]
        return sorted(sec), f"{p.name} ({len(sec)} instants)"
    rows = [m for m in _jsonl(p) if m.get("kind") != "detail" and isinstance(m.get("t"), (int, float))]
    if seat is not None:
        rows = [m for m in rows if m.get("seat") == seat]
    if slot is None:
        slot = next((m.get("slot") for m in rows if m.get("slot")), None)
    if slot is not None:
        rows = [m for m in rows if m.get("slot") == slot]
    times = sorted(m["t"] / 1000.0 for m in rows)
    return times, f"{p.name} slot={slot} seat={seat} ({len(times)} coups)"
