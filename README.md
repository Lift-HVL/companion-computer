# companion-computer — Queen Bee onboard brain

Autonom flykontroll for Raspberry Pi 5 om bord på Queen Bee. Pi-en snakker
MAVLink med en ArduPilot-flightcontroller, kjører YOLOv8-deteksjon på et USB-kamera,
og styrer atferd gjennom en enkel tilstandsmaskin (FSM).

Denne versjonen er en lettvekts-omskriving. Målet er lite kode, tydelige
grenser mellom moduler, og at ingenting kjører i loopen som ikke må være der.

## Rask start

```bash
pip install -r requirements.txt
python main.py
```

Alle knotter og tunbare parametere lever i `config.py`. MAVLink-tilkoblingen
kan overstyres uten å røre filen:

```bash
LIFT_MAVLINK_CONNECTION=udpin:127.0.0.1:14552 python main.py   # bridge
LIFT_MAVLINK_CONNECTION=/dev/ttyAMA0                python main.py   # serial
```

## Arkitektur

Én kontroll-loop i `main.py` binder tre lag sammen i fast takt:

```
                       main.py  (kontroll-loop)
                          │
   ┌──────────────────────┼──────────────────────┐
   ▼                      ▼                      ▼
 mavlink/                fsm/                perception/
 telemetri +          tilstander +          kamera +
 kommandoer           hendelser            deteksjon
                          ▲
                          │
                      autonomy/
                      søk + tracking

              utils/  logging · tastatur · felles
              models/ YOLO-vekter
```

Hver iterasjon av loopen gjør bare fem ting:

1. Tømmer MAVLink-bufferen inn i en fersk `VehicleState`.
2. Kjører én kamera-frame gjennom detektoren.
3. Leser eventuell operatør-tast.
4. Genererer én FSM-hendelse ut fra state + deteksjon + tastetrykk, og lar
   FSM-en avgjøre neste tilstand.
5. Utfører atferden som hører til gjeldende tilstand (søk, tracking, hover, …).

Alt annet — telemetri-parsing, PI-regulator, kamera-oppsett, YOLO-inferens —
er innkapslet bak modulgrensene under.

## Mappestruktur

```
companion-computer/
├── main.py              # entry point + kontroll-loop
├── config.py            # alle tunbare parametere
├── requirements.txt     # Python-avhengigheter
├── README.md            # (denne filen)
│
├── mavlink/             # ArduPilot-bro: telemetri, kommandoer, helse
├── fsm/                 # tilstandsmaskin: states, events, transitions
├── perception/          # kamera + YOLO-deteksjon
├── autonomy/            # autonome atferder (søk, tracking)
├── utils/               # logging, tastatur, felles hjelpere
└── models/              # YOLO-vekter (.pt-filer)
```

Hver mappe har sin egen README som forklarer hva som hører hjemme der og
hva som ikke gjør det. Kort oppsummert:

| Mappe         | Ansvar                                                                 |
| ------------- | ---------------------------------------------------------------------- |
| `mavlink/`    | All kommunikasjon med flightcontrolleren. Ingen forretningslogikk.     |
| `fsm/`        | Tilstander, hendelser og overganger. Vet ingenting om MAVLink.         |
| `perception/` | Kamera-abstraksjon og YOLO-inferens. Returnerer bare deteksjoner.      |
| `autonomy/`   | Én atferd per fil. Leser deteksjoner, skriver til `mavlink/commands`.  |
| `utils/`      | Små, generelle hjelpere. Kjenner ikke til drone-domene.                |
| `models/`     | Bare vektfiler og en README som sier hvor de kommer fra.               |

## Prinsipper for koden

- **Én ting per fil.** Hvis en fil trenger to overskrifter, er det to filer.
- **Loopen eier tiden.** Moduler eksponerer korte, ikke-blokkerende
  `update()`-metoder. Ingen `sleep`, ingen ventende socket-lesing utenfor
  loopen selv.
- **Config er data.** `config.py` inneholder verdier, ikke kode. Alt som
  kan overstyres uten kodeendring, går via miljøvariabler.
- **Ingen sirkulære avhengigheter.** Pilene i arkitektur-diagrammet peker
  én vei. `autonomy/` importerer fra `mavlink/` og `perception/`; motsatt
  vei skjer aldri.
- **Feil er hendelser.** MAVLink-timeout, tapt GPS-fix, lav batteri —
  alt blir til én `Event` som FSM-en håndterer. Ingen kaster unntak opp
  gjennom loopen.

## Sikkerhet og failsafe

Batteri, GPS-fix, EKF-helse og heartbeat-timeout genererer `FAULT`,
`RECOVERABLE_FAULT` eller `CRITICAL_FAULT` og fører alltid tilbake til en
sikker tilstand (RTL eller LAND). Terskler ligger i `config.py`.

## Lisens

MIT — se `LICENSE`.
