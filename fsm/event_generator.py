from typing import Optional

from config import (
    CRITICAL_BATTERY_THRESHOLD,
    HEARTBEAT_TIMEOUT,
    LOW_BATTERY_THRESHOLD,
    MIN_SATELLITES,
    TAKEOFF_ALTITUDE,
)
from fsm.event import Event
from fsm.states import State


FLYING_STATES = {
    State.ARMED,
    State.TAKEOFF,
    State.HOVER,
    State.SEARCH,
    State.TRACK,
    State.RTL,
}


class EventGenerator:
    def generate(
        self,
        state: State,
        vehicle,
        detection,
        key: Optional[str],
        now: float,
    ) -> Optional[Event]:
        """Return the highest-priority event for the current loop tick."""
        if state is not State.BOOT:
            heartbeat_age = now - vehicle.last_heartbeat_time
            if not vehicle.connected or heartbeat_age > HEARTBEAT_TIMEOUT:
                return Event.FAULT

        if state is State.BOOT:
            return Event.INIT_OK if vehicle.connected else None

        battery = vehicle.battery_remaining_pct
        if battery is not None:
            if battery <= CRITICAL_BATTERY_THRESHOLD:
                return Event.CRITICAL_FAULT
            if battery <= LOW_BATTERY_THRESHOLD:
                return Event.RECOVERABLE_FAULT

        if key == "l":
            return Event.LAND
        if key == "r" and state is State.FAILSAFE:
            return Event.RESET_ON_GND
        if key == "s" and state is State.HOVER:
            return Event.START_SEARCH
        if key == "t" and state is State.ARMED and self._takeoff_ready(vehicle):
            return Event.TAKEOFF

        if state in FLYING_STATES:
            if not vehicle.gps_ok or not vehicle.ekf_ok:
                return Event.FAULT
            if vehicle.satellites_visible < MIN_SATELLITES:
                return Event.FAULT

        if state is State.STANDBY and vehicle.armed:
            return Event.ARMED
        if state is State.ARMED and not vehicle.armed:
            return Event.DISARMED

        if (
            state is State.TAKEOFF
            and vehicle.altitude_relative_m >= TAKEOFF_ALTITUDE
        ):
            return Event.ALTITUDE_REACHED

        if (
            state is State.LAND
            and not vehicle.armed
            and vehicle.altitude_relative_m <= 0.1
        ):
            return Event.LANDED

        if state is State.RTL and getattr(vehicle, "home_reached", False):
            return Event.HOME_REACHED

        if state is State.SEARCH and detection is not None:
            return Event.TARGET_FOUND
        if state is State.TRACK and detection is None:
            return Event.TARGET_LOST

        return None

    @staticmethod
    def _takeoff_ready(vehicle) -> bool:
        battery = vehicle.battery_remaining_pct
        return (
            vehicle.connected
            and vehicle.gps_ok
            and vehicle.ekf_ok
            and vehicle.satellites_visible >= MIN_SATELLITES
            and battery is not None
            and battery > LOW_BATTERY_THRESHOLD
        )
