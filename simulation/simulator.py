"""Simulation engine for the Fly-in project."""

from models.drone import Drone
from models.zone import Zone
from models.graph import Graph


class Simulator:
    """Run a basic drone movement simulation."""

    def __init__(
        self,
        graph: Graph,
        drones: list[Drone],
        assignments: dict[int, list[Zone]]
    ) -> None:
        self.graph = graph
        self.drones = drones
        self.assignments = assignments
        self.positions: dict[int, int] = {
            drone.drone_id: 0 for drone in drones
        }  # dron_id - indice_ruta
        self.max_turns = 10000

    def _get_zone_occupancy(self) -> dict[str, int]:
        """Return current zone occupancy."""

        occupancy: dict[str, int] = {}

        for drone in self.drones:
            if drone.is_delivered:
                continue

            if drone.in_transit_to is not None:
                continue

            zone_name = drone.current_zone.name
            occupancy[zone_name] = occupancy.get(zone_name, 0) + 1

        return occupancy

    def _validate_zone_occupancy(self) -> None:
        """Validate that no zone exceeds its capacity.

        Raises:
            ValueError: If a zone exceeds its capacity.
        """
        occupancy = self._get_zone_occupancy()

        for zone_name, count in occupancy.items():
            zone = self.graph.get_zone(zone_name)

            if zone == self.graph.start_zone:
                continue

            if zone == self.graph.end_zone:
                continue

            if count > zone.max_drones:
                raise ValueError(
                    f"Zone {zone.name} exceeds capacity"
                )

    def _validate_assignments(self) -> None:
        """Validate drone path assignments.

        Raises:
            ValueError: If an assignment is missing or invalid.
        """
        for drone in self.drones:
            if drone.drone_id not in self.assignments:
                raise ValueError(
                    f"Missing assignment for drone D{drone.drone_id}"
                )

            path = self.assignments[drone.drone_id]

            if len(path) < 2:
                raise ValueError(
                    f"Invalid path for drone D{drone.drone_id}"
                )

            if path[0] != drone.current_zone:
                raise ValueError(
                    f"Path for drone D{drone.drone_id} "
                    "does not start at current zone"
                )

            if path[-1] != self.graph.end_zone:
                raise ValueError(
                    f"Path for drone D{drone.drone_id} "
                    "does not end at end zone"
                )

    def run(self) -> list[str]:
        """Run the simulation.

        Returns:
            A list of output lines, one per turn.
        """
        self._validate_zone_occupancy()
        self._validate_assignments()
        output: list[str] = []

        turns = 0

        while not all(drone.is_delivered for drone in self.drones):
            turn_count += 1

            if turn_count > self.max_turns:
                raise ValueError("Simulation exceeded maximum turns")

            turn_moves: list[str] = []
            zone_occupancy = self._get_zone_occupancy()
            planned_entries: dict[str, int] = {}
            planned_exits: dict[str, int] = {}
            planned_connections: dict[str, int] = {}

            for drone in self.drones:  # un turno para todos los drones
                if drone.is_delivered:
                    continue

## drones en transito:-----------------------------------------------------------------------
                if drone.in_transit_to is not None:
                    drone.remaining_turns -= 1

                    if drone.remaining_turns == 0:
                        self.positions[drone.drone_id] += 1
                        drone.current_zone = drone.in_transit_to
                        turn_moves.append(
                            f"D{drone.drone_id}-{drone.current_zone.name}"
                        )
                        drone.in_transit_to = None

                        if drone.current_zone == self.assignments[
                            drone.drone_id
                        ][-1]:
                            drone.is_delivered = True
                    else:
                        turn_moves.append(
                            f"D{drone.drone_id}-"
                            f"{drone.current_zone.name}-"
                            f"{drone.in_transit_to.name}"
                        )

                    continue  # !!!

## preparacion del movimiento----------------------------------------------------------------
                path = self.assignments[drone.drone_id]
                current_index = self.positions[drone.drone_id]

                if current_index + 1 >= len(path):
                    drone.is_delivered = True
                    continue

                next_index = current_index + 1
                next_zone = path[next_index]
                current_zone = path[current_index]

## comprobar capacidad de conexión------------------------------------------------------------
                planned_exits[current_zone.name] = (
                    planned_exits.get(current_zone.name, 0) + 1
                )

                connection = self.graph.get_connection(
                    current_zone,
                    next_zone,
                )
                connection_key = (
                    f"{connection.zone_a.name}-{connection.zone_b.name}"
                )

                current_connection_entries = planned_connections.get(
                    connection_key,
                    0,
                )

                if (
                    current_connection_entries
                    >= connection.max_link_capacity
                ):
                    planned_exits[current_zone.name] -= 1
                    continue

                planned_connections[connection_key] = (
                    current_connection_entries + 1
                )

# comprobar capacidad de la zona destino-----------------------------------------------------
                is_end_zone = next_zone == path[-1]

                if not is_end_zone:
                    current_occupancy = zone_occupancy.get(next_zone.name, 0)
                    exits_from_zone = planned_exits.get(next_zone.name, 0)
                    entries_to_zone = planned_entries.get(next_zone.name, 0)

                    expected_occupancy = (
                        current_occupancy
                        - exits_from_zone
                        + entries_to_zone
                    )

                    if expected_occupancy >= next_zone.max_drones:
                        planned_exits[current_zone.name] -= 1
                        continue

                    planned_entries[next_zone.name] = entries_to_zone + 1

# ejecutar el movimiento (normal vs restricted)------------------------------------------------.
                if next_zone.zone_type == "restricted":
                    drone.in_transit_to = next_zone
                    drone.remaining_turns = 1

                    turn_moves.append(
                        f"D{drone.drone_id}-"
                        f"{current_zone.name}-{next_zone.name}"
                    )
                else:
                    self.positions[drone.drone_id] = next_index
                    drone.current_zone = next_zone

                    turn_moves.append(
                        f"D{drone.drone_id}-{next_zone.name}"
                    )

                    if next_zone == path[-1]:
                        drone.is_delivered = True

            if turn_moves:
                output.append(" ".join(turn_moves))

        return output
