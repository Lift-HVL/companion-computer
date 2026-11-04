from enum import Enum, auto

class Event(Enum):
    INIT_OK = auto()                  # Initialization completed successfully

    ARMED = auto()                    # Arm command
    DISARMED = auto()                 # Disarm command

    TAKEOFF = auto()                  # Takeoff command
    ALTITUDE_REACHED = auto()         # Drone has reached the desired altitude

    START_SEARCH = auto()             # Start search command
    TARGET_FOUND = auto()             # Drone has found the target
    TARGET_LOST = auto()              # Drone has lost the target
    STOP_OPERATION = auto()           # Stop search/track operation command

    LAND = auto()                     # Land command
    # ABORT_LANDING = auto() #Implement later if needed
    LANDED = auto()                   # Drone has landed

    # FORCE_RETURN = auto() #Implement later if needed
    # ABORT_RETURN = auto() #Implement later if needed
    
    HOME_REACHED = auto()             # Drone has reached the home position
    RESET_ON_GND = auto()             # Drone has reset while on the ground
    
    MANUAL_OVERRIDE = auto()
    MANUAL_DONE = auto()
    
    FAULT = auto()                    # Drone has encountered a fault
    RECOVERABLE_FAULT = auto()        # Drone has encountered a recoverable fault
    CRITICAL_FAULT = auto()           # Drone has encountered a critical fault

