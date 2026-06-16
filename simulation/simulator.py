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
        } ##dron_id - indice_ruta

    def run(self) -> list[str]:
        """Run the simulation.

        Returns:
            A list of output lines, one per turn.
        """
        output: list[str] = []

        while not all(drone.is_delivered for drone in self.drones):
            turn_moves: list[str] = []
            planned_entries: dict[str, int] = {}
            planned_connections: dict[str, int] = {}

            for drone in self.drones: ## un turno para todos los drones
                if drone.is_delivered:
                    continue

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

                    continue ##!!!

                path = self.assignments[drone.drone_id]
                current_index = self.positions[drone.drone_id]

                if current_index + 1 >= len(path):
                    drone.is_delivered = True
                    continue

## check conexion.max_link_capacity
                next_index = current_index + 1
                next_zone = path[next_index]

                current_zone = path[current_index]
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
                    continue

                planned_connections[connection_key] = (
                    current_connection_entries + 1
                )
## zone.max_drones
                is_end_zone = next_zone == path[-1]

                if not is_end_zone:
                    current_entries = planned_entries.get(next_zone.name, 0)

                    if current_entries >= next_zone.max_drones:
                        continue

                    planned_entries[next_zone.name] = current_entries + 1

## si la zona es restricted...
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