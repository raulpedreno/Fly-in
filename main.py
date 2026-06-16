"""Main entry point for the Fly-in project."""

from models.connection import Connection
from models.graph import Graph
from models.zone import Zone
from parser.parser import Parser
from algorithms.pathfinder import Pathfinder
from models.drone import Drone
from simulation.simulator import Simulator

def main() -> None:
    """Run a temporary model test."""
    start = Zone("start", 0, 0)
    restricted = Zone("restricted", 1, 0, zone_type="restricted")
    end = Zone("end", 2, 0)

    graph = Graph()
    graph.add_zone(start)
    graph.add_zone(restricted)
    graph.add_zone(end)
    graph.add_connection(Connection(start, restricted))
    graph.add_connection(Connection(restricted, end))

    drone = Drone(1, start)
    path = [start, restricted, end]

    simulator = Simulator(
        graph=graph,
        drones=[drone],
        assignments={1: path},
    )

    output = simulator.run()

    print(output)
if __name__ == "__main__":
    main()