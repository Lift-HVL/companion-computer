# mavlink/

All kommunikasjon med ArduPilot-flightcontrolleren. Ingenting annet.

Denne mappen er en tynn bro mellom `pymavlink` og resten av koden. Ingen
forretningslogikk, ingen FSM-kjennskap, ingen kamera. Hvis en modul her må
importere fra `fsm/`, `autonomy/` eller `perception/`, står den feil sted.

## Hva skal ligge her

| Fil               | Ansvar                                                                              |
| ----------------- | ----------------------------------------------------------------------------------- |
| `client.py`       | Åpner MAVLink-tilkobling (UDP eller serial), leverer rå meldinger inn i loopen.     |
| `vehicle_state.py`| `@dataclass` med ferskeste telemetri. Oppdateres av `client.py` i loopen.           |
| `commands.py`     | Sender kommandoer: `arm`, `disarm`, `takeoff`, `land`, `set_yaw_rate`, `set_forward_speed`, `rtl`. |
| `health.py`       | Utleder helse-flagg (`gps_ok`, `ekf_ok`, batteri-nivå) fra `VehicleState`.          |

## Kontrakter

- `client.py` er **ikke-blokkerende**. `drain()` returnerer med en gang;
  loopen kaller den én gang per iterasjon.
- `VehicleState` er en ren dataklasse — ingen metoder som gjør I/O.
- `commands.py` returnerer så snart meldingen er lagt på tråden. Den venter
  ikke på ACK. Bekreftelse på at kommandoen ble utført leses av loopen fra
  neste `VehicleState`-oppdatering.
- Rammer for hastighetskommandoer bruker `MAV_FRAME_BODY_NED`, slik at
  "forover" alltid er dronas nese uansett heading.

## Meldinger vi bryr oss om

Bare disse parses inn i `VehicleState`. Andre meldinger droppes stille.

```
HEARTBEAT            → connected, armed, mode
GLOBAL_POSITION_INT  → altitude_relative_m, lat/lon, heading
GPS_RAW_INT          → gps_fix_type, satellites_visible
SYS_STATUS           → battery_voltage_v, battery_remaining_pct
VFR_HUD              → groundspeed_m_s, climb_rate_m_s
EKF_STATUS_REPORT    → ekf_ok
```

Legg til en ny melding bare hvis den brukes av `event_generator` eller en
konkret kommando. Ellers vokser dataklassen uten grunn.

## Hva skal *ikke* ligge her

- FSM-hendelser eller state-navn.
- Kamera- eller deteksjonskode.
- Regulatorer (PI, PID) — de hører hjemme i `autonomy/`.
- Retry-løkker eller blokkerende `wait_for_message`. Loopen eier tiden.
