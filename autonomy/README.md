# autonomy/

Autonome atferder. Én fil per atferd. Ingen atferd tar over loopen — de
eksponerer bare `update()` og lar `main.py` bestemme takten.

Dette er stedet der `perception/` (hva ser vi?) møter `mavlink/commands`
(hva skal vi gjøre?). Regulatorer, søkemønstre og tilnærmings­strategier
hører hjemme her.

## Hva skal ligge her

| Fil         | Ansvar                                                                        |
| ----------- | ----------------------------------------------------------------------------- |
| `track.py`  | `TargetTracker` — PI-regulert yaw mot mål, fremdrift til bbox fyller frame.   |
| `search.py` | `SearchPattern` — ikke-blokkerende plenklipper-mønster (våken pr. tick).     |

Legg til flere filer når nye atferder trengs (patrulje, formasjons­flyging,
osv.). Én fil, én klasse, én `update()`.

## Standard-kontrakt for en atferd

```python
class Behaviour:
    def __init__(self, mavlink_commands, config): ...

    def update(self, vehicle_state, detection, dt) -> bool:
        """Kjør ett steg. Returner True hvis oppgaven er fullført."""

    def reset(self) -> None:
        """Kalles når FSM forlater atferden. Nullstill regulator-tilstand."""
```

- **Ikke-blokkerende.** `update()` skal returnere umiddelbart.
- **Idempotent oppstart.** `reset()` må kunne kalles gjentatte ganger uten
  å ødelegge intern tilstand.
- **Ingen egne timers.** `dt` sendes inn fra loopen. Aldri `time.sleep()`.
- **Ingen direkte skriv til `VehicleState`.** Atferden leser derfra og
  skriver til `mavlink/commands`.

## PI-regulator (`track.py`)

- Utgang = `KP × pixel_error + KI × integral`
- Integralet klemmes til `±YAW_INTEGRAL_MAX` (anti-windup).
- Både integral og timer nullstilles ved `reset()` — også hver gang målet
  forsvinner mellom to ticks. Ellers slår gammelt avvik inn på neste
  observasjon.
- Sluttavstand måles på bbox-høyde relativt til frame-høyde
  (`BBOX_REACH_THRESHOLD`). Ingen rangefinder kreves.

## Hva skal *ikke* ligge her

- MAVLink-parsing (bruk `mavlink/vehicle_state.py`).
- YOLO-inferens (bruk `perception/detector.py`).
- FSM-overganger — atferden signaliserer bare `True` når den er ferdig;
  `event_generator.py` gjør det om til `TASK_COMPLETED`.
