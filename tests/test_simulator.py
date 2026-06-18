"""Tests for the Simulator."""

from models.drone import Drone
from models.zone import Zone
from simulation.simulator import Simulator
from models.connection import Connection
from models.graph import Graph
import pytest


def test_get_zone_occupancy_counts_drones_in_zones() -> None:
    """Test current zone occupancy count."""
    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0)

    graph = Graph()
    graph.add_zone(start)
    graph.add_zone(a)
    graph.add_connection(Connection(start, a))

    drones = [
        Drone(1, start),
        Drone(2, start),
        Drone(3, a),
    ]

    simulator = Simulator(
        graph=graph,
        drones=drones,
        assignments={
            1: [start, a],
            2: [start, a],
            3: [a],
        },
    )

    occupancy = simulator._get_zone_occupancy()

    assert occupancy == {
        "start": 2,
        "A": 1,
    }


def test_get_zone_occupancy_ignores_delivered_and_transit_drones() -> None:
    """Test occupancy ignores delivered and in-transit drones."""
    start = Zone("start", 0, 0)
    restricted = Zone("restricted", 1, 0, zone_type="restricted")

    graph = Graph()
    graph.add_zone(start)
    graph.add_zone(restricted)
    graph.add_connection(Connection(start, restricted))

    drone_in_zone = Drone(1, start)
    drone_delivered = Drone(2, start)
    drone_in_transit = Drone(3, start)

    drone_delivered.is_delivered = True
    drone_in_transit.in_transit_to = restricted
    drone_in_transit.remaining_turns = 1

    simulator = Simulator(
        graph=graph,
        drones=[
            drone_in_zone,
            drone_delivered,
            drone_in_transit,
        ],
        assignments={
            1: [start, restricted],
            2: [start, restricted],
            3: [start, restricted],
        },
    )

    occupancy = simulator._get_zone_occupancy()

    assert occupancy == {
        "start": 1,
    }


def test_validate_zone_occupancy_raises_when_zone_exceeds_capacity() -> None:
    """Test validation fails if a regular zone exceeds capacity."""
    a = Zone("A", 1, 0, max_drones=1)
    end = Zone("end", 2, 0)

    graph = Graph()
    graph.add_zone(a)
    graph.add_zone(end)
    graph.add_connection(Connection(a, end))

    drones = [
        Drone(1, a),
        Drone(2, a),
    ]

    simulator = Simulator(
        graph=graph,
        drones=drones,
        assignments={
            1: [a, end],
            2: [a, end],
        },
    )

    with pytest.raises(ValueError):
        simulator._validate_zone_occupancy()


def test_validate_zone_occupancy_allows_multiple_drones_in_start() -> None:
    """Test validation allows multiple drones in start zone."""
    start = Zone("start", 0, 0, max_drones=1)
    end = Zone("end", 1, 0)

    graph = Graph()
    graph.set_start_zone(start)
    graph.set_end_zone(end)
    graph.add_connection(Connection(start, end))

    drones = [
        Drone(1, start),
        Drone(2, start),
    ]

    simulator = Simulator(
        graph=graph,
        drones=drones,
        assignments={
            1: [start, end],
            2: [start, end],
        },
    )

    simulator._validate_zone_occupancy()


def test_validate_zone_occupancy_allows_multiple_drones_in_end() -> None:
    """Test validation allows multiple drones in end zone."""
    start = Zone("start", 0, 0)
    end = Zone("end", 1, 0, max_drones=1)

    graph = Graph()
    graph.set_start_zone(start)
    graph.set_end_zone(end)
    graph.add_connection(Connection(start, end))

    drone_1 = Drone(1, end)
    drone_2 = Drone(2, end)

    drones = [drone_1, drone_2]

    simulator = Simulator(
        graph=graph,
        drones=drones,
        assignments={
            1: [start, end],
            2: [start, end],
        },
    )

    simulator._validate_zone_occupancy()


def test_validate_assignments_missing_assignment_raises_error() -> None:
    """Test missing drone assignment raises an error."""
    start = Zone("start", 0, 0)
    end = Zone("end", 1, 0)

    graph = Graph()
    graph.add_zone(start)
    graph.add_zone(end)
    graph.add_connection(Connection(start, end))

    drone = Drone(1, start)

    simulator = Simulator(
        graph=graph,
        drones=[drone],
        assignments={},
    )

    with pytest.raises(ValueError):
        simulator._validate_assignments()


def test_validate_assignments_invalid_short_path_raises_error() -> None:
    """Test path with fewer than two zones raises an error."""
    start = Zone("start", 0, 0)

    graph = Graph()
    graph.add_zone(start)

    drone = Drone(1, start)

    simulator = Simulator(
        graph=graph,
        drones=[drone],
        assignments={
            1: [start],
        },
    )

    with pytest.raises(ValueError):
        simulator._validate_assignments()


