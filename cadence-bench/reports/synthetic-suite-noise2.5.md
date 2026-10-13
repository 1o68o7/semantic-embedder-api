# Banc d'essai cadence — synthétique « steady22 »

IMU : 4200 points · samples : 240 · référence : strokes.jsonl slot=1B seat=None (87 coups)

## Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 100 % | 0.17 | 0.09 | 0.23 | 0.39 | 100 % | 100 % | — |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 1.04 | 0.39 | 1.28 | 2.37 | 55 % | 88 % | — |
| Coup par coup, dernier cycle (bande large) | 100 % | 3.10 | 0.95 | 4.03 | 5.85 | 27 % | 41 % | — |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 1.04 | 0.39 | 1.28 | 2.37 | 55 % | 88 % | — |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.59 | -0.06 | 0.71 | 1.25 | 86 % | 100 % | — |

## Référence = cadence du dernier cycle (mesure la réactivité)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 99 % | 0.46 | 0.08 | 0.56 | 0.96 | 90 % | 100 % | — |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 1.20 | 0.32 | 1.46 | 2.50 | 50 % | 81 % | — |
| Coup par coup, dernier cycle (bande large) | 100 % | 3.12 | 0.87 | 4.04 | 5.94 | 24 % | 39 % | — |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 1.20 | 0.32 | 1.46 | 2.50 | 50 % | 81 % | — |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.81 | 0.01 | 1.15 | 1.58 | 71 % | 98 % | — |

## MAE par régime (réf. 24 s)

| Régime | Data Row actuel (autocorr. 24 s) | Coup par coup, médiane 6 cycles (bande large) | Coup par coup, dernier cycle (bande large) | Coup par coup, médiane 6, sans portillon vitesse | Coup par coup, médiane 6, bande Data Row |
|---|---|---|---|---|---|
| ref <20 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 20-26 spm | 0.17 (n=229) | 1.04 (n=229) | 3.10 (n=229) | 1.04 (n=229) | 0.59 (n=229) |
| ref 26-32 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 32-38 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref >=38 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| stable (|Δref 10 s| < 3) | 0.17 (n=219) | 1.01 (n=219) | 3.13 (n=219) | 1.01 (n=219) | 0.58 (n=219) |
| transition (|Δref 10 s| ≥ 3) | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |

Confiance Data Row : high 97 % · medium 0 % · low 3 %

