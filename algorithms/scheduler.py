"""Drone scheduling logic for the Fly-in project."""

from models.zone import Zone
from models.graph import Graph


class Scheduler:
    """Assign drones to candidate paths."""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def _get_first_connection_capacity(self, path: list[Zone]) -> int:
        """Return the capacity of the first connection in a path.

        Args:
            path: Path to evaluate.

        Returns:
            Capacity of the first connection.
        """
        if len(path) < 2:
            return 1

        connection = self.graph.get_connection(path[0], path[1])
        return connection.max_link_capacity

    def _get_path_cost(self, path: list[Zone]) -> int:
        """Return an estimated path cost."""
        total_cost = 0

        for zone in path[1:]:
            if zone.zone_type == "restricted":
                total_cost += 2
            else:
                total_cost += 1

        return total_cost

    def assign_paths(
        self,
        nb_drones: int,
        paths: list[list[Zone]],
    ) -> dict[int, list[Zone]]:
        """Assign each drone to one available path."""

        if nb_drones < 1:
            raise ValueError("nb_drones must be greater than 0")

        if not paths:
            raise ValueError("No paths available")

        assignments: dict[int, list[Zone]] = {}

        path_loads = [0 for _ in paths]

        for drone_id in range(1, nb_drones + 1):
            best_path_index = min(
                range(len(paths)),
                key=lambda index: (
                    self._get_path_cost(paths[index])
                    + path_loads[index] // self._get_first_connection_capacity(paths[index])
                ),)
##Elige la ruta cuyo coste total = (longitud de la ruta) + (número de drones ya asignados a esa ruta) sea el menor // mwx_link_capacity.

            assignments[drone_id] = paths[best_path_index]
            path_loads[best_path_index] += 1

        return assignments
