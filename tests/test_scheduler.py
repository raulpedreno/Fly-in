"""Tests for the Scheduler."""

import pytest

from algorithms.scheduler import Scheduler
from models.zone import Zone
from models.graph import Graph


def test_assign_paths_prefers_shorter_path() -> None:
    """Test assigning more drones to shorter paths."""
    graph = Graph()
    scheduler = Scheduler(graph)

    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0)
    b = Zone("B", 1, 1)
    c = Zone("C", 2, 1)
    end = Zone("end", 3, 0)

    short_path = [start, a, end]
    long_path = [start, b, c, end]

    assignments = scheduler.assign_paths(
        3,
        [short_path, long_path],
    )

    assert assignments[1] == short_path
    assert assignments[2] == short_path
    assert assignments[3] == long_path

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