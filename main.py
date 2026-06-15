"""Main entry point for the Fly-in project."""

from models.connection import Connection
from models.graph import Graph
from models.zone import Zone
from parser.parser import Parser
from algorithms.pathfinder import Pathfinder


def main() -> None:
    """Run a temporary model test."""
    graph = Graph()

    parsero = Parser("map.txt")
    graph = parsero.parse()
    
    print("--------------------------------")

    start = graph.start_zone
    end = graph.end_zone
    pathfinder = Pathfinder(graph)
    path = pathfinder.find_path(start, end)

    print (path)
if __name__ == "__main__":
    main()