from unittest.mock import MagicMock
import pytest
from pymavlink import mavutil

from mavlink.commands import Command

# Anta at klassen din ligger i en fil som heter 'commands.py'
# from commands import Command

@pytest.fixture
def mock_master():
    """Lager et falskt 'master'-objekt som simulerer MAVLink-tilkoblingen."""
    master = MagicMock()
    master.target_system = 1
    master.target_component = 1
    return master

@pytest.fixture
def cmd():
    """Returnerer en instans av Command-klassen."""
    return Command()


def test_arm(cmd, mock_master):
    cmd.arm(mock_master)
    mock_master.arducopter_arm.assert_called_once()


def test_disarm(cmd, mock_master):
    cmd.disarm(mock_master)
    mock_master.arducopter_disarm.assert_called_once()


def test_takeoff(cmd, mock_master):
    altitude = 10.0
    cmd.takeoff(mock_master, altitude)
    
    # Sjekk at command_long_send ble kalt med riktige parametere for Takeoff
    mock_master.mav.command_long_send.assert_called_once_with(
        1, 1,  # target_system, target_component
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,     # confirmation
        0, 0, 0, 0, 0, 0,  # param 1-6
        altitude           # param 7 (høyde)
    )


def test_land(cmd, mock_master):
    cmd.land(mock_master)
    mock_master.mav.command_long_send.assert_called_once()
    # Du kan også sjekke at MAV_CMD_NAV_LAND ble brukt
    args, _ = mock_master.mav.command_long_send.call_args
    assert args[2] == mavutil.mavlink.MAV_CMD_NAV_LAND


def test_set_forward_speed(cmd, mock_master):
    speed = 5.0
    cmd.set_forward_speed(mock_master, speed)
    
    # Sjekk at set_position_target_local_ned_send ble kalt
    mock_master.mav.set_position_target_local_ned_send.assert_called_once()
    args, _ = mock_master.mav.set_position_target_local_ned_send.call_args
    
    # args[3] er rammeverk (MAV_FRAME_BODY_NED) og args[5] er selve hastigheten (vx)
    assert args[3] == mavutil.mavlink.MAV_FRAME_BODY_NED
    assert args[8] == speed