from dataclasses import dataclass
from typing import Optional


@dataclass
class VehicleState:
    connected: bool = False
    last_heartbeat_time: float = 0.0

    armed: bool = False
    mode: str = "UNKNOWN"

    altitude_relative_m: float = 0.0
    altitude_absolute_m: float = 0.0

    latitude: Optional[float] = None
    longitude: Optional[float] = None
    heading_deg: Optional[float] = None

    groundspeed_m_s: float = 0.0
    climb_rate_m_s: float = 0.0

    battery_voltage_v: Optional[float] = None
    battery_remaining_pct: Optional[int] = None

    gps_fix_type: int = 0
    satellites_visible: int = 0
    gps_ok: bool = False

    ekf_ok: bool = False
