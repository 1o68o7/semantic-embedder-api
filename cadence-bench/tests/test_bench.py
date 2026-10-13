"""Tests du banc : vérité connue synthétique, chargeurs, métriques."""
import json
import tempfile
import unittest
from pathlib import Path

from cadence_bench import loaders, metrics, report, synth
from cadence_bench.runner import match_strokes, reference_series


class Bench(unittest.TestCase):
    def test_steady_scenario_is_accurate_for_both(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = synth.write_session(tmp, "steady22")
            res = report.evaluate(d, ref=str(d / "strokes.jsonl"))
        for name in ("dart_ac", "stroke_median6"):
            m = res["algos"][name]["vs_window24"]
            self.assertGreater(m["coverage"], 0.9, name)
            self.assertLess(m["mae"], 1.0, name)

    def test_reference_series(self):
        catches = [i * 2.0 for i in range(40)]  # 30 spm
        inst, win = reference_series(catches, [50.0])
        self.assertAlmostEqual(inst[50.0], 30.0)
        self.assertAlmostEqual(win[50.0], 30.0)

    def test_reference_stale(self):
        inst, win = reference_series([0, 2, 4, 6, 8], [100.0])
        self.assertIsNone(inst[100.0])
        self.assertIsNone(win[100.0])

    def test_loader_picks_one_slot_and_skips_details(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "strokes.jsonl"
            rows = [{"t": 1000 * i, "slot": "1B"} for i in range(5)] \
                + [{"t": 1000 * i + 3, "slot": "1T"} for i in range(5)] \
                + [{"kind": "detail", "t": 5}]
            p.write_text("\n".join(json.dumps(r) for r in rows))
            times, _ = loaders.load_reference_catches(p)
            self.assertEqual(len(times), 5)
            times_t, _ = loaders.load_reference_catches(p, slot="1T")
            self.assertAlmostEqual(times_t[0], 0.003)

    def test_loader_csv_ms_and_s(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "c.csv"
            p.write_text("t\n1791000000000\n1791000002000\n")
            times, _ = loaders.load_reference_catches(p)
            self.assertEqual(times, [1791000000.0, 1791000002.0])

    def test_best_lag_needs_variation(self):
        flat = {float(i): 22.0 for i in range(100)}
        self.assertIsNone(metrics.best_lag(flat, flat))
        ramp = {float(i): 18.0 + i * 0.2 for i in range(100)}
        delayed = {float(i): 18.0 + (i - 5) * 0.2 for i in range(100)}
        lag, _, _ = metrics.best_lag(delayed, ramp)
        self.assertEqual(lag, 5)

    def test_match_strokes_perfect(self):
        c = [i * 2.0 for i in range(30)]
        m = match_strokes([x + 0.7 for x in c], c)
        self.assertAlmostEqual(m["recall"], 1.0)
        self.assertAlmostEqual(m["precision"], 1.0)


if __name__ == "__main__":
    unittest.main()
