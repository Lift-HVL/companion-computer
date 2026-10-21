from enum import Enum, auto

class Event(Enum):
    INIT_OK = auto()                  # Initialization completed successfully

    ARMED = auto()                     # Drone is armed and ready to take off
    DISARMED = auto()                  # Drone is disarmed

    TAKEOFF = auto()                   # Drone is taking off
    ALTITUDE_REACHED = auto()          # Drone has reached the desired altitude

    START_SEARCH = auto()                # Drone is starting the search operation
    TARGET_FOUND = auto()               # Drone has found the target
    TARGET_LOST = auto()                # Drone has lost the target

    LAND = auto()                    # Drone is landing
    LANDED = auto()                  # Drone has landed

    HOME_REACHED = auto()              # Drone has reached the home position
    RESET_ON_GND = auto()                # Drone has reset while on the ground
    
    FAULT = auto()                   # Drone has encountered a fault
    RECOVERABLE_FAULT = auto()        # Drone has encountered a recoverable fault
    CRITICAL_FAULT = auto()           # Drone has encountered a critical fault

