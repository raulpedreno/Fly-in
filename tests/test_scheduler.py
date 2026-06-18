"""Tests for the Scheduler."""

import pytest

from algorithms.scheduler import Scheduler
from models.zone import Zone
from models.graph import Graph
from models.connection import Connection
from algorithms.pathfinder import Pathfinder


def test_assign_paths_invalid_nb_drones_raises_error() -> None:
    """Test that invalid drone count raises an error."""
    graph = Graph()
    scheduler = Scheduler(graph)

    start = Zone("start", 0, 0)
    end = Zone("end", 1, 0)
    path = [start, end]

    with pytest.raises(ValueError):
        scheduler.assign_paths(0, [path])


def test_scheduler_get_path_cost_normal_path() -> None:
    """Test scheduler path cost with normal zones."""
    graph = Graph()
    scheduler = Scheduler(graph)

    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0)
    end = Zone("end", 2, 0)

    path = [start, a, end]

    assert scheduler._get_path_cost(path) == 2


def test_scheduler_get_path_cost_with_restricted_zone() -> None:
    """Test scheduler path cost with restricted zone."""
    graph = Graph()
    scheduler = Scheduler(graph)

    start = Zone("start", 0, 0)
    restricted = Zone("restricted", 1, 0, zone_type="restricted")
    end = Zone("end", 2, 0)

    path = [start, restricted, end]

    assert scheduler._get_path_cost(path) == 3


def test_scheduler_get_path_cost_normal_path() -> None:
    """Test scheduler path cost with normal zones."""
    graph = Graph()
    scheduler = Scheduler(graph)

    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0)
    end = Zone("end", 2, 0)

    path = [start, a, end]

    assert scheduler._get_path_cost(path) == 2


def test_scheduler_get_path_cost_with_restricted_zone() -> None:
    """Test scheduler path cost with restricted zone."""
    graph = Graph()
    scheduler = Scheduler(graph)

    start = Zone("start", 0, 0)
    restricted = Zone("restricted", 1, 0, zone_type="restricted")
    end = Zone("end", 2, 0)

    path = [start, restricted, end]

    assert scheduler._get_path_cost(path) == 3


def test_scheduler_get_first_connection_capacity() -> None:
    """Test getting the first connection capacity of a path."""
    graph = Graph()

    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0)
    end = Zone("end", 2, 0)

    graph.add_zone(start)
    graph.add_zone(a)
    graph.add_zone(end)
    graph.add_connection(
        Connection(
            start,
            a,
            max_link_capacity=3,
        )
    )
    graph.add_connection(Connection(a, end))

    scheduler = Scheduler(graph)

    assert scheduler._get_first_connection_capacity([start, a, end]) == 3


def test_find_all_paths_respects_max_depth() -> None:
    """Test that paths deeper than max_depth are ignored."""
    graph = Graph()

    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0)
    b = Zone("B", 2, 0)
    end = Zone("end", 3, 0)

    graph.add_zone(start)
    graph.add_zone(a)
    graph.add_zone(b)
    graph.add_zone(end)

    graph.add_connection(Connection(start, a))
    graph.add_connection(Connection(a, b))
    graph.add_connection(Connection(b, end))

    pathfinder = Pathfinder(graph)

    paths = pathfinder.find_all_paths(
        start,
        end,
        max_depth=3,
    )

    assert paths == []
