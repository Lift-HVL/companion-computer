from dataclasses import dataclass

from .vehicle_state import VehicleState

# Define a dataclass to hold the health status flags
@dataclass
class HealthStatus:
    gps_ok: bool
    ekf_ok: bool
    battery_ok: bool


# Derive health flags from the latest vehicle telemetry
def evaluate_health(state: VehicleState) -> HealthStatus:
    """Derive health flags from the latest vehicle telemetry."""

    # GPS is considered OK if the fix type is 3D or better (3 or 4)
    gps_ok = state.gps_fix_type >= 3

    # EKF is considered OK if the EKF status flag is True
    ekf_ok = state.ekf_ok

    # Battery is considered OK if the remaining percentage is known and above 20%
    battery_ok = (
        state.battery_remaining_pct is not None
        and state.battery_remaining_pct >= 20
    )

    # Return the health status as a dataclass instance
    return HealthStatus(
        gps_ok=gps_ok,
        ekf_ok=ekf_ok,
        battery_ok=battery_ok,
    )