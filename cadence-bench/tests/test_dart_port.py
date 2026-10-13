"""Conformité du port Python avec apps/datar0w/test/imu_cadence_test.dart (AvSim-v1 @ f4e3bbb).

Chaque test rejoue un test Dart ; si l'un échoue, le port a divergé du code de l'app.
"""
import math
import unittest

from cadence_bench.dart_port import HIGH, LOW, MEDIUM, TelCadenceDetector, classify

T0 = 1_791_000_000.0


def feed_sinus(d, period_s, sog, duration_s=28, amp_deg=4.0, fs=17.5):
    n = round(duration_s * fs)
    for i in range(n):
        t = T0 + round(i * 1000 / fs) / 1000.0
        d.add(pitch_deg=amp_deg * math.sin(2 * math.pi * (i / fs) / period_s), t_s=t, gy=0, sog=sog)


class DartConformance(unittest.TestCase):
    def test_sinus_high(self):
        d = TelCadenceDetector()
        feed_sinus(d, 2.05, 3.0)
        self.assertEqual(d.confidence, HIGH)
        self.assertAlmostEqual(d.spm, 60 / 2.05, delta=1.0)
        self.assertEqual(d.src, "imu_pitch_ac")

    def test_200hz_delivery(self):
        d = TelCadenceDetector()
        feed_sinus(d, 2.05, 3.0, fs=200)
        self.assertIsNotNone(d.spm)
        self.assertAlmostEqual(d.spm, 60 / 2.05, delta=1.5)

    def test_bursts(self):
        d = TelCadenceDetector()
        for i in range(28 * 17):
            burst = i // 5
            t = T0 + round(burst * 5 * 1000 / 17) / 1000.0
            d.add(pitch_deg=4 * math.sin(2 * math.pi * (i / 17) / 2.05), t_s=t, gy=0, sog=3.0)
        self.assertIsNotNone(d.spm)

    def test_low_sog(self):
        d = TelCadenceDetector()
        feed_sinus(d, 2.05, 0.4)
        self.assertEqual(d.confidence, LOW)
        self.assertIsNone(d.spm)
        self.assertIsNone(d.src)

    def test_divergent_estimators_not_high(self):
        e = classify(force=0.5, sog=3.0, spm_ac=30, spm_peaks=22)
        self.assertEqual(e.confidence, MEDIUM)
        self.assertEqual(e.src, "imu_pitch_ac_approx")

    def test_no_peaks_medium(self):
        e = classify(force=0.5, sog=3.0, spm_ac=30, spm_peaks=None)
        self.assertEqual(e.confidence, MEDIUM)
        self.assertEqual(e.spm, 30)

    def test_peaks_unreachable_medium(self):
        d = TelCadenceDetector(min_peak_gap_s=20)
        feed_sinus(d, 2.05, 3.0)
        self.assertEqual(d.confidence, MEDIUM)

    def test_short_fixture_range(self):
        d = TelCadenceDetector()
        feed_sinus(d, 2.05, 3.0, duration_s=28)
        self.assertEqual(d.confidence, HIGH)
        self.assertTrue(28.0 <= d.spm <= 31.0)

    def test_gczekf_like(self):
        d = TelCadenceDetector()
        feed_sinus(d, 60 / 29.2, 2.8, duration_s=40, amp_deg=5)
        self.assertEqual(d.confidence, HIGH)
        self.assertTrue(28.0 <= d.spm <= 31.0)


if __name__ == "__main__":
    unittest.main()
