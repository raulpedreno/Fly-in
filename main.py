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
    a = Zone("A", 1, 0)
    end = Zone("end", 2, 0)

    drones = [
        Drone(1, start),
        Drone(2, start),
    ]

    path = [start, a, end]

    simulator = Simulator(
        drones=drones,
        assignments={
            1: path,
            2: path,
        },
    )

    output = simulator.run()

    print(output)
if __name__ == "__main__":
    main()