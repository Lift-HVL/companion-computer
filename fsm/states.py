from enum import Enum, auto

class State(Enum):
    BOOT = auto()                   # Drone is booting up
    STANDBY = auto()                # Drone is on standby, waiting for commands
    ARMED = auto()                  # Drone is armed and ready to take off   
    TAKEOFF = auto()                # Drone is taking off
    HOVER = auto()                  # Drone is hovering in place
    SEARCH = auto()
    TRACK = auto()
    FAILSAFE = auto()               # Drone is in failsafe mode due to an error or loss of signal
    RTL = auto()                    # Drone is returning to launch point
    LAND = auto()                   # Drone is landing
    
    