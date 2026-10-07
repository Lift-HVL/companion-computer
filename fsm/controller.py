from fsm.event import Event
from fsm.states import State


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


class FSM:
    def __init__(self) -> None:
        self.state = State.BOOT

    def handle(self, event: Event) -> State:
        """Handle one event and return the current state."""
        if event is Event.CRITICAL_FAULT:
            self.state = State.LAND
        elif event is Event.RECOVERABLE_FAULT:
            self.state = State.RTL
        elif event is Event.FAULT:
            self.state = State.FAILSAFE
        else:
            self.state = TRANSITIONS.get(
                (self.state, event),
                self.state,
            )

        return self.state
