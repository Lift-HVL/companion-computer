# utils/

Små, generelle hjelpere. Ingen drone-kunnskap.

En modul hører hjemme her hvis den kan flyttes rett over i et annet
Python-prosjekt uten endring. Så snart en fil begynner å importere fra
`mavlink/`, `fsm/`, `perception/` eller `autonomy/`, tilhører den ikke
utils lenger.

## Hva skal ligge her

| Fil           | Ansvar                                                                        |
| ------------- | ----------------------------------------------------------------------------- |
| `logger.py`   | Én tidsstemplet loggfil per kjøring, én linje per iterasjon.                  |
| `keyboard.py` | Ikke-blokkerende tastatur-lesing fra terminalen (Linux + Windows).            |
| `rate.py`     | Enkel loop-timer: `wait_next_tick()` sover det som mangler for å holde HZ.    |

## Kontrakter

- Ingen global tilstand. Alt er klasser eller rene funksjoner.
- Ingen `print()` — bruk `logger` eller la det være.
- `keyboard.get_key()` returnerer `str | None`. Aldri unntak.

## Operatør-taster

Selve *hva* tastene betyr er ikke utils-domene — mappingen bor i
`fsm/event_generator.py`. `keyboard.py` leverer bare tegnet.

Referanse for hva som brukes i dag (holdes i sync med `event_generator`):

| Tast | Effekt                       | Betingelse               |
| ---- | ---------------------------- | ------------------------ |
| `s`  | Start søk                    | FSM i `HOVER`            |
| `l`  | Land                         | Alle tilstander          |
| `r`  | Reset fra failsafe           | FSM i `FAILSAFE`         |
| `q`  | Avslutt rent                 | Alle tilstander          |

## Hva skal *ikke* ligge her

- Konfigurasjon (bor i `config.py` på rot).
- Domene-modeller (`VehicleState`, `Detection`, …).
- Alt som kaller `pymavlink` eller `ultralytics`.
