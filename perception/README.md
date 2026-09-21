# perception/

Kamera og objektdeteksjon. Alt som gjør piksler om til `Detection`-objekter.

Denne mappen er en ren produsent: den leverer siste deteksjon på forespørsel.
Den bestemmer aldri hva drona skal gjøre — det er `autonomy/` sin jobb.

## Hva skal ligge her

| Fil          | Ansvar                                                                            |
| ------------ | --------------------------------------------------------------------------------- |
| `camera.py`  | `Camera`-klasse rundt OpenCV `VideoCapture`. `read()` gir siste frame eller `None`. |
| `detector.py`| YOLOv8-innpakking. `update(frame)` returnerer `Detection` eller `None`.           |
| `types.py`   | `Detection`-dataklasse (bbox, konfidens, klasse, frame-størrelse).                |

## Kontrakter

- `Camera.read()` er **ikke-blokkerende**. Feilaktig frame → `None`.
- `Detector.update()` kjøres én gang per YOLO-tick (se `YOLO_UPDATE_RATE`
  i `config.py`). Mellom ticks returnerer den forrige detection uendret,
  eller `None` hvis ingen.
- `Detection`-koordinater er i piksler, med origo i øvre venstre hjørne av
  frame. Konvertering til vinkelfeil gjøres i `autonomy/track.py`, ikke her.
- Kildekilden til frames (USB-kamera, fil, RTSP) er byttbar bak `Camera`.
  Resten av koden skal ikke merke forskjell.

## Visning

Annotert frame kan vises i et OpenCV-vindu for debug, men vinduet er
**valgfritt** og styres av `SHOW_CAMERA` i `config.py`. Produksjonsdrift på
Pi-en kjører uten `imshow`.

## Modeller

Vektfiler ligger i `../models/`. `detector.py` leser stien fra
`config.YOLO_MODEL_PATH` — aldri hard-kodet.

## Hva skal *ikke* ligge her

- Regulatorer eller yaw-beregning.
- MAVLink-kall.
- FSM-hendelser (`START_TRACK` genereres i `fsm/event_generator.py`, ikke her).
