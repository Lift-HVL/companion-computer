# models/

YOLO-vektfiler. Ikke sjekk inn koden som *bruker* dem her — det bor i
`perception/`.

## Hva skal ligge her

| Fil            | Beskrivelse                                            |
| -------------- | ------------------------------------------------------ |
| `yolov8m.pt`   | YOLOv8 medium, standard base-modell fra Ultralytics.   |
| `my_model.pt`  | Egen-trent modell for Queen Bee-målet.                 |

Filnavn matcher det `config.YOLO_MODEL_PATH` peker på. Endres filnavnet,
endres `config.py`.

## Sjekk-inn-regler

Store `.pt`-filer er OK å committe hvis de er små nok for repoet, men
foretrukket praksis:

- Base-modeller (yolov8n/s/m/l/x) lastes ned én gang og pekes på — ikke
  committes.
- Egen-trente modeller committes med en kort tekstbit i denne READMEen
  om dato, treningssett og ytelse.

## Sporing av egne modeller

Når en ny egen-trent modell legges til, oppdater tabellen under:

| Modell         | Dato       | Treningssett | mAP@50 | Notat                       |
| -------------- | ---------- | ------------ | ------ | --------------------------- |
| `my_model.pt`  | YYYY-MM-DD | (fyll inn)   | (fyll) | (fyll inn kort om treningen)|

## Hva skal *ikke* ligge her

- Python-kode.
- Bilder eller video (bruk `.gitignore` for det).
- Skript for trening — de hører hjemme i et eget verktøy-repo, ikke i
  produksjons­koden på Pi-en.