Détection de coups (candidat) : rappel 100 %, précision 100 % (87 détectés / 87 réf., décalage pic de pitch → prise d'eau +0.86 s, défini à un cycle près)


---

# Banc d'essai cadence — synthétique « low16 »

IMU : 4200 points · samples : 240 · référence : strokes.jsonl slot=1B seat=None (64 coups)

## Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 100 % | 0.13 | 0.06 | 0.17 | 0.28 | 100 % | 100 % | — |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 0.74 | 0.48 | 1.04 | 1.42 | 80 % | 93 % | — |
| Coup par coup, dernier cycle (bande large) | 100 % | 2.69 | 1.23 | 4.58 | 4.89 | 34 % | 53 % | — |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 0.74 | 0.48 | 1.04 | 1.42 | 80 % | 93 % | — |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.65 | -0.03 | 0.82 | 1.66 | 84 % | 100 % | — |

## Référence = cadence du dernier cycle (mesure la réactivité)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 100 % | 0.25 | 0.05 | 0.31 | 0.53 | 100 % | 100 % | — |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 0.79 | 0.46 | 1.09 | 1.56 | 70 % | 93 % | — |
| Coup par coup, dernier cycle (bande large) | 100 % | 2.68 | 1.18 | 4.56 | 4.73 | 32 % | 54 % | — |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 0.79 | 0.46 | 1.09 | 1.56 | 70 % | 93 % | — |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.72 | -0.06 | 0.90 | 1.59 | 76 % | 98 % | — |

## MAE par régime (réf. 24 s)

| Régime | Data Row actuel (autocorr. 24 s) | Coup par coup, médiane 6 cycles (bande large) | Coup par coup, dernier cycle (bande large) | Coup par coup, médiane 6, sans portillon vitesse | Coup par coup, médiane 6, bande Data Row |
|---|---|---|---|---|---|
| ref <20 spm | 0.13 (n=225) | 0.74 (n=225) | 2.69 (n=225) | 0.74 (n=225) | 0.65 (n=225) |
| ref 20-26 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 26-32 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 32-38 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref >=38 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| stable (|Δref 10 s| < 3) | 0.13 (n=215) | 0.74 (n=215) | 2.69 (n=215) | 0.74 (n=215) | 0.63 (n=215) |
| transition (|Δref 10 s| ≥ 3) | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |

Confiance Data Row : high 97 % · medium 0 % · low 3 %

Détection de coups (candidat) : rappel 98 %, précision 98 % (64 détectés / 64 réf., décalage pic de pitch → prise d'eau +0.98 s, défini à un cycle près)


---

# Banc d'essai cadence — synthétique « step20_32 »

IMU : 4200 points · samples : 240 · référence : strokes.jsonl slot=1B seat=None (104 coups)

## Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 100 % | 0.69 | -0.28 | 2.03 | 0.68 | 93 % | 95 % | +3 s (MAE 0.63) |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 1.33 | 0.63 | 2.01 | 3.11 | 57 % | 78 % | -10 s (MAE 1.00) |
| Coup par coup, dernier cycle (bande large) | 100 % | 3.86 | 1.75 | 5.57 | 8.47 | 19 % | 44 % | -18 s (MAE 3.44) |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 1.33 | 0.63 | 2.01 | 3.11 | 57 % | 78 % | -10 s (MAE 1.00) |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.76 | 0.42 | 1.13 | 1.77 | 79 % | 91 % | -3 s (MAE 0.69) |

## Référence = cadence du dernier cycle (mesure la réactivité)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 99 % | 1.44 | -0.82 | 3.65 | 1.55 | 80 % | 93 % | +16 s (MAE 0.60) |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 1.39 | 0.06 | 1.98 | 2.82 | 49 % | 80 % | +6 s (MAE 1.30) |
| Coup par coup, dernier cycle (bande large) | 100 % | 3.54 | 1.15 | 5.01 | 8.23 | 23 % | 42 % | -14 s (MAE 3.48) |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 1.39 | 0.06 | 1.98 | 2.82 | 49 % | 80 % | +6 s (MAE 1.30) |
| Coup par coup, médiane 6, bande Data Row | 99 % | 1.04 | -0.14 | 1.87 | 1.71 | 69 % | 91 % | +5 s (MAE 0.75) |

## MAE par régime (réf. 24 s)

| Régime | Data Row actuel (autocorr. 24 s) | Coup par coup, médiane 6 cycles (bande large) | Coup par coup, dernier cycle (bande large) | Coup par coup, médiane 6, sans portillon vitesse | Coup par coup, médiane 6, bande Data Row |
|---|---|---|---|---|---|
| ref <20 spm | 0.22 (n=55) | 1.78 (n=55) | 4.88 (n=55) | 1.78 (n=55) | 0.68 (n=55) |
| ref 20-26 spm | 0.62 (n=64) | 1.68 (n=64) | 3.83 (n=64) | 1.68 (n=64) | 0.94 (n=64) |
| ref 26-32 spm | 1.25 (n=81) | 0.95 (n=81) | 3.47 (n=81) | 0.95 (n=81) | 0.78 (n=81) |
| ref 32-38 spm | 0.14 (n=27) | 0.68 (n=27) | 3.04 (n=27) | 0.68 (n=27) | 0.40 (n=27) |
| ref >=38 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| stable (|Δref 10 s| < 3) | 0.28 (n=195) | 1.23 (n=195) | 3.64 (n=195) | 1.23 (n=195) | 0.60 (n=195) |
| transition (|Δref 10 s| ≥ 3) | 4.55 (n=22) | 2.61 (n=22) | 6.40 (n=22) | 2.61 (n=22) | 2.26 (n=22) |

Confiance Data Row : high 93 % · medium 4 % · low 3 %

Détection de coups (candidat) : rappel 88 %, précision 88 % (104 détectés / 104 réf., décalage pic de pitch → prise d'eau +0.51 s, défini à un cycle près)

## Temps d'établissement après le saut de cadence (±1,5 spm tenu 5 s)

| Algo | Établissement |
|---|---|
| Data Row actuel (autocorr. 24 s) | 18 s |
| Coup par coup, médiane 6 cycles (bande large) | 13 s |
| Coup par coup, dernier cycle (bande large) | 13 s |
| Coup par coup, médiane 6, sans portillon vitesse | 13 s |
| Coup par coup, médiane 6, bande Data Row | 16 s |


---

# Banc d'essai cadence — synthétique « ramp18_36 »

IMU : 5250 points · samples : 300 · référence : strokes.jsonl slot=1B seat=None (135 coups)

## Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 100 % | 0.23 | 0.07 | 0.29 | 0.47 | 100 % | 100 % | -1 s (MAE 0.22) |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 0.71 | 0.12 | 0.93 | 1.45 | 72 % | 96 % | -2 s (MAE 0.70) |
| Coup par coup, dernier cycle (bande large) | 100 % | 3.44 | 1.26 | 5.07 | 8.15 | 22 % | 46 % | -30 s (MAE 3.39) |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 0.71 | 0.12 | 0.93 | 1.45 | 72 % | 96 % | -2 s (MAE 0.70) |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.58 | 0.22 | 0.75 | 1.29 | 80 % | 100 % | -3 s (MAE 0.57) |

## Référence = cadence du dernier cycle (mesure la réactivité)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 99 % | 0.67 | -0.50 | 0.82 | 1.33 | 77 % | 99 % | +9 s (MAE 0.51) |
| Coup par coup, médiane 6 cycles (bande large) | 99 % | 0.95 | -0.48 | 1.20 | 2.10 | 59 % | 90 % | +5 s (MAE 0.83) |
| Coup par coup, dernier cycle (bande large) | 99 % | 3.43 | 0.65 | 4.98 | 7.97 | 22 % | 41 % | -5 s (MAE 3.31) |
| Coup par coup, médiane 6, sans portillon vitesse | 99 % | 0.95 | -0.48 | 1.20 | 2.10 | 59 % | 90 % | +5 s (MAE 0.83) |
| Coup par coup, médiane 6, bande Data Row | 99 % | 0.83 | -0.38 | 1.03 | 1.65 | 67 % | 94 % | +9 s (MAE 0.71) |

## MAE par régime (réf. 24 s)

| Régime | Data Row actuel (autocorr. 24 s) | Coup par coup, médiane 6 cycles (bande large) | Coup par coup, dernier cycle (bande large) | Coup par coup, médiane 6, sans portillon vitesse | Coup par coup, médiane 6, bande Data Row |
|---|---|---|---|---|---|
| ref <20 spm | 0.15 (n=31) | 0.72 (n=31) | 2.98 (n=31) | 0.72 (n=31) | 0.37 (n=31) |
| ref 20-26 spm | 0.17 (n=103) | 0.68 (n=103) | 3.04 (n=103) | 0.68 (n=103) | 0.76 (n=103) |
| ref 26-32 spm | 0.26 (n=101) | 0.62 (n=101) | 3.65 (n=101) | 0.62 (n=101) | 0.47 (n=101) |
| ref 32-38 spm | 0.34 (n=52) | 0.92 (n=52) | 4.08 (n=52) | 0.92 (n=52) | 0.56 (n=52) |
| ref >=38 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| stable (|Δref 10 s| < 3) | 0.23 (n=277) | 0.70 (n=277) | 3.37 (n=277) | 0.70 (n=277) | 0.58 (n=277) |
| transition (|Δref 10 s| ≥ 3) | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |

Confiance Data Row : high 97 % · medium 0 % · low 3 %

Détection de coups (candidat) : rappel 98 %, précision 99 % (133 détectés / 135 réf., décalage pic de pitch → prise d'eau +0.75 s, défini à un cycle près)


---

# Banc d'essai cadence — synthétique « start_sequence »

IMU : 3150 points · samples : 180 · référence : strokes.jsonl slot=1B seat=None (98 coups)

## Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 98 % | 0.53 | -0.18 | 0.81 | 0.93 | 90 % | 94 % | +0 s (MAE 0.53) |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 1.10 | -0.49 | 1.38 | 2.39 | 59 % | 84 % | -6 s (MAE 0.82) |
| Coup par coup, dernier cycle (bande large) | 100 % | 3.62 | -0.15 | 4.78 | 7.48 | 26 % | 41 % | -9 s (MAE 3.16) |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 1.10 | -0.49 | 1.38 | 2.39 | 59 % | 84 % | -6 s (MAE 0.84) |
| Coup par coup, médiane 6, bande Data Row | 100 % | 0.76 | -0.35 | 1.05 | 1.72 | 77 % | 93 % | -4 s (MAE 0.58) |

## Référence = cadence du dernier cycle (mesure la réactivité)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 97 % | 1.28 | 0.64 | 1.88 | 3.15 | 57 % | 81 % | +10 s (MAE 0.96) |
| Coup par coup, médiane 6 cycles (bande large) | 98 % | 1.07 | 0.31 | 1.52 | 2.57 | 64 % | 83 % | +4 s (MAE 1.00) |
| Coup par coup, dernier cycle (bande large) | 98 % | 3.39 | 0.66 | 4.75 | 7.60 | 25 % | 50 % | -1 s (MAE 3.17) |
| Coup par coup, médiane 6, sans portillon vitesse | 99 % | 1.09 | 0.34 | 1.55 | 2.74 | 63 % | 82 % | +4 s (MAE 1.00) |
| Coup par coup, médiane 6, bande Data Row | 98 % | 1.03 | 0.45 | 1.51 | 2.25 | 65 % | 89 % | +6 s (MAE 0.86) |

## MAE par régime (réf. 24 s)

| Régime | Data Row actuel (autocorr. 24 s) | Coup par coup, médiane 6 cycles (bande large) | Coup par coup, dernier cycle (bande large) | Coup par coup, médiane 6, sans portillon vitesse | Coup par coup, médiane 6, bande Data Row |
|---|---|---|---|---|---|
| ref <20 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 20-26 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 26-32 spm | 0.33 (n=108) | 0.92 (n=108) | 3.77 (n=108) | 0.92 (n=108) | 0.55 (n=108) |
| ref 32-38 spm | 0.36 (n=33) | 1.24 (n=33) | 3.21 (n=33) | 1.24 (n=33) | 0.66 (n=33) |
| ref >=38 spm | 1.41 (n=30) | 1.55 (n=33) | 3.56 (n=33) | 1.55 (n=33) | 1.53 (n=33) |
| stable (|Δref 10 s| < 3) | 0.43 (n=152) | 0.98 (n=152) | 3.47 (n=152) | 0.98 (n=152) | 0.70 (n=152) |
| transition (|Δref 10 s| ≥ 3) | 0.44 (n=12) | 2.85 (n=12) | 6.74 (n=12) | 2.85 (n=12) | 1.38 (n=12) |

Confiance Data Row : high 78 % · medium 17 % · low 4 %

Détection de coups (candidat) : rappel 98 %, précision 99 % (97 détectés / 98 réf., décalage pic de pitch → prise d'eau -0.68 s, défini à un cycle près)


---

# Banc d'essai cadence — synthétique « sprint40 »

IMU : 4200 points · samples : 240 · référence : strokes.jsonl slot=1B seat=None (136 coups)

## Référence = cadence moyenne sur 24 s (équitable pour un estimateur fenêtré)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 100 % | 0.32 | -0.05 | 0.52 | 0.59 | 95 % | 98 % | +0 s (MAE 0.32) |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 1.40 | -0.02 | 1.89 | 3.09 | 49 % | 77 % | -7 s (MAE 1.38) |
| Coup par coup, dernier cycle (bande large) | 100 % | 4.33 | 0.05 | 6.10 | 8.31 | 15 % | 32 % | -9 s (MAE 4.17) |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 1.40 | -0.02 | 1.89 | 3.09 | 49 % | 77 % | -7 s (MAE 1.38) |
| Coup par coup, médiane 6, bande Data Row | 100 % | 1.10 | 0.49 | 1.59 | 2.23 | 63 % | 87 % | -7 s (MAE 0.99) |

## Référence = cadence du dernier cycle (mesure la réactivité)

| Algo | Couverture | MAE | Biais | RMSE | P90 | ±1 spm | ±2 spm | Retard estimé |
|---|---|---|---|---|---|---|---|---|
| Data Row actuel (autocorr. 24 s) | 98 % | 1.17 | -0.57 | 2.29 | 1.90 | 71 % | 90 % | +10 s (MAE 0.81) |
| Coup par coup, médiane 6 cycles (bande large) | 100 % | 1.54 | -0.58 | 2.18 | 3.00 | 44 % | 70 % | +5 s (MAE 1.34) |
| Coup par coup, dernier cycle (bande large) | 100 % | 4.18 | -0.49 | 6.01 | 8.58 | 14 % | 38 % | -1 s (MAE 4.09) |
| Coup par coup, médiane 6, sans portillon vitesse | 100 % | 1.54 | -0.58 | 2.18 | 3.00 | 44 % | 70 % | +5 s (MAE 1.34) |
| Coup par coup, médiane 6, bande Data Row | 100 % | 1.16 | -0.00 | 1.74 | 2.27 | 59 % | 83 % | +5 s (MAE 1.04) |

## MAE par régime (réf. 24 s)

| Régime | Data Row actuel (autocorr. 24 s) | Coup par coup, médiane 6 cycles (bande large) | Coup par coup, dernier cycle (bande large) | Coup par coup, médiane 6, sans portillon vitesse | Coup par coup, médiane 6, bande Data Row |
|---|---|---|---|---|---|
| ref <20 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 20-26 spm | — (n=0) | — (n=0) | — (n=0) | — (n=0) | — (n=0) |
| ref 26-32 spm | 0.26 (n=120) | 1.09 (n=120) | 3.84 (n=120) | 1.09 (n=120) | 0.86 (n=120) |
| ref 32-38 spm | 1.45 (n=11) | 3.75 (n=11) | 6.72 (n=11) | 3.75 (n=11) | 4.64 (n=11) |
| ref >=38 spm | 0.28 (n=100) | 1.51 (n=100) | 4.64 (n=100) | 1.51 (n=100) | 0.99 (n=100) |
| stable (|Δref 10 s| < 3) | 0.24 (n=200) | 1.21 (n=200) | 4.11 (n=200) | 1.21 (n=200) | 0.81 (n=200) |
| transition (|Δref 10 s| ≥ 3) | 1.07 (n=21) | 3.03 (n=21) | 6.99 (n=21) | 3.03 (n=21) | 3.49 (n=21) |

Confiance Data Row : high 64 % · medium 33 % · low 3 %

Détection de coups (candidat) : rappel 79 %, précision 84 % (128 détectés / 136 réf., décalage pic de pitch → prise d'eau -0.63 s, défini à un cycle près)

## Temps d'établissement après le saut de cadence (±1,5 spm tenu 5 s)

| Algo | Établissement |
|---|---|
| Data Row actuel (autocorr. 24 s) | 18 s |
| Coup par coup, médiane 6 cycles (bande large) | 9 s |
| Coup par coup, dernier cycle (bande large) | 6 s |
| Coup par coup, médiane 6, sans portillon vitesse | 9 s |
| Coup par coup, médiane 6, bande Data Row | 9 s |
