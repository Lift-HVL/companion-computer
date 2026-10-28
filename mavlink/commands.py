import math

from pymavlink import mavutil

YAW_RATE_MASK = (
      mavutil.mavlink.POSITION_TARGET_TYPEMASK_X_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_Y_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_Z_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_IGNORE
  )

VELOCITY_ONLY_MASK = (
      mavutil.mavlink.POSITION_TARGET_TYPEMASK_X_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_Y_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_Z_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_IGNORE
      | mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_RATE_IGNORE
  )


class MAVLinkCommands:
    def __init__(self, connection) -> None:
        self.connection = connection

    def set_mode(self, mode_name: str) -> None:
        """Spørr ArduPilot til å endre fly modus"""
        mode_mapping = self.connection.mode_mapping()

        if mode_mapping is None or mode_name not in mode_mapping: 
            raise ValueError(f"Unknown flight mode: {mode_name}")

        mode_id = mode_mapping[mode_name]

        self.connection.mav.set_mode_send(
            self.connection.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,mode_id,
        )

        def guided(self) -> None:
            """Entrer GUIDED modus for companion-computer control."""