import logging
from pymavlink import mavutil

class Command:

    #Arms the drone
    def arm(self, master):
        master.arducopter_arm()

    #Disarms the drone
    def disarm(self, master):
        master.arducopter_disarm()

    #send takeoff command to the drone
    def takeoff(self, master, altitude):
        try:
            master.mav.command_long_send(
                master.target_system,
                master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                0,
                0, 0, 0, 0, 0, 0,
                altitude
            )
        except Exception as e:
            logging.error(f"Error sending takeoff command: {e}")
    
    #send land command to the drone
    def land(self, master):
        try:
            master.mav.command_long_send(
                master.target_system,
                master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_LAND,
                0,
                0, 0, 0, 0, 0, 0, 0
            )
        except Exception as e:
            logging.error(f"Error sending land command: {e}")

    #send set yaw command to the drone
    def set_yaw_rate (self, master, yaw_rate : float):
        try:
            master.mav.command_long_send(
                master.target_system,
                master.target_component,
                mavutil.mavlink.MAV_CMD_CONDITION_YAW,
                0, 0, yaw_rate, 1, 1, 0, 0
            )
        except Exception as e:
            logging.error(f"Error sending set yaw rate command: {e}")
    
    #Set the forward speed of the drone
    def set_forward_speed(self, master, speed : float):
        try:
            
            #mask so only the speed is set, and not the other parameters
            type_mask = 0b0000110111000111

            master.mav.set_position_target_local_ned_send(
                0,
                master.target_system,
                master.target_component,
                mavutil.mavlink.MAV_FRAME_BODY_NED,
                type_mask,
                0, 0, 0, speed, 0.0, 0.0, 0, 0
            )
        except Exception as e:
            logging.error(f"Error sending set forward speed command: {e}")
    
    #Send the return to launch command to the drone
    def rtl(self, master):
        try:
            master.mav.command_long_send(
                master.target_system,
                master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
                0, 0, 0, 0, 0, 0, 0
            )
        except Exception as e:
            logging.error(f"Error sending RTL command: {e}")

