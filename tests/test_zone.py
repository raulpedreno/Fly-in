"""Tests for the Zone model."""

import pytest

from models.zone import Zone


def test_create_valid_zone() -> None:
    """Test that a valid zone can be created."""
    zone = Zone("A", 1, 2)

    assert zone.name == "A"
    assert zone.x == 1
    assert zone.y == 2
    assert zone.zone_type == "normal"
    assert zone.color == "none"
    assert zone.max_drones == 1


def test_invalid_zone_type_raises_error() -> None:
    """Test that an invalid zone type raises an error."""
    with pytest.raises(ValueError):
        Zone("A", 1, 2, zone_type="invalid")


def test_invalid_capacity_raises_error() -> None:
    """Test that invalid capacity raises an error."""
    with pytest.raises(ValueError):
        Zone("A", 1, 2, max_drones=0)


def test_invalid_name_with_dash_raises_error() -> None:
    """Test that zone names cannot contain dashes."""
    with pytest.raises(ValueError):
        Zone("bad-name", 1, 2)