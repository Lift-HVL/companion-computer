from pymavlink import mavutil
from mavlink.vehicle_state import VehicleState


class MAVLinkClient:
    def __init__(self, connection_string: str, baudrate: int) -> None:
        self.connection = mavutil.mavlink_connection(
            connection_string,
            baud=baudrate,
        )

    def drain(
        self,
        state: VehicleState,
        now: float,
    ) -> int:
        received_count = 0

        while True:
            message = self.connection.recv_match(blocking=False)

            if message is None:
                break

            if message.get_type() == 'BAD_DATA':
                continue

            self._apply_message(
                state=state,
                message=message,
                now=now,
            )

            received_count += 1

        return received_count

    def _apply_message(self, state: VehicleState, message, now: float) -> None:

        message_type = message.get_type()

        if message_type == "HEARTBEAT":
            state.connected = True
            state.last_heartbeat_time = now

            state.armed = bool(
                message.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
            )
            state.mode = mavutil.mode_string_v10(message)

        elif message_type == "GLOBAL_POSITION_INT":
            state.latitude = message.lat / 10_000_000
            state.longitude = message.lon / 10_000_000

            state.altitude_relative_m = message.relative_alt / 1000.0
            state.altitude_absolute_m = message.alt / 1000.0

            if message.hdg == 65535:
                state.heading_deg = None
            else:
                state.heading_deg = message.hdg / 100.0

        elif message_type == "GPS_RAW_INT":
            state.gps_fix_type = message.fix_type
            state.satellites_visible = (
                0 if message.satellites_visible == 255
                else message.satellites_visible
            )
            state.gps_ok = message.fix_type >= 3  # 3D fix or better

        elif message_type == "SYS_STATUS":
            if message.voltage_battery == 65535:
                state.battery_voltage_v = None
            else:
                state.battery_voltage_v = message.voltage_battery / 1000.0

            if message.battery_remaining < 0:
                state.battery_remaining_pct = None
            else:
                state.battery_remaining_pct = message.battery_remaining

        elif message_type == "VFR_HUD":
            state.groundspeed_m_s = message.groundspeed
            state.climb_rate_m_s = message.climb

        elif message_type == "EKF_STATUS_REPORT":
            required_flags = 0x1F
            state.ekf_ok = (message.flags & required_flags) == required_flags
