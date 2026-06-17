"""Main entry point for the Fly-in project."""

import sys
from algorithms.pathfinder import Pathfinder
from algorithms.scheduler import Scheduler
from models.drone import Drone
from parser.parser import Parser
from simulation.simulator import Simulator
from visualization.terminal_view import TerminalView


def main() -> None:
    """Run the Fly-in simulation."""

    if len(sys.argv) != 2:
        raise ValueError("Usage: python3 main.py <map_file>")

    parser = Parser(sys.argv[1])
    graph = parser.parse()

    if graph.start_zone is None or graph.end_zone is None:
        raise ValueError("Graph must have start and end zones")

    pathfinder = Pathfinder(graph)
    paths = pathfinder.find_all_paths(
        graph.start_zone,
        graph.end_zone,
    )

    scheduler = Scheduler(graph)
    assignments = scheduler.assign_paths(
        graph.nb_drones,
        paths,
    )

    drones = [
        Drone(drone_id, graph.start_zone)
        for drone_id in range(1, graph.nb_drones + 1)
    ]

    simulator = Simulator(
        graph=graph,
        drones=drones,
        assignments=assignments,
    )

    turns = simulator.run()

    view = TerminalView()
    view.display_turns(turns)


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)
