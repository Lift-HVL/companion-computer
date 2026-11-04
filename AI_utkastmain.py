
  import time

  from mavlink.vehicle_state import VehicleState
  from fsm.controller import FSM
  from fsm.event_generator import EventGenerator


  # Delane main eig og koplar saman
  vehicle = VehicleState()
  fsm = FSM()
  event_generator = EventGenerator()


  def process_tick(
      now: float,
      key: str | None = None,
      detection=None,
  ) -> None:
      """Køyr éin simulert runde av main-loopen."""

      previous_state = fsm.state

      event = event_generator.generate(
          state=fsm.state,
          vehicle=vehicle,
          detection=detection,
          key=key,
          now=now,
      )

      if event is not None:
          fsm.handle(event)

      print(
          f"event={event.name if event else 'None'}, "
          f"state={previous_state.name} -> {fsm.state.name}, "
          f"armed={vehicle.armed}"
      )


  print("Start:")
  print(vehicle)
  print(f"FSM state: {fsm.state.name}")


  # --------------------------------------------------
  # Runde 1: Simuler heartbeat frå ArduPilot
  # --------------------------------------------------

  now = time.monotonic()

  vehicle.connected = True
  vehicle.last_heartbeat_time = now
  vehicle.armed = False
  vehicle.mode = "STABILIZE"

  process_tick(now)

  # Forventa:
  # INIT_OK og BOOT -> STANDBY


  # --------------------------------------------------
  # Runde 2: Simuler at ArduPilot har armed drona
  # --------------------------------------------------

  now = time.monotonic()

  vehicle.last_heartbeat_time = now
  vehicle.armed = True
  vehicle.mode = "GUIDED"

  process_tick(now)

  # Forventa:
  # ARMED og STANDBY -> ARMED


  # --------------------------------------------------
  # Runde 3: Simuler at drona er klar for takeoff
  # --------------------------------------------------

  now = time.monotonic()

  vehicle.last_heartbeat_time = now
  vehicle.gps_ok = True
  vehicle.ekf_ok = True
  vehicle.satellites_visible = 10
  vehicle.battery_remaining_pct = 80

  process_tick(now, key="t")

  # Forventa:
  # TAKEOFF og ARMED -> TAKEOFF