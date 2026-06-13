"""Main entry point for the Fly-in project."""

from models.connection import Connection
from models.graph import Graph
from models.zone import Zone
from parser.parser import Parser


def main() -> None:
    """Run a temporary model test."""
    graph = Graph()

    parsero = Parser("map.txt")
    graph = parsero.parse()
    
    print(f"{graph.zones}")
    print(f"{graph.connections}")


if __name__ == "__main__":
    main()