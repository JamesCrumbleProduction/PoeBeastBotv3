from .helpers import (
    build_beasts_statuses,
    build_machine_statuses,
    get_extended_mode_status,
    wait_monitoring_server_connection
)

wait_monitoring_server_connection()

MachineStatus = build_machine_statuses()
BEASTS_STATUSES: dict[str, MachineStatus] = build_beasts_statuses(
    MachineStatus
)
EXTENDED_MODE: bool = get_extended_mode_status()
