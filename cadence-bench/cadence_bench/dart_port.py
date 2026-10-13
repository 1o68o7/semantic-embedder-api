"""Port fidèle de `apps/datar0w/lib/session/tel_cadence.dart` (TelCadenceDetector).

Référence : 1o68o7/AvSim-v1 @ f4e3bbb. Toute évolution du Dart doit être
répercutée ici (voir tests/test_dart_port.py, qui rejoue les tests Dart).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

HIGH, MEDIUM, LOW = "high", "medium", "low"


@dataclass
class Estimate:
    spm: float | None
    confidence: str
    src: str | None
    force: float | None = None
    spm_ac: float | None = None
    spm_peaks: float | None = None


_LOW = Estimate(None, LOW, None)


@dataclass
class _Sample:
    t: float
    raw: float
    y: float


def classify(force, sog, spm_ac, spm_peaks=None, high_force=0.35, medium_force=0.22,
             high_sog=1.6, medium_sog=1.1, max_spm_delta=5.0) -> Estimate:
    peaks_ok = spm_peaks is not None and abs(spm_ac - spm_peaks) < max_spm_delta
    if force >= high_force and sog >= high_sog and peaks_ok:
        return Estimate(spm_ac, HIGH, "imu_pitch_ac", force, spm_ac, spm_peaks)
    if force >= medium_force and sog >= medium_sog:
        return Estimate(spm_ac, MEDIUM, "imu_pitch_ac_approx", force, spm_ac, spm_peaks)
    return Estimate(None, LOW, None, force, spm_ac, spm_peaks)


def _index_near(times, t):
    best, best_d = 0, abs(times[0] - t)
    for i in range(1, len(times)):
        d = abs(times[i] - t)
        if d < best_d:
            best, best_d = i, d
    return best


def spm_from_peaks(times, signal, min_gap_s):
    if len(signal) < 8:
        return None
    mean = sum(signal) / len(signal)
    sigma = math.sqrt(sum((v - mean) ** 2 for v in signal) / len(signal))
    thr = max(0.35, 0.55 * sigma)
    peaks: list[float] = []
    for i in range(1, len(signal) - 1):
        y = signal[i]
        if y < thr:
            continue
        if y >= signal[i - 1] and y > signal[i + 1]:
            t = times[i]
            if not peaks or t - peaks[-1] >= min_gap_s:
                peaks.append(t)
            elif y > signal[_index_near(times, peaks[-1])]:
                peaks[-1] = t
    if len(peaks) < 3:
        return None
    gaps = sorted(b - a for a, b in zip(peaks, peaks[1:]))
    med = gaps[len(gaps) // 2]
    return 60.0 / med if med > 0 else None


def estimate_window(samples, sog, min_lag_s=1.45, max_lag_s=3.8, min_peak_gap_s=1.5,
                    high_force=0.35, medium_force=0.22, high_sog=1.6, medium_sog=1.1,
                    max_spm_delta=5.0) -> Estimate:
    if len(samples) < 40:
        return _LOW
    t0, t1 = samples[0].t, samples[-1].t
    dur = t1 - t0
    if dur < 8.0:
        return _LOW
    fs = (len(samples) - 1) / dur
    if fs < 2.5 or fs > 80:
        return _LOW
    ys = [s.y for s in samples]
    mean = sum(ys) / len(ys)
    x = [y - mean for y in ys]
    min_lag = max(1, math.floor(min_lag_s * fs))
    max_lag = min(len(x) // 2, math.ceil(max_lag_s * fs))
    if max_lag <= min_lag:
        return _LOW
    energy = sum(v * v for v in x)
    if energy < 1e-9:
        return _LOW
    best_lag, best_ac = min_lag, -1.0
    for lag in range(min_lag, max_lag + 1):
        num = 0.0
        for i in range(len(x) - lag):
            num += x[i] * x[i + lag]
        ac = num / energy
        if ac > best_ac:
            best_ac, best_lag = ac, lag
    spm_ac = 60.0 / (best_lag / fs)
    peaks = spm_from_peaks([s.t for s in samples], x, min_peak_gap_s)
    return classify(best_ac, sog if sog is not None else 0.0, spm_ac, peaks,
                    high_force, medium_force, high_sog, medium_sog, max_spm_delta)


@dataclass
class TelCadenceDetector:
    window_s: float = 24.0
    min_lag_s: float = 1.45
    max_lag_s: float = 3.8
    hp_hz: float = 0.28
    lp_hz: float = 0.68
    min_peak_gap_s: float = 1.5
    high_force: float = 0.35
    medium_force: float = 0.22
    high_sog: float = 1.6
    medium_sog: float = 1.1
    max_spm_delta: float = 5.0

    MIN_SAMPLE_GAP_S = 0.05

    spm: float | None = None
    confidence: str = LOW
    src: str | None = None
    _sog: float | None = None
    _buf: list = field(default_factory=list)
    _hp_y: float = 0.0
    _hp_x: float = 0.0
    _lp_y: float = 0.0
    _init: bool = False
    _last_ts: float = 0.0

    def add(self, pitch_deg, t_s, gy=None, sog=None, recompute=True):
        if sog is not None:
            self._sog = sog
        if self._buf and t_s - self._buf[-1].t < self.MIN_SAMPLE_GAP_S:
            return
        signal = pitch_deg
        if len(self._buf) >= 8 and gy is not None:
            n = min(16, len(self._buf))
            recent = [s.raw for s in self._buf[-n:]]
            if abs(max(recent) - min(recent)) < 0.4:
                signal = gy
        self._buf.append(_Sample(t_s, pitch_deg, self._bandpass(signal, t_s)))
        cut = t_s - self.window_s
        while self._buf and self._buf[0].t < cut:
            self._buf.pop(0)
        if recompute:
            self.recompute()

    def set_sog(self, sog):
        self._sog = sog

    def recompute(self) -> Estimate:
        est = estimate_window(self._buf, self._sog, self.min_lag_s, self.max_lag_s,
                              self.min_peak_gap_s, self.high_force, self.medium_force,
                              self.high_sog, self.medium_sog, self.max_spm_delta)
        self.spm, self.confidence, self.src = est.spm, est.confidence, est.src
        return est

    def _bandpass(self, x, t):
        if not self._init:
            self._init = True
            self._hp_x, self._hp_y, self._lp_y, self._last_ts = x, 0.0, 0.0, t
            return 0.0
        dt = t - self._last_ts
        self._last_ts = t
        if dt <= 0 or dt > 1.0:
            dt = 1.0 / 17.5
        rc_hp = 1.0 / (2 * math.pi * self.hp_hz)
        hp = rc_hp / (rc_hp + dt) * (self._hp_y + x - self._hp_x)
        self._hp_x, self._hp_y = x, hp
        rc_lp = 1.0 / (2 * math.pi * self.lp_hz)
        self._lp_y += dt / (rc_lp + dt) * (hp - self._lp_y)
        return self._lp_y
