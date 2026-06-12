"""Main entry point for the Fly-in project."""

from models.connection import Connection
from models.graph import Graph
from models.zone import Zone
from parser.parser import Parser


def main() -> None:
    """Run a temporary model test."""
    graph = Graph()

    start = Zone("start", 0, 0)
    end = Zone("end", 10, 10)

    graph.set_start_zone(start)
    graph.set_end_zone(end)
    graph.add_connection(Connection(start, end))

    ##graph.validate()

    print(graph.zones)
    print(graph.connections)
    print("Graph is valid!")

    parsero = Parser("map.txt")
    graph = parsero.parse()
    
    print(f"{graph.zones}")


if __name__ == "__main__":
    main()