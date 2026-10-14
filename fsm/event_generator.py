from typing import Optional

# Import configuration constants from the config module.
from config import (
    CRITICAL_BATTERY_THRESHOLD,
    HEARTBEAT_TIMEOUT,
    LOW_BATTERY_THRESHOLD,
    MIN_SATELLITES,
    TAKEOFF_ALTITUDE,
)

# import the Event and State classes from their respective modules.
from fsm.event import Event
from fsm.states import State

# Define the set of states that are considered "flying" states.
FLYING_STATES = {
    State.ARMED,
    State.TAKEOFF,
    State.HOVER,
    State.SEARCH,
    State.TRACK,
    State.RTL,
}

# Class responsible for generating events based on the current state, vehicle status, and user input.
class EventGenerator:

    # Generate an event based on the current state, vehicle status, detection, user input, and time.
    def generate(
        self,
        state: State,
        vehicle,
        detection,
        key: Optional[str],
        now: float,
    ) -> Optional[Event]:
        """Return the highest-priority event for the current loop tick."""

        # Update heartbeat_age and check for connection issues if the state is not BOOT.
        if state is not State.BOOT:
            heartbeat_age = now - vehicle.last_heartbeat_time
            if not vehicle.connected or heartbeat_age > HEARTBEAT_TIMEOUT:
                return Event.FAULT

        # Check for initialization completion if the state is BOOT.
        if state is State.BOOT:
            return Event.INIT_OK if vehicle.connected else None

        battery = vehicle.battery_remaining_pct # Get the remaining battery percentage from the vehicle.

        # Check battery levels and generate appropriate events based on thresholds.
        if battery is not None:
            if battery <= CRITICAL_BATTERY_THRESHOLD:
                return Event.CRITICAL_FAULT
            if battery <= LOW_BATTERY_THRESHOLD:
                return Event.RECOVERABLE_FAULT

        # Handle user input events based on the current state, and key pressed on the remote.
        if key == "l":
            return Event.LAND
        if key == "r" and state is State.FAILSAFE:
            return Event.RESET_ON_GND
        if key == "s" and state is State.HOVER:
            return Event.START_SEARCH
        if key == "t" and state is State.ARMED and self._takeoff_ready(vehicle):
            return Event.TAKEOFF

        # Check for faults in flying states based on GPS, EKF, and satellite visibility.
        if state in FLYING_STATES:
            # Check that the vehicle has a valid GPS and EKF (Extended Kalman Filter) status.
            if not vehicle.gps_ok or not vehicle.ekf_ok:
                return Event.FAULT
            # Check that the vehicle has a sufficient number of visible satellites.
            if vehicle.satellites_visible < MIN_SATELLITES:
                return Event.FAULT

        # Check for standby- and armed state, to generate events for arming and disarming the vehicle.
        if state is State.STANDBY and vehicle.armed:
            return Event.ARMED
        if state is State.ARMED and not vehicle.armed:
            return Event.DISARMED

        # Give ALTITUDE_REACHED event when the vehicle is in TAKEOFF state and has reached the desired altitude.
        if (
            state is State.TAKEOFF
            and vehicle.altitude_relative_m >= TAKEOFF_ALTITUDE
        ):
            return Event.ALTITUDE_REACHED

        # Give LANDED event when the vehicle is disarmed and on the ground.
        if (
            state is State.LAND
            and not vehicle.armed
            and vehicle.altitude_relative_m <= 0.1
        ):
            return Event.LANDED

        # Give HOME_REACHED event when the vehicle is in RTL state and has reached the home position.
        if state is State.RTL and getattr(vehicle, "home_reached", False):
            return Event.HOME_REACHED

        # Give TARGET_FOUND event when the vehicle is in SEARCH state and a target is detected.
        if state is State.SEARCH and detection is not None:
            return Event.TARGET_FOUND
        # Give TARGET_LOST event when the vehicle is in TRACK state and no target is detected.
        if state is State.TRACK and detection is None:
            return Event.TARGET_LOST

        # If no events are generated based on the above conditions, return None.
        return None

    # Check if the vehicle is ready for takeoff based on its connection status, GPS, EKF, satellite visibility, and battery level.
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
