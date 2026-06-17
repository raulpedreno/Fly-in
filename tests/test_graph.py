"""Tests for the Graph model."""

import pytest

from models.graph import Graph
from models.zone import Zone
from models.connection import Connection


def test_add_zone() -> None:
    """Test that a zone can be added to the graph."""
    graph = Graph()
    zone = Zone("A", 0, 0)

    graph.add_zone(zone)

    assert graph.zones["A"] == zone


def test_get_zone() -> None:
    """Test that a zone can be retrieved by name."""
    graph = Graph()
    zone = Zone("A", 0, 0)

    graph.add_zone(zone)

    assert graph.get_zone("A") == zone


def test_get_unknown_zone_raises_error() -> None:
    """Test that getting an unknown zone raises an error."""
    graph = Graph()

    with pytest.raises(ValueError):
        graph.get_zone("Unknown")


def test_duplicate_zone_raises_error() -> None:
    """Test that duplicate zone names are rejected."""
    graph = Graph()

    graph.add_zone(Zone("A", 0, 0))

    with pytest.raises(ValueError):
        graph.add_zone(Zone("A", 1, 1))


def test_add_connection() -> None:
    """Test that a connection can be added to the graph."""
    graph = Graph()
    zone_a = Zone("A", 0, 0)
    zone_b = Zone("B", 1, 1)

    graph.add_zone(zone_a)
    graph.add_zone(zone_b)

    connection = Connection(zone_a, zone_b)
    graph.add_connection(connection)

    assert graph.connections == [connection]


def test_duplicate_connection_same_direction_raises_error() -> None:
    """Test that duplicate connections in same direction are rejected."""
    graph = Graph()
    zone_a = Zone("A", 0, 0)
    zone_b = Zone("B", 1, 1)

    graph.add_zone(zone_a)
    graph.add_zone(zone_b)

    graph.add_connection(Connection(zone_a, zone_b))

    with pytest.raises(ValueError):
        graph.add_connection(Connection(zone_a, zone_b))


def test_duplicate_connection_opposite_direction_raises_error() -> None:
    """Test that duplicate bidirectional connections are rejected."""
    graph = Graph()
    zone_a = Zone("A", 0, 0)
    zone_b = Zone("B", 1, 1)

    graph.add_zone(zone_a)
    graph.add_zone(zone_b)

    graph.add_connection(Connection(zone_a, zone_b))

    with pytest.raises(ValueError):
        graph.add_connection(Connection(zone_b, zone_a))


def test_get_neighbors() -> None:
    """Test that graph returns adjacent zones."""
    graph = Graph()
    zone_a = Zone("A", 0, 0)
    zone_b = Zone("B", 1, 1)
    zone_c = Zone("C", 2, 2)

    graph.add_zone(zone_a)
    graph.add_zone(zone_b)
    graph.add_zone(zone_c)

    graph.add_connection(Connection(zone_a, zone_b))
    graph.add_connection(Connection(zone_a, zone_c))

    neighbors = graph.get_neighbors(zone_a)

    assert zone_b in neighbors
    assert zone_c in neighbors
    assert len(neighbors) == 2


def test_get_neighbors_bidirectional() -> None:
    """Test that connections work in both directions."""
    graph = Graph()
    zone_a = Zone("A", 0, 0)
    zone_b = Zone("B", 1, 1)

    graph.add_zone(zone_a)
    graph.add_zone(zone_b)
    graph.add_connection(Connection(zone_a, zone_b))

    neighbors = graph.get_neighbors(zone_b)

    assert neighbors == [zone_a]


def test_set_start_zone() -> None:
    """Test that the start zone can be set."""
    graph = Graph()
    start = Zone("start", 0, 0)

    graph.set_start_zone(start)

    assert graph.start_zone == start
    assert graph.zones["start"] == start


def test_set_end_zone() -> None:
    """Test that the end zone can be set."""
    graph = Graph()
    end = Zone("end", 10, 10)

    graph.set_end_zone(end)

    assert graph.end_zone == end
    assert graph.zones["end"] == end


def test_duplicate_start_zone_raises_error() -> None:
    """Test that only one start zone can exist."""
    graph = Graph()

    graph.set_start_zone(Zone("start", 0, 0))

    with pytest.raises(ValueError):
        graph.set_start_zone(Zone("other_start", 1, 1))


def test_duplicate_end_zone_raises_error() -> None:
    """Test that only one end zone can exist."""
    graph = Graph()

    graph.set_end_zone(Zone("end", 10, 10))

    with pytest.raises(ValueError):
        graph.set_end_zone(Zone("other_end", 11, 11))


def test_validate_valid_graph() -> None:
    """Test that a complete graph is valid."""
    graph = Graph()
    start = Zone("start", 0, 0)
    end = Zone("end", 10, 10)

    graph.set_nb_drones(1)
    graph.set_start_zone(start)
    graph.set_end_zone(end)
    graph.add_connection(Connection(start, end))

    graph.validate()


def test_validate_without_drones_raises_error() -> None:
    """Test that graph without drones is invalid."""
    graph = Graph()

    with pytest.raises(ValueError):
        graph.validate()


def test_validate_without_start_raises_error() -> None:
    """Test that graph without start zone is invalid."""
    graph = Graph()
    end = Zone("end", 10, 10)

    graph.set_nb_drones(1)
    graph.set_end_zone(end)

    with pytest.raises(ValueError):
        graph.validate()


def test_validate_without_end_raises_error() -> None:
    """Test that graph without end zone is invalid."""
    graph = Graph()
    start = Zone("start", 0, 0)

    graph.set_nb_drones(1)
    graph.set_start_zone(start)

    with pytest.raises(ValueError):
        graph.validate()


def test_validate_without_connections_raises_error() -> None:
    """Test that graph without connections is invalid."""
    graph = Graph()
    start = Zone("start", 0, 0)
    end = Zone("end", 10, 10)

    graph.set_nb_drones(1)
    graph.set_start_zone(start)
    graph.set_end_zone(end)

    with pytest.raises(ValueError):
        graph.validate()


def test_get_connection() -> None:
    """Test that a connection can be retrieved."""
    graph = Graph()
    zone_a = Zone("A", 0, 0)
    zone_b = Zone("B", 1, 1)

    graph.add_zone(zone_a)
    graph.add_zone(zone_b)

    connection = Connection(zone_a, zone_b)
    graph.add_connection(connection)

    assert graph.get_connection(zone_a, zone_b) == connection


def test_get_connection_bidirectional() -> None:
    """Test that a connection can be retrieved bidirectionally."""
    graph = Graph()
    zone_a = Zone("A", 0, 0)
    zone_b = Zone("B", 1, 1)

    graph.add_zone(zone_a)
    graph.add_zone(zone_b)

    connection = Connection(zone_a, zone_b)
    graph.add_connection(connection)

    assert graph.get_connection(zone_b, zone_a) == connection


def test_get_connection_unknown_raises_error() -> None:
    """Test that missing connection raises an error."""
    graph = Graph()
    zone_a = Zone("A", 0, 0)
    zone_b = Zone("B", 1, 1)

    graph.add_zone(zone_a)
    graph.add_zone(zone_b)

    with pytest.raises(ValueError):
        graph.get_connection(zone_a, zone_b)
