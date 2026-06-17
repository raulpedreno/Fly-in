"""Pathfinding algorithms for the Fly-in project."""

import heapq

from models.graph import Graph
from models.zone import Zone


class Pathfinder:
    """Find paths inside a graph."""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def find_path(self, start: Zone, end: Zone) -> list[Zone]:
        """Find the lowest-cost path between two zones using Dijkstra."""

        queue: list[tuple[int, int, int, Zone, list[Zone]]] = []
        visited: set[str] = set()
        counter = 0

        heapq.heappush(queue, (0, 0, counter, start, [start]))

        while queue:
            current_cost, _, _, current_zone, path = heapq.heappop(queue)

            if current_zone.name in visited:
                continue

            visited.add(current_zone.name)

            if current_zone.name == end.name:
                return path

            for neighbor in self.graph.get_neighbors(current_zone):
                if neighbor.name in visited:
                    continue

                try:
                    movement_cost = self.get_movement_cost(neighbor)
                except ValueError:
                    continue

                counter += 1
                priority_penalty = 0 if neighbor.zone_type == "priority" else 1
                heapq.heappush(
                    queue,
                    (
                        current_cost + movement_cost,
                        priority_penalty,
                        counter,
                        neighbor,
                        path + [neighbor],
                    ),
                )

        raise ValueError("No path found")

    def get_movement_cost(self, zone: Zone) -> int:
        """Return the movement cost to enter a zone."""

        if zone.zone_type == "blocked":
            raise ValueError("Cannot move into a blocked zone")

        if zone.zone_type == "restricted":
            return 2

        return 1

    def find_all_paths(
        self,
        start: Zone,
        end: Zone,
        max_paths: int = 10,
    ) -> list[list[Zone]]:
        """Find multiple valid paths between two zones."""

        paths: list[list[Zone]] = []
        stack: list[list[Zone]] = [[start]]

        while stack and len(paths) < max_paths:
            path = stack.pop()
            current_zone = path[-1]

            if current_zone.name == end.name:
                paths.append(path)
                continue

            for neighbor in self.graph.get_neighbors(current_zone):
                if neighbor.name in {zone.name for zone in path}:
                    continue

                if neighbor.zone_type == "blocked":
                    continue

                stack.append(path + [neighbor])

        return sorted(paths, key=self.get_path_cost)

    def get_path_cost(self, path: list[Zone]) -> int:
        """Return the total movement cost of a path."""

        total_cost = 0

        for zone in path[1:]:
            total_cost += self.get_movement_cost(zone)

        return total_cost
