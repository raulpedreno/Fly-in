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

            for drone in self.drones: ## un turno para todos los drones
                if drone.is_delivered:
                    continue

                path = self.assignments[drone.drone_id]
                current_index = self.positions[drone.drone_id]

                if current_index + 1 >= len(path):
                    drone.is_delivered = True
                    continue

                next_index = current_index + 1
                next_zone = path[next_index]

                is_end_zone = next_zone == path[-1]

                if not is_end_zone:
                    current_entries = planned_entries.get(next_zone.name, 0)

                    if current_entries >= next_zone.max_drones:
                        continue

                    planned_entries[next_zone.name] = current_entries + 1

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