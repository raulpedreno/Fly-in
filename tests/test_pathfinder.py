"""Tests for the Pathfinder."""

import pytest

from algorithms.pathfinder import Pathfinder
from models.connection import Connection
from models.graph import Graph
from models.zone import Zone


def test_find_simple_path() -> None:
    """Test finding a simple path."""
    graph = Graph()
    start = Zone("start", 0, 0)
    end = Zone("end", 2, 2)

    graph.add_zone(start)
    graph.add_zone(end)
    graph.add_connection(Connection(start, end))

    pathfinder = Pathfinder(graph)
    path = pathfinder.find_path(start, end)

    assert path == [start, end]


def test_find_path_avoids_blocked_zone() -> None:
    """Test that blocked zones are ignored."""
    graph = Graph()
    start = Zone("start", 0, 0)
    blocked = Zone("blocked", 1, 1, zone_type="blocked")
    end = Zone("end", 2, 2)

    graph.add_zone(start)
    graph.add_zone(blocked)
    graph.add_zone(end)

    graph.add_connection(Connection(start, blocked))
    graph.add_connection(Connection(blocked, end))

    pathfinder = Pathfinder(graph)

    with pytest.raises(ValueError):
        pathfinder.find_path(start, end)


def test_find_path_with_alternative_route() -> None:
    """Test finding an alternative route around a blocked zone."""
    graph = Graph()
    start = Zone("start", 0, 0)
    blocked = Zone("blocked", 1, 1, zone_type="blocked")
    alternative = Zone("alternative", 1, 0)
    end = Zone("end", 2, 2)

    graph.add_zone(start)
    graph.add_zone(blocked)
    graph.add_zone(alternative)
    graph.add_zone(end)

    graph.add_connection(Connection(start, blocked))
    graph.add_connection(Connection(blocked, end))
    graph.add_connection(Connection(start, alternative))
    graph.add_connection(Connection(alternative, end))

    pathfinder = Pathfinder(graph)
    path = pathfinder.find_path(start, end)

    assert path == [start, alternative, end]


def test_find_path_without_solution_raises_error() -> None:
    """Test that no path raises an error."""
    graph = Graph()
    start = Zone("start", 0, 0)
    end = Zone("end", 2, 2)

    graph.add_zone(start)
    graph.add_zone(end)

    pathfinder = Pathfinder(graph)

    with pytest.raises(ValueError):
        pathfinder.find_path(start, end)


def test_movement_cost_normal_zone() -> None:
    """Test movement cost for a normal zone."""
    graph = Graph()
    pathfinder = Pathfinder(graph)
    zone = Zone("A", 0, 0, zone_type="normal")

    assert pathfinder.get_movement_cost(zone) == 1


def test_movement_cost_priority_zone() -> None:
    """Test movement cost for a priority zone."""
    graph = Graph()
    pathfinder = Pathfinder(graph)
    zone = Zone("A", 0, 0, zone_type="priority")

    assert pathfinder.get_movement_cost(zone) == 1


def test_movement_cost_restricted_zone() -> None:
    """Test movement cost for a restricted zone."""
    graph = Graph()
    pathfinder = Pathfinder(graph)
    zone = Zone("A", 0, 0, zone_type="restricted")

    assert pathfinder.get_movement_cost(zone) == 2


def test_movement_cost_blocked_zone_raises_error() -> None:
    """Test movement cost for a blocked zone."""
    graph = Graph()
    pathfinder = Pathfinder(graph)
    zone = Zone("A", 0, 0, zone_type="blocked")

    with pytest.raises(ValueError):
        pathfinder.get_movement_cost(zone)


def test_dijkstra_prefers_lower_cost_path() -> None:
    """Test that Dijkstra prefers a longer but cheaper path."""
    graph = Graph()

    start = Zone("start", 0, 0)
    restricted_a = Zone("restricted_a", 1, 1, zone_type="restricted")
    restricted_b = Zone("restricted_b", 2, 1, zone_type="restricted")
    normal_a = Zone("normal_a", 1, 0)
    normal_b = Zone("normal_b", 2, 0)
    end = Zone("end", 3, 0)

    graph.add_zone(start)
    graph.add_zone(restricted_a)
    graph.add_zone(restricted_b)
    graph.add_zone(normal_a)
    graph.add_zone(normal_b)
    graph.add_zone(end)

    graph.add_connection(Connection(start, restricted_a))
    graph.add_connection(Connection(restricted_a, restricted_b))
    graph.add_connection(Connection(restricted_b, end))

    graph.add_connection(Connection(start, normal_a))
    graph.add_connection(Connection(normal_a, normal_b))
    graph.add_connection(Connection(normal_b, end))

    pathfinder = Pathfinder(graph)
    path = pathfinder.find_path(start, end)

    assert path == [start, normal_a, normal_b, end]


