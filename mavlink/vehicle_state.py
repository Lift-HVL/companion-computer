from dataclass import dataclass
from typing import Optional

@dataclass
class vehicle_state:
    
    #HEARTBEAT
    connected : Bool = False
    armed : Bool = False
    mode : Optional[str] = None

    #GLOBAL_POSITION_INT
    altitiude_relative_m : float = 0.0
    latitude : float = 0.0
    longitude : float = 0.0
    heading : float = 0.0 #Degrees

    #GPS_RAW_INT
    gps_fix_type : int = 0
    satallites_visible : int = 0    
    
    #SYS_STATUS
    battery_voltage_v : float = 0.0
    battery_remaining_pct : int = 0 #percentage

    #VFR_HUD
    groundspeed_m_s : float = 0.0
    climb_rate_m_s : float = 0.0

    #EKF_STATUS_REPORT
    ekf_ok : bool = False




    