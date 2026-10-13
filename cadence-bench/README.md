# cadence-bench

Banc d'essai de la cadence de **Data Row** (`apps/datar0w/lib/session/tel_cadence.dart`, repo
`1o68o7/AvSim-v1`) face à un détecteur **coup par coup** inspiré d'Open Rowing Monitor.
Python 3 standard uniquement (pas de dépendance). Destiné à rejoindre `AvSim-v1/tools/cadence-bench/`.

## Ce qu'il fait

1. Rejoue un `imu.jsonl` (`pitch_raw`, `gy`, horodatage `t` en ms) dans :
   * `dart_ac` : **port fidèle** de `TelCadenceDetector` (passe-bande 0,28–0,68 Hz, autocorrélation sur
     24 s, recoupement par les pics, confiance high/medium/low, portillon vitesse) ;
   * `stroke_*` : détecteur coup par coup (hystérésis creux→pic, bornes de durée de cycle,
     médiane des 6 derniers cycles). Variantes : bande large, bande Data Row, sans portillon vitesse,
     dernier cycle seul.
2. Compare à une **référence** sur une grille de 1 Hz : couverture, MAE, biais, RMSE, P90, % à ±1/±2 spm,
   retard estimé, MAE par régime (tranche de cadence, stable/transitoire), rappel et précision de la
   détection de coups.

## Utilisation

```bash
cd cadence-bench
python3 -m cadence_bench run <dossier_séance> --ref strokes.jsonl [--slot 1B] --md rapport.md --json rapport.json
python3 -m cadence_bench run --imu imu.jsonl --samples samples.jsonl --ref prises_deau.csv
python3 -m cadence_bench suite --noise 2.5 --md reports/synthetic-suite.md   # scénarios synthétiques
python3 -m cadence_bench synth step20_32 /tmp/s --noise 2.0 --burst           # générer une séance
python3 -m unittest discover -s tests -t .                                    # tests
```

Entrées : `imu.jsonl` ; `samples.jsonl` (1 Hz, champ `sog` pour le portillon vitesse) ;
référence = `strokes.jsonl` du stroke sensor (champ `t`, filtrage `--slot`/`--seat`) **ou** CSV d'instants
de prise d'eau (ms UTC ou s). Sans `--ref`, le rapport se limite à la couverture et à la cadence médiane.

## Deux références, pourquoi

* **moyenne 24 s** : équitable pour un estimateur fenêtré, mais favorise Data Row (même fenêtre) ;
* **dernier cycle** : mesure la réactivité, mais contient le bruit coup à coup (~2 %) du rameur.

Lire les deux. Pour la réactivité, la `suite` mesure aussi le **temps d'établissement** après un saut de cadence.

## Limites — à lire avant d'interpréter

* **Aucun `imu.jsonl` réel n'est dans les dépôts** (exports non versionnés ; les jeux `data/mock/stroke-sensor`
  sont simulés et ne contiennent pas d'IMU). Les chiffres des `reports/` sont **synthétiques**
  (bruit blanc gaussien, forme d'onde inventée) : ils valident le banc et donnent des ordres de grandeur,
  **pas** les performances en eau.
* La vérité terrain réelle devra venir d'un stroke sensor, d'un PM5 ou d'un pointage vidéo, sur la même
  séance et avec des horloges alignées (le `t` de `strokes.jsonl` est l'heure de réception, quelques ms à
  quelques centaines de ms de retard BLE possibles).
* Le port Python est vérifié par `tests/test_dart_port.py`, qui rejoue les tests de `imu_cadence_test.dart`.
  Il n'est pas comparé sortie à sortie avec le Dart sur des séries réelles (Dart absent de l'environnement) :
  à faire en exécutant le Dart sur le même `imu.jsonl` et en comparant à `dart_ac`.
* Le détecteur coup par coup est un **candidat**, pas le moteur d'ORM (qui travaille sur les impulsions d'un
  volant d'ergomètre). Le décalage entre pic de pitch et prise d'eau est défini à un cycle près.