def test_validate_assignments_path_wrong_start_raises_error() -> None:
    """Test path that does not start at drone zone raises an error."""
    start = Zone("start", 0, 0)
    other = Zone("other", 1, 0)
    end = Zone("end", 2, 0)

    graph = Graph()
    graph.add_zone(start)
    graph.add_zone(other)
    graph.add_zone(end)
    graph.add_connection(Connection(start, end))
    graph.add_connection(Connection(other, end))

    drone = Drone(1, start)

    simulator = Simulator(
        graph=graph,
        drones=[drone],
        assignments={
            1: [other, end],
        },
    )

    with pytest.raises(ValueError):
        simulator._validate_assignments()


def test_validate_assignments_path_wrong_end_raises_error() -> None:
    """Test path that does not end at graph end zone raises an error."""
    start = Zone("start", 0, 0)
    wrong_end = Zone("wrong_end", 1, 0)
    real_end = Zone("end", 2, 0)

    graph = Graph()
    graph.set_start_zone(start)
    graph.add_zone(wrong_end)
    graph.set_end_zone(real_end)
    graph.add_connection(Connection(start, wrong_end))
    graph.add_connection(Connection(wrong_end, real_end))

    drone = Drone(1, start)

    simulator = Simulator(
        graph=graph,
        drones=[drone],
        assignments={
            1: [start, wrong_end],
        },
    )

    with pytest.raises(ValueError):
        simulator._validate_assignments()


def test_validate_assignments_path_without_connection_raises_error() -> None:
    """Test path with disconnected consecutive zones raises an error."""
    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0)
    end = Zone("end", 2, 0)

    graph = Graph()
    graph.set_start_zone(start)
    graph.add_zone(a)
    graph.set_end_zone(end)

    graph.add_connection(Connection(start, a))
    # Missing connection: A-end

    drone = Drone(1, start)

    simulator = Simulator(
        graph=graph,
        drones=[drone],
        assignments={
            1: [start, a, end],
        },
    )

    with pytest.raises(ValueError):
        simulator._validate_assignments()


def test_simulator_detects_deadlock_when_no_drone_moves() -> None:
    """Test simulator raises an error when no drone can move."""
    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0, max_drones=1)
    end = Zone("end", 2, 0)

    graph = Graph()
    graph.set_start_zone(start)
    graph.add_zone(a)
    graph.set_end_zone(end)
    graph.add_connection(Connection(start, a))
    graph.add_connection(Connection(a, end))

    drone = Drone(1, a)

    simulator = Simulator(
        graph=graph,
        drones=[drone],
        assignments={
            1: [a, end],
        },
    )

    graph.connections.clear()

    with pytest.raises(ValueError):
        simulator.run()


def test_restricted_zone_respects_connection_capacity() -> None:
    """Test restricted movement respects connection capacity."""
    start = Zone("start", 0, 0)
    restricted = Zone("restricted", 1, 0, zone_type="restricted")
    end = Zone("end", 2, 0)

    graph = Graph()
    graph.set_start_zone(start)
    graph.add_zone(restricted)
    graph.set_end_zone(end)
    graph.add_connection(
        Connection(
            start,
            restricted,
            max_link_capacity=1,
        )
    )
    graph.add_connection(Connection(restricted, end))

    drones = [
        Drone(1, start),
        Drone(2, start),
    ]

    path = [start, restricted, end]

    simulator = Simulator(
        graph=graph,
        drones=drones,
        assignments={
            1: path,
            2: path,
        },
    )

    output = simulator.run()

    assert output == [
        "D1-start-restricted",
        "D1-restricted D2-start-restricted",
        "D1-end D2-restricted",
        "D2-end",
    ]


def test_restricted_zone_capacity_when_arriving_from_different_paths() -> None:
    """Test restricted zone capacity with arrivals from different paths."""
    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0)
    b = Zone("B", 1, 1)
    restricted = Zone(
        "restricted",
        2,
        0,
        zone_type="restricted",
        max_drones=1,
    )
    end = Zone("end", 3, 0)

    graph = Graph()
    graph.set_start_zone(start)
    graph.add_zone(a)
    graph.add_zone(b)
    graph.add_zone(restricted)
    graph.set_end_zone(end)

    graph.add_connection(Connection(start, a))
    graph.add_connection(Connection(start, b))
    graph.add_connection(Connection(a, restricted))
    graph.add_connection(Connection(b, restricted))
    graph.add_connection(Connection(restricted, end))

    drone_1 = Drone(1, start)
    drone_2 = Drone(2, start)

    simulator = Simulator(
        graph=graph,
        drones=[drone_1, drone_2],
        assignments={
            1: [start, a, restricted, end],
            2: [start, b, restricted, end],
        },
    )

    output = simulator.run()

    assert output == [
        "D1-A D2-B",
        "D1-A-restricted",
        "D1-restricted D2-B-restricted",
        "D1-end D2-restricted",
        "D2-end",
    ]
