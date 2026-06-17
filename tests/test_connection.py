"""Tests for the Connection model."""

import pytest

from models.connection import Connection
from models.zone import Zone


def test_create_valid_connection() -> None:
    """Test that a valid connection can be created."""
    zone_a = Zone("A", 0, 0)
    zone_b = Zone("B", 1, 1)

    connection = Connection(zone_a, zone_b)

    assert connection.zone_a == zone_a
    assert connection.zone_b == zone_b
    assert connection.max_link_capacity == 1


def test_custom_capacity() -> None:
    """Test custom connection capacity."""
    zone_a = Zone("A", 0, 0)
    zone_b = Zone("B", 1, 1)

    connection = Connection(
        zone_a,
        zone_b,
        max_link_capacity=3,
    )

    assert connection.max_link_capacity == 3


def test_invalid_capacity_raises_error() -> None:
    """Test invalid connection capacity."""
    zone_a = Zone("A", 0, 0)
    zone_b = Zone("B", 1, 1)

    with pytest.raises(ValueError):
        Connection(
            zone_a,
            zone_b,
            max_link_capacity=0,
        )
