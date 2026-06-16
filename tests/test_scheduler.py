"""Tests for the Scheduler."""

import pytest

from algorithms.scheduler import Scheduler
from models.zone import Zone


def test_assign_paths_single_path() -> None:
    """Test assigning all drones to a single path."""
    scheduler = Scheduler()

    start = Zone("start", 0, 0)
    end = Zone("end", 1, 1)
    path = [start, end]

    assignments = scheduler.assign_paths(3, [path])

    assert assignments[1] == path
    assert assignments[2] == path
    assert assignments[3] == path


def test_assign_paths_multiple_paths() -> None:
    """Test assigning drones across multiple paths."""
    scheduler = Scheduler()

    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0)
    b = Zone("B", 1, 1)
    end = Zone("end", 2, 0)

    path_1 = [start, a, end]
    path_2 = [start, b, end]

    assignments = scheduler.assign_paths(4, [path_1, path_2])

    assert assignments[1] == path_1
    assert assignments[2] == path_2
    assert assignments[3] == path_1
    assert assignments[4] == path_2


def test_assign_paths_without_paths_raises_error() -> None:
    """Test that assigning without paths raises an error."""
    scheduler = Scheduler()

    with pytest.raises(ValueError):
        scheduler.assign_paths(3, [])