# fsm/

Tilstandsmaskinen. Bestemmer hva drona *får lov til* å gjøre akkurat nå.

FSM-en kjenner ikke MAVLink, ikke YOLO, og ikke kamera. Den tar imot én
`Event` per tick og svarer med en ny (eller uendret) tilstand. Alt annet
er utenfor mandat.

## Hva skal ligge her

| Fil                  | Ansvar                                                                    |
| -------------------- | ------------------------------------------------------------------------- |
| `states.py`          | `State`-enum og `Autonomy`-enum (`SEARCH`, `TRACK`, `NONE`).              |
| `event.py`           | `Event`-enum med alle triggere.                                           |
| `controller.py`      | `FSMController` — overgangs­tabell og `handle_event(event)`.              |
| `event_generator.py` | Maper `VehicleState` + detektor + operatør-tast → én `Event` per tick.    |

## Tilstander

```
BOOT → STANDBY → ARMED → TAKEOFF → HOVER ⇄ MANUAL
                                     │
                                     ├─ SEARCH ⇄ TRACK
                                     └─ LAND → STANDBY

Alle tilstander ── FAULT ──► FAILSAFE ── RECOVERABLE ─► RTL ─► LAND
                                     └── CRITICAL   ─────────► LAND
                                     └── RESET_ON_GND ───────► STANDBY
```

Selve overgangs­tabellen bor i `controller.py`. Diagrammet over er
sannheten om hvordan tabellen skal se ut — endres én, endres den andre.

## Prioritet i `event_generator`

Bare **én** hendelse per tick. Rekkefølgen bestemmer hva som vinner:

1. Tilkoblingsfeil (heartbeat-timeout)
2. Init (første heartbeat mottatt)
3. Arm / disarm (fra telemetri)
4. Høyde nådd (takeoff → hover)
5. Landing (`LANDED_DISARM`)
6. Batteri (critical før low)
7. GPS/EKF-helse
8. Måldeteksjon (`START_TRACK` / `TARGET_LOST`)

## Kontrakter

- `handle_event()` er **ren funksjon av (state, event)**. Ingen side-effekter,
  ingen I/O, ingen logging fra denne filen.
- Ukjent event i en gitt state ignoreres — loggingen forteller det, ikke
  et unntak.
- `event_generator.generate()` returnerer `Event | None`. `None` betyr
  "ingenting endret seg, hold posisjon".

## Hva skal *ikke* ligge her

- MAVLink-parsing eller kommandoer.
- Regulatorer eller kamera-oppsett.
- Timers eller `sleep`. Tid kommer inn som feltet `now` i `generate()`.
