from fsm.event import Event
from fsm.states import State

# Define the state transition mapping for the finite state machine (FSM).
TRANSITIONS = {
    #Startup
    (State.BOOT, Event.INIT_OK): State.STANDBY,
    (State.STANDBY, Event.ARMED): State.ARMED,
    
    #Armed -> next state
    (State.ARMED, Event.DISARMED): State.STANDBY,
    (State.ARMED, Event.TAKEOFF): State.TAKEOFF,
    (State.ARMED, Event.FAULT): State.STANDBY, #Necessary? Go to failsafe instead?
    
    #Takeoff -> next state
    (State.TAKEOFF, Event.LAND): State.LAND,
    (State.TAKEOFF, Event.ALTITUDE_REACHED): State.HOVER,
    (State.TAKEOFF, Event.FAULT): State.LAND, #Necessary? ...
    
    #etc
    (State.HOVER, Event.START_SEARCH): State.SEARCH,
    (State.HOVER, Event.MANUAL_OVERRIDE): State.MANUAL,
    (State.HOVER, Event.LAND): State.LAND,
    (State.HOVER, Event.FAULT): State.FAILSAFE,
    
    (State.MANUAL, Event.MANUAL_DONE): State.HOVER,
    (State.MANUAL, Event.FAULT): State.FAILSAFE,
    
    (State.SEARCH, Event.TARGET_FOUND): State.TRACK,
    (State.SEARCH, Event.STOP_OPERATION): State.HOVER,
    (State.SEARCH, Event.FAULT): State.FAILSAFE,
    
    (State.TRACK, Event.TARGET_LOST): State.SEARCH,
    (State.TRACK, Event.STOP_OPERATION): State.HOVER,
    (State.TRACK, Event.FAULT): State.FAILSAFE,

    (State.RTL, Event.HOME_REACHED): State.LAND,  #Implement abort landing+RTL?
    (State.LAND, Event.LANDED): State.STANDBY,
    
    (State.FAILSAFE, Event.RECOVERABLE_FAULT): State.RTL,
    (State.FAILSAFE, Event.CRITICAL_FAULT): State.LAND,
    (State.FAILSAFE, Event.RESET_ON_GND): State.STANDBY,  #Farlig, eneste som skrur av motorer i luften
}

# Define the finite state machine (FSM) class that manages state transitions based on events.
class FSM:

    # Initialize the FSM with the initial state set to BOOT.
    def __init__(self) -> None:
        self.state = State.BOOT

    # Define the method to handle events and update the current state based on the event received.
    def handle(self, event: Event) -> State:   
        """Handle one event and return the current state."""

        self.state = TRANSITIONS.get(
            (self.state, event),
            self.state,
        )

        # Return the current state after handling the event.
        return self.state
