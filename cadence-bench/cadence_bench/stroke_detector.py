"""Détecteur coup par coup, candidat inspiré d'Open Rowing Monitor.

Reprend trois idées d'ORM (app/engine/Rower.js, RowingStatistics.js) :
  1. machine à états avec hystérésis : un coup n'est validé que si le signal a
     franchi un creux puis un pic (équivalent des durées minimales de phase) ;
  2. bornes de plausibilité sur la durée de cycle (min/max stroke time) ;
  3. cadence = 60 / médiane glissante des N dernières durées de cycle (N=6, comme
     `numOfPhasesForAveragingScreenData`).
Le signal d'entrée est le pitch filtré en passe-bande ; la bande est paramétrable
(celle de Data Row, 0,28–0,68 Hz, plafonne à ~41 spm).
"""
from __future__ import annotations

import math
import statistics
from collections import deque
from dataclasses import dataclass, field


@dataclass
class StrokeDetector:
    hp_hz: float = 0.25
    lp_hz: float = 1.2
    min_cycle_s: float = 1.2      # ~50 spm max
    max_cycle_s: float = 6.0      # ~10 spm min
    median_n: int = 6
    rms_window_s: float = 10.0
    floor_deg: float = 0.35       # même plancher que Data Row
    hyst_frac: float = 0.25       # repli minimal (fraction de l'amplitude) pour confirmer un pic
    min_sog: float | None = 1.1   # None = pas de portillon vitesse

    events: list = field(default_factory=list)   # (t_pic, t_confirmation)
    cycles: deque = field(default_factory=lambda: deque(maxlen=6))
    _hp_x = 0.0
    _hp_y = 0.0
    _lp_y = 0.0
    _init = False
    _last_t = 0.0
    _rms: deque = field(default_factory=deque)
    _state = "seek_trough"
    _peak_t = 0.0
    _peak_y = -1e9
    _trough_y = 1e9
    _sog: float | None = None
    _last_event_t: float | None = None

    def __post_init__(self):
        self.cycles = deque(maxlen=self.median_n)

    def _filter(self, x, t):
        if not self._init:
            self._init, self._hp_x, self._last_t = True, x, t
            return 0.0
        dt = t - self._last_t
        self._last_t = t
        if dt <= 0 or dt > 1.0:
            dt = 1 / 17.5
        rc = 1 / (2 * math.pi * self.hp_hz)
        hp = rc / (rc + dt) * (self._hp_y + x - self._hp_x)
        self._hp_x, self._hp_y = x, hp
        rc = 1 / (2 * math.pi * self.lp_hz)
        self._lp_y += dt / (rc + dt) * (hp - self._lp_y)
        return self._lp_y

    def _amp(self):
        if len(self._rms) < 10:
            return None
        return math.sqrt(sum(v * v for _, v in self._rms) / len(self._rms)) * math.sqrt(2)

    def add(self, pitch_deg, t_s, sog=None):
        if sog is not None:
            self._sog = sog
        y = self._filter(pitch_deg, t_s)
        self._rms.append((t_s, y))
        while self._rms and self._rms[0][0] < t_s - self.rms_window_s:
            self._rms.popleft()
        amp = self._amp()
        if amp is None:
            return
        thr = max(self.floor_deg, 0.5 * amp)
        hyst = max(self.floor_deg * 0.5, self.hyst_frac * amp)
        if self._state == "seek_trough":
            # Phase « Recovery » : on attend un creux franc (y < -thr) avant d'armer un pic.
            self._trough_y = min(self._trough_y, y)
            if self._trough_y <= -thr and y > self._trough_y + hyst:
                self._state, self._peak_y, self._peak_t = "seek_peak", y, t_s
        else:
            # Phase « Drive » : suivi du pic ; confirmé quand le signal retombe de `hyst`.
            if y > self._peak_y:
                self._peak_y, self._peak_t = y, t_s
            elif self._peak_y >= thr and y < self._peak_y - hyst:
                self._confirm(self._peak_t, t_s)
                self._state, self._trough_y, self._peak_y = "seek_trough", y, -1e9

    def _confirm(self, t_peak, t_now):
        if self._last_event_t is not None:
            cycle = t_peak - self._last_event_t
            if cycle < self.min_cycle_s:
                return                       # trop rapproché : ignoré (rebond)
            if cycle > self.max_cycle_s:
                self.cycles.clear()          # pause : on repart de zéro, comme ORM
            else:
                self.cycles.append(cycle)
        self._last_event_t = t_peak
        self.events.append((t_peak, t_now))

    def spm_median(self, t_now):
        """Cadence lissée (médiane des N derniers cycles), None si périmée/portillon fermé."""
        if self.min_sog is not None and (self._sog is None or self._sog < self.min_sog):
            return None
        if not self.cycles or self._last_event_t is None:
            return None
        if t_now - self._last_event_t > self.max_cycle_s:
            return None
        return 60.0 / statistics.median(self.cycles)

    def spm_last(self, t_now):
        """Cadence instantanée (dernier cycle), pour mesurer la réactivité."""
        if self.min_sog is not None and (self._sog is None or self._sog < self.min_sog):
            return None
        if not self.cycles or t_now - (self._last_event_t or -1e9) > self.max_cycle_s:
            return None
        return 60.0 / self.cycles[-1]