def test_dijkstra_prefers_priority_zone_on_cost_tie() -> None:
    """Test that priority zones are preferred when total cost ties."""
    graph = Graph()

    start = Zone("start", 0, 0)
    priority = Zone("priority", 1, 0, zone_type="priority")
    normal = Zone("normal", 1, 1)
    end = Zone("end", 2, 0)

    graph.add_zone(start)
    graph.add_zone(priority)
    graph.add_zone(normal)
    graph.add_zone(end)

    graph.add_connection(Connection(start, priority))
    graph.add_connection(Connection(priority, end))

    graph.add_connection(Connection(start, normal))
    graph.add_connection(Connection(normal, end))

    pathfinder = Pathfinder(graph)
    path = pathfinder.find_path(start, end)

    assert path == [start, priority, end]


def test_find_all_paths_returns_multiple_paths() -> None:
    """Test finding multiple paths."""
    graph = Graph()

    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0)
    b = Zone("B", 1, 1)
    end = Zone("end", 2, 0)

    graph.add_zone(start)
    graph.add_zone(a)
    graph.add_zone(b)
    graph.add_zone(end)

    graph.add_connection(Connection(start, a))
    graph.add_connection(Connection(a, end))

    graph.add_connection(Connection(start, b))
    graph.add_connection(Connection(b, end))

    pathfinder = Pathfinder(graph)
    paths = pathfinder.find_all_paths(start, end)

    assert len(paths) == 2
    assert [start, a, end] in paths
    assert [start, b, end] in paths


def test_find_all_paths_ignores_blocked_zones() -> None:
    """Test that all paths ignore blocked zones."""
    graph = Graph()

    start = Zone("start", 0, 0)
    blocked = Zone("blocked", 1, 0, zone_type="blocked")
    end = Zone("end", 2, 0)

    graph.add_zone(start)
    graph.add_zone(blocked)
    graph.add_zone(end)

    graph.add_connection(Connection(start, blocked))
    graph.add_connection(Connection(blocked, end))

    pathfinder = Pathfinder(graph)
    paths = pathfinder.find_all_paths(start, end)

    assert paths == []


def test_get_path_cost() -> None:
    """Test total path cost calculation."""
    graph = Graph()
    pathfinder = Pathfinder(graph)

    start = Zone("start", 0, 0)
    normal = Zone("normal", 1, 0)
    restricted = Zone("restricted", 2, 0, zone_type="restricted")
    end = Zone("end", 3, 0)

    path = [start, normal, restricted, end]

    assert pathfinder.get_path_cost(path) == 4


def test_find_all_paths_returns_sorted_by_cost() -> None:
    """Test that all paths are sorted by total cost."""
    graph = Graph()

    start = Zone("start", 0, 0)
    restricted_a = Zone("restricted_a", 1, 0, zone_type="restricted")
    restricted_b = Zone("restricted_b", 2, 0, zone_type="restricted")
    normal_a = Zone("normal_a", 1, 1)
    normal_b = Zone("normal_b", 2, 1)
    end = Zone("end", 3, 0)

    graph.add_zone(start)
    graph.add_zone(restricted_a)
    graph.add_zone(restricted_b)
    graph.add_zone(normal_a)
    graph.add_zone(normal_b)
    graph.add_zone(end)

    graph.add_connection(Connection(start, restricted_a))
    graph.add_connection(Connection(restricted_a, restricted_b))
    graph.add_connection(Connection(restricted_b, end))

    graph.add_connection(Connection(start, normal_a))
    graph.add_connection(Connection(normal_a, normal_b))
    graph.add_connection(Connection(normal_b, end))

    pathfinder = Pathfinder(graph)
    paths = pathfinder.find_all_paths(start, end)

    assert paths[0] == [start, normal_a, normal_b, end]
    assert paths[1] == [start, restricted_a, restricted_b, end]
