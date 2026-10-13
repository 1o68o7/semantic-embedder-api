# Banc d'essai cadence — synthétique « steady22 »

IMU : 4200 points · samples : 240 · référence : strokes.jsonl slot=1B seat=None (87 coups)

## Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 100 % | 0.13 | 0.03 | 0.17 | 0.29 | 100 % | 100 % | — |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 0.26 | 0.07 | 0.32 | 0.49 | 100 % | 100 % | — |
| Coup par coup, dernier cycle (bande large) | 100 % | 0.84 | 0.03 | 1.07 | 1.68 | 66 % | 93 % | — |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 0.26 | 0.07 | 0.32 | 0.49 | 100 % | 100 % | — |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.20 | 0.06 | 0.26 | 0.46 | 100 % | 100 % | — |

## Référence = cadence du dernier cycle (mesure la réactivité)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 99 % | 0.43 | 0.02 | 0.54 | 0.96 | 92 % | 100 % | — |
| Coup par coup, médiane 6 cycles (bande large) | 99 % | 0.49 | 0.07 | 0.61 | 1.06 | 90 % | 100 % | — |
| Coup par coup, dernier cycle (bande large) | 99 % | 0.85 | 0.03 | 1.10 | 1.65 | 69 % | 92 % | — |
| Coup par coup, médiane 6, sans portillon vitesse | 99 % | 0.49 | 0.07 | 0.61 | 1.06 | 90 % | 100 % | — |
| Coup par coup, médiane 6, bande Data Row | 99 % | 0.44 | 0.06 | 0.55 | 0.91 | 93 % | 100 % | — |

## MAE par régime (réf. 24 s)

| Régime | Data Row actuel (autocorr. 24 s) | Coup par coup, médiane 6 cycles (bande large) | Coup par coup, dernier cycle (bande large) | Coup par coup, médiane 6, sans portillon vitesse | Coup par coup, médiane 6, bande Data Row |
|---|---|---|---|---|---|
| ref <20 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 20-26 spm | 0.13 (n=229) | 0.26 (n=229) | 0.84 (n=229) | 0.26 (n=229) | 0.20 (n=229) |
| ref 26-32 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 32-38 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref >=38 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| stable (|Δref 10 s| < 3) | 0.13 (n=219) | 0.26 (n=219) | 0.84 (n=219) | 0.26 (n=219) | 0.20 (n=219) |
| transition (|Δref 10 s| ≥ 3) | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |

Confiance Data Row : high 97 % · medium 0 % · low 3 %

