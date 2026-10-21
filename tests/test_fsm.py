import unittest

from fsm.controller import FSM
from fsm.event import Event
from fsm.states import State


class FSMTests(unittest.TestCase):
    def test_normal_flight_path(self) -> None:
        fsm = FSM()

        self.assertEqual(fsm.handle(Event.INIT_OK), State.STANDBY)
        self.assertEqual(fsm.handle(Event.ARMED), State.ARMED)
        self.assertEqual(fsm.handle(Event.TAKEOFF), State.TAKEOFF)
        self.assertEqual(fsm.handle(Event.ALTITUDE_REACHED), State.HOVER)
        self.assertEqual(fsm.handle(Event.START_SEARCH), State.SEARCH)
        self.assertEqual(fsm.handle(Event.TARGET_FOUND), State.TRACK)
        self.assertEqual(fsm.handle(Event.TARGET_LOST), State.SEARCH)
        self.assertEqual(fsm.handle(Event.LAND), State.LAND)
        self.assertEqual(fsm.handle(Event.LANDED), State.STANDBY)

    def test_critical_fault_lands_from_any_state(self) -> None:
        fsm = FSM()
        fsm.state = State.TRACK

        self.assertEqual(fsm.handle(Event.CRITICAL_FAULT), State.LAND)

    def test_recoverable_fault_uses_rtl(self) -> None:
        fsm = FSM()
        fsm.state = State.HOVER

        self.assertEqual(fsm.handle(Event.RECOVERABLE_FAULT), State.RTL)

    def test_unknown_transition_keeps_current_state(self) -> None:
        fsm = FSM()

        self.assertEqual(fsm.handle(Event.TARGET_FOUND), State.BOOT)


if __name__ == "__main__":
    unittest.main()
