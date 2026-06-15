"""Tests for the Drone model."""

import pytest

from models.drone import Drone
from models.zone import Zone


def test_create_valid_drone() -> None:
    """Test that a valid drone can be created."""
    start = Zone("start", 0, 0)

    drone = Drone(1, start)

    assert drone.drone_id == 1
    assert drone.current_zone == start
    assert drone.is_delivered is False


def test_invalid_drone_id_raises_error() -> None:
    """Test that drone id must be positive."""
    start = Zone("start", 0, 0)

    with pytest.raises(ValueError):
        Drone(0, start)