Détection de coups (candidat) : rappel 99 %, précision 99 % (87 détectés / 87 réf., décalage pic de pitch → prise d'eau -1.20 s, défini à un cycle près)


---

# Banc d'essai cadence — synthétique « low16 »

IMU : 4200 points · samples : 240 · référence : strokes.jsonl slot=1B seat=None (64 coups)

## Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 100 % | 0.09 | 0.06 | 0.11 | 0.18 | 100 % | 100 % | — |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 0.19 | -0.07 | 0.24 | 0.40 | 100 % | 100 % | — |
| Coup par coup, dernier cycle (bande large) | 100 % | 1.11 | 0.36 | 2.83 | 1.15 | 81 % | 92 % | — |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 0.19 | -0.07 | 0.24 | 0.40 | 100 % | 100 % | — |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.17 | -0.06 | 0.22 | 0.38 | 100 % | 100 % | — |

## Référence = cadence du dernier cycle (mesure la réactivité)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 100 % | 0.24 | 0.05 | 0.30 | 0.49 | 100 % | 100 % | — |
| Coup par coup, médiane 6 cycles (bande large) | 99 % | 0.33 | -0.08 | 0.42 | 0.65 | 99 % | 100 % | — |
| Coup par coup, dernier cycle (bande large) | 99 % | 1.09 | 0.35 | 2.78 | 1.52 | 80 % | 92 % | — |
| Coup par coup, médiane 6, sans portillon vitesse | 99 % | 0.33 | -0.08 | 0.42 | 0.65 | 99 % | 100 % | — |
| Coup par coup, médiane 6, bande Data Row | 99 % | 0.32 | -0.08 | 0.39 | 0.65 | 100 % | 100 % | — |

## MAE par régime (réf. 24 s)

| Régime | Data Row actuel (autocorr. 24 s) | Coup par coup, médiane 6 cycles (bande large) | Coup par coup, dernier cycle (bande large) | Coup par coup, médiane 6, sans portillon vitesse | Coup par coup, médiane 6, bande Data Row |
|---|---|---|---|---|---|
| ref <20 spm | 0.09 (n=225) | 0.19 (n=225) | 1.11 (n=225) | 0.19 (n=225) | 0.17 (n=225) |
| ref 20-26 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 26-32 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 32-38 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref >=38 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| stable (|Δref 10 s| < 3) | 0.09 (n=215) | 0.18 (n=215) | 1.12 (n=215) | 0.18 (n=215) | 0.16 (n=215) |
| transition (|Δref 10 s| ≥ 3) | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |

Confiance Data Row : high 96 % · medium 0 % · low 3 %

Détection de coups (candidat) : rappel 97 %, précision 98 % (63 détectés / 64 réf., décalage pic de pitch → prise d'eau -1.60 s, défini à un cycle près)


---

# Banc d'essai cadence — synthétique « step20_32 »

IMU : 4200 points · samples : 240 · référence : strokes.jsonl slot=1B seat=None (104 coups)

## Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 100 % | 0.68 | -0.31 | 2.07 | 0.61 | 93 % | 95 % | +5 s (MAE 0.63) |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 0.59 | 0.36 | 1.25 | 1.06 | 90 % | 94 % | -5 s (MAE 0.51) |
| Coup par coup, dernier cycle (bande large) | 100 % | 1.30 | 0.58 | 2.23 | 2.41 | 64 % | 83 % | -9 s (MAE 1.00) |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 0.59 | 0.36 | 1.25 | 1.06 | 90 % | 94 % | -5 s (MAE 0.51) |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.56 | 0.31 | 1.25 | 0.93 | 91 % | 94 % | -5 s (MAE 0.47) |

## Référence = cadence du dernier cycle (mesure la réactivité)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 99 % | 1.45 | -0.86 | 3.70 | 1.55 | 80 % | 93 % | +16 s (MAE 0.60) |
| Coup par coup, médiane 6 cycles (bande large) | 99 % | 0.78 | -0.20 | 1.66 | 1.40 | 82 % | 97 % | +5 s (MAE 0.50) |
| Coup par coup, dernier cycle (bande large) | 99 % | 0.85 | 0.01 | 1.16 | 1.96 | 64 % | 91 % | +1 s (MAE 0.84) |
| Coup par coup, médiane 6, sans portillon vitesse | 99 % | 0.78 | -0.20 | 1.66 | 1.40 | 82 % | 97 % | +5 s (MAE 0.50) |
| Coup par coup, médiane 6, bande Data Row | 99 % | 0.74 | -0.23 | 1.69 | 1.41 | 86 % | 96 % | +5 s (MAE 0.48) |

## MAE par régime (réf. 24 s)

| Régime | Data Row actuel (autocorr. 24 s) | Coup par coup, médiane 6 cycles (bande large) | Coup par coup, dernier cycle (bande large) | Coup par coup, médiane 6, sans portillon vitesse | Coup par coup, médiane 6, bande Data Row |
|---|---|---|---|---|---|
| ref <20 spm | 0.14 (n=55) | 0.21 (n=55) | 0.71 (n=55) | 0.21 (n=55) | 0.15 (n=55) |
| ref 20-26 spm | 0.66 (n=64) | 0.70 (n=64) | 1.87 (n=64) | 0.70 (n=64) | 0.70 (n=64) |
| ref 26-32 spm | 1.25 (n=81) | 0.83 (n=81) | 1.40 (n=81) | 0.83 (n=81) | 0.82 (n=81) |
| ref 32-38 spm | 0.14 (n=27) | 0.41 (n=27) | 0.80 (n=27) | 0.41 (n=27) | 0.29 (n=27) |
| ref >=38 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| stable (|Δref 10 s| < 3) | 0.26 (n=195) | 0.33 (n=195) | 1.03 (n=195) | 0.33 (n=195) | 0.30 (n=195) |
| transition (|Δref 10 s| ≥ 3) | 4.69 (n=22) | 3.04 (n=22) | 3.98 (n=22) | 3.04 (n=22) | 3.02 (n=22) |

Confiance Data Row : high 93 % · medium 4 % · low 3 %

Détection de coups (candidat) : rappel 98 %, précision 99 % (103 détectés / 104 réf., décalage pic de pitch → prise d'eau -0.86 s, défini à un cycle près)

## Temps d'établissement après le saut de cadence (±1,5 spm tenu 5 s)

| Algo | Établissement |
|---|---|
| Data Row actuel (autocorr. 24 s) | 18 s |
| Coup par coup, médiane 6 cycles (bande large) | 9 s |
| Coup par coup, dernier cycle (bande large) | 3 s |
| Coup par coup, médiane 6, sans portillon vitesse | 9 s |
| Coup par coup, médiane 6, bande Data Row | 9 s |


---

# Banc d'essai cadence — synthétique « ramp18_36 »

IMU : 5250 points · samples : 300 · référence : strokes.jsonl slot=1B seat=None (135 coups)

## Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 100 % | 0.20 | 0.07 | 0.25 | 0.41 | 100 % | 100 % | -1 s (MAE 0.20) |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 0.37 | 0.25 | 0.48 | 0.83 | 95 % | 100 % | -4 s (MAE 0.32) |
| Coup par coup, dernier cycle (bande large) | 100 % | 1.13 | 0.60 | 1.61 | 2.46 | 54 % | 86 % | -10 s (MAE 0.99) |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 0.37 | 0.25 | 0.48 | 0.83 | 95 % | 100 % | -4 s (MAE 0.32) |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.30 | 0.20 | 0.40 | 0.65 | 97 % | 100 % | -3 s (MAE 0.27) |

## Référence = cadence du dernier cycle (mesure la réactivité)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 99 % | 0.67 | -0.50 | 0.81 | 1.27 | 75 % | 99 % | +8 s (MAE 0.50) |
| Coup par coup, médiane 6 cycles (bande large) | 99 % | 0.60 | -0.33 | 0.77 | 1.23 | 80 % | 99 % | +5 s (MAE 0.52) |
| Coup par coup, dernier cycle (bande large) | 99 % | 1.02 | 0.02 | 1.47 | 2.23 | 59 % | 87 % | +0 s (MAE 1.02) |
| Coup par coup, médiane 6, sans portillon vitesse | 99 % | 0.60 | -0.33 | 0.77 | 1.23 | 80 % | 99 % | +5 s (MAE 0.52) |
| Coup par coup, médiane 6, bande Data Row | 99 % | 0.58 | -0.37 | 0.74 | 1.21 | 81 % | 99 % | +6 s (MAE 0.46) |

## MAE par régime (réf. 24 s)

| Régime | Data Row actuel (autocorr. 24 s) | Coup par coup, médiane 6 cycles (bande large) | Coup par coup, dernier cycle (bande large) | Coup par coup, médiane 6, sans portillon vitesse | Coup par coup, médiane 6, bande Data Row |
|---|---|---|---|---|---|
| ref <20 spm | 0.14 (n=31) | 0.18 (n=31) | 0.61 (n=31) | 0.18 (n=31) | 0.13 (n=31) |
| ref 20-26 spm | 0.13 (n=103) | 0.29 (n=103) | 0.83 (n=103) | 0.29 (n=103) | 0.23 (n=103) |
| ref 26-32 spm | 0.23 (n=101) | 0.47 (n=101) | 1.47 (n=101) | 0.47 (n=101) | 0.40 (n=101) |
| ref 32-38 spm | 0.32 (n=52) | 0.46 (n=52) | 1.37 (n=52) | 0.46 (n=52) | 0.36 (n=52) |
| ref >=38 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| stable (|Δref 10 s| < 3) | 0.20 (n=277) | 0.38 (n=277) | 1.16 (n=277) | 0.38 (n=277) | 0.31 (n=277) |
| transition (|Δref 10 s| ≥ 3) | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |

Confiance Data Row : high 97 % · medium 0 % · low 3 %

Détection de coups (candidat) : rappel 99 %, précision 100 % (134 détectés / 135 réf., décalage pic de pitch → prise d'eau -0.91 s, défini à un cycle près)


---

# Banc d'essai cadence — synthétique « start_sequence »

IMU : 3150 points · samples : 180 · référence : strokes.jsonl slot=1B seat=None (98 coups)

## Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 98 % | 0.51 | -0.17 | 0.80 | 0.93 | 90 % | 94 % | +0 s (MAE 0.51) |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 0.66 | -0.48 | 1.09 | 1.89 | 80 % | 92 % | -5 s (MAE 0.46) |
| Coup par coup, dernier cycle (bande large) | 100 % | 1.62 | -0.83 | 2.27 | 3.59 | 52 % | 73 % | -9 s (MAE 1.26) |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 0.66 | -0.48 | 1.09 | 1.89 | 80 % | 92 % | -5 s (MAE 0.46) |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.66 | -0.36 | 1.02 | 1.79 | 80 % | 93 % | -4 s (MAE 0.49) |

## Référence = cadence du dernier cycle (mesure la réactivité)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 97 % | 1.28 | 0.65 | 1.91 | 3.42 | 58 % | 81 % | +13 s (MAE 0.95) |
| Coup par coup, médiane 6 cycles (bande large) | 98 % | 0.84 | 0.32 | 1.40 | 2.08 | 77 % | 90 % | +5 s (MAE 0.63) |
| Coup par coup, dernier cycle (bande large) | 98 % | 1.20 | -0.02 | 1.67 | 2.68 | 59 % | 83 % | -1 s (MAE 1.14) |
| Coup par coup, médiane 6, sans portillon vitesse | 99 % | 0.84 | 0.33 | 1.40 | 2.08 | 77 % | 90 % | +5 s (MAE 0.63) |
| Coup par coup, médiane 6, bande Data Row | 98 % | 0.90 | 0.45 | 1.45 | 1.97 | 75 % | 90 % | +5 s (MAE 0.65) |

## MAE par régime (réf. 24 s)

| Régime | Data Row actuel (autocorr. 24 s) | Coup par coup, médiane 6 cycles (bande large) | Coup par coup, dernier cycle (bande large) | Coup par coup, médiane 6, sans portillon vitesse | Coup par coup, médiane 6, bande Data Row |
|---|---|---|---|---|---|
| ref <20 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 20-26 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 26-32 spm | 0.32 (n=108) | 0.31 (n=108) | 0.98 (n=108) | 0.31 (n=108) | 0.36 (n=108) |
| ref 32-38 spm | 0.34 (n=33) | 1.13 (n=33) | 2.40 (n=33) | 1.13 (n=33) | 1.05 (n=33) |
| ref >=38 spm | 1.39 (n=30) | 1.35 (n=33) | 2.96 (n=33) | 1.35 (n=33) | 1.23 (n=33) |
| stable (|Δref 10 s| < 3) | 0.42 (n=152) | 0.53 (n=152) | 1.45 (n=152) | 0.53 (n=152) | 0.53 (n=152) |
| transition (|Δref 10 s| ≥ 3) | 0.36 (n=12) | 2.45 (n=12) | 3.94 (n=12) | 2.45 (n=12) | 2.18 (n=12) |

Confiance Data Row : high 79 % · medium 16 % · low 4 %

Détection de coups (candidat) : rappel 99 %, précision 100 % (97 détectés / 98 réf., décalage pic de pitch → prise d'eau -0.85 s, défini à un cycle près)


---

# Banc d'essai cadence — synthétique « sprint40 »

IMU : 4200 points · samples : 240 · référence : strokes.jsonl slot=1B seat=None (136 coups)

## Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 100 % | 0.30 | -0.07 | 0.47 | 0.57 | 95 % | 99 % | +0 s (MAE 0.30) |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 0.55 | 0.27 | 1.26 | 0.82 | 91 % | 95 % | -5 s (MAE 0.51) |
| Coup par coup, dernier cycle (bande large) | 100 % | 1.53 | 0.40 | 2.54 | 3.44 | 47 % | 82 % | -9 s (MAE 1.35) |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 0.55 | 0.27 | 1.26 | 0.82 | 91 % | 95 % | -5 s (MAE 0.51) |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.57 | 0.34 | 1.34 | 0.85 | 91 % | 94 % | -6 s (MAE 0.49) |

## Référence = cadence du dernier cycle (mesure la réactivité)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 98 % | 1.16 | -0.60 | 2.25 | 1.92 | 70 % | 90 % | +8 s (MAE 0.82) |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 0.89 | -0.22 | 1.64 | 1.56 | 70 % | 96 % | +4 s (MAE 0.72) |
| Coup par coup, dernier cycle (bande large) | 100 % | 1.33 | -0.10 | 2.36 | 2.88 | 50 % | 81 % | +1 s (MAE 1.21) |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 0.89 | -0.22 | 1.64 | 1.56 | 70 % | 96 % | +4 s (MAE 0.72) |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.83 | -0.17 | 1.56 | 1.58 | 70 % | 96 % | +4 s (MAE 0.67) |

## MAE par régime (réf. 24 s)

| Régime | Data Row actuel (autocorr. 24 s) | Coup par coup, médiane 6 cycles (bande large) | Coup par coup, dernier cycle (bande large) | Coup par coup, médiane 6, sans portillon vitesse | Coup par coup, médiane 6, bande Data Row |
|---|---|---|---|---|---|
| ref <20 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 20-26 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 26-32 spm | 0.24 (n=120) | 0.40 (n=120) | 1.25 (n=120) | 0.40 (n=120) | 0.40 (n=120) |
| ref 32-38 spm | 1.18 (n=11) | 4.23 (n=11) | 6.02 (n=11) | 4.23 (n=11) | 4.47 (n=11) |
| ref >=38 spm | 0.28 (n=100) | 0.32 (n=100) | 1.36 (n=100) | 0.32 (n=100) | 0.33 (n=100) |
| stable (|Δref 10 s| < 3) | 0.23 (n=200) | 0.29 (n=200) | 1.29 (n=200) | 0.29 (n=200) | 0.29 (n=200) |
| transition (|Δref 10 s| ≥ 3) | 0.93 (n=21) | 3.00 (n=21) | 4.17 (n=21) | 3.00 (n=21) | 3.31 (n=21) |

Confiance Data Row : high 51 % · medium 46 % · low 3 %

Détection de coups (candidat) : rappel 99 %, précision 100 % (134 détectés / 136 réf., décalage pic de pitch → prise d'eau -0.69 s, défini à un cycle près)

## Temps d'établissement après le saut de cadence (±1,5 spm tenu 5 s)

| Algo | Établissement |
|---|---|
| Data Row actuel (autocorr. 24 s) | 18 s |
| Coup par coup, médiane 6 cycles (bande large) | 9 s |
| Coup par coup, dernier cycle (bande large) | 15 s |
| Coup par coup, médiane 6, sans portillon vitesse | 9 s |
| Coup par coup, médiane 6, bande Data Row | 7 s |
