"""Drone scheduling logic for the Fly-in project."""

from models.zone import Zone


class Scheduler:
    """Assign drones to candidate paths."""

    def assign_paths(
        self,
        nb_drones: int,
        paths: list[list[Zone]],
    ) -> dict[int, list[Zone]]:
        """Assign each drone to one available path."""

        if not paths:
            raise ValueError("No paths available")

        assignments: dict[int, list[Zone]] = {}

        for drone_id in range(1, nb_drones + 1):
            path_index = (drone_id - 1) % len(paths)
            assignments[drone_id] = paths[path_index]

        return assignments
