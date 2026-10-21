from fsm.event import Event
from fsm.states import State

# Define the state transition mapping for the finite state machine (FSM).
TRANSITIONS = {
    (State.BOOT, Event.INIT_OK): State.STANDBY,
    (State.STANDBY, Event.ARMED): State.ARMED,
    (State.ARMED, Event.DISARMED): State.STANDBY,
    (State.ARMED, Event.TAKEOFF): State.TAKEOFF,
    (State.TAKEOFF, Event.ALTITUDE_REACHED): State.HOVER,
    (State.HOVER, Event.START_SEARCH): State.SEARCH,
    (State.SEARCH, Event.TARGET_FOUND): State.TRACK,
    (State.TRACK, Event.TARGET_LOST): State.SEARCH,
    (State.ARMED, Event.LAND): State.LAND,
    (State.TAKEOFF, Event.LAND): State.LAND,
    (State.HOVER, Event.LAND): State.LAND,
    (State.SEARCH, Event.LAND): State.LAND,
    (State.TRACK, Event.LAND): State.LAND,
    (State.FAILSAFE, Event.LAND): State.LAND,
    (State.RTL, Event.HOME_REACHED): State.LAND,
    (State.LAND, Event.LANDED): State.STANDBY,
    (State.FAILSAFE, Event.RESET_ON_GND): State.STANDBY,
}

# Define the finite state machine (FSM) class that manages state transitions based on events.
class FSM:

    # Initialize the FSM with the initial state set to BOOT.
    def __init__(self) -> None:
        self.state = State.BOOT

    # Define the method to handle events and update the current state based on the event received.
    def handle(self, event: Event) -> State:
        """Handle one event and return the current state."""

        # Set state to LAND if critical fault
        if event is Event.CRITICAL_FAULT:
            self.state = State.LAND
        # Set state to RTL if recoverable fault
        elif event is Event.RECOVERABLE_FAULT:
            self.state = State.RTL
        # Set state to FAILSAFE if fault
        elif event is Event.FAULT:
            self.state = State.FAILSAFE
        # For all other events, look up the next state in the TRANSITIONS mapping.
        else:
            self.state = TRANSITIONS.get(
                (self.state, event),
                self.state,
            )

        # Return the current state after handling the event.
        return self.state
