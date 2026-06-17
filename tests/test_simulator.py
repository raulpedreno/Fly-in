"""Tests for the Simulator."""

from models.drone import Drone
from models.zone import Zone
from simulation.simulator import Simulator
from models.connection import Connection
from models.graph import Graph


def test_simulator_single_drone() -> None:
    """Test simulation with one drone."""
    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0)
    end = Zone("end", 2, 0)

    graph = Graph()
    graph.add_zone(start)
    graph.add_zone(a)
    graph.add_zone(end)
    graph.add_connection(Connection(start, a))
    graph.add_connection(Connection(a, end))

    drone = Drone(1, start)
    path = [start, a, end]

    simulator = Simulator(
        graph=graph,
        drones=[drone],
        assignments={1: path},
    )

    output = simulator.run()

    assert output == [
        "D1-A",
        "D1-end",
    ]


def test_simulator_multiple_drones_respects_zone_capacity() -> None:
    """Test simulation respects zone capacity."""
    start = Zone("start", 0, 0)
    a = Zone("A", 1, 0)
    end = Zone("end", 2, 0)

    graph = Graph()
    graph.add_zone(start)
    graph.add_zone(a)
    graph.add_zone(end)
    graph.add_connection(Connection(start, a))
    graph.add_connection(Connection(a, end))

    drones = [
        Drone(1, start),
        Drone(2, start),
    ]

    path = [start, a, end]

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
        "D1-A",
        "D1-end D2-A",
        "D2-end",
    ]


def test_simulator_respects_connection_capacity() -> None:
    """Test that connection capacity is respected."""
    start = Zone("start", 0, 0)
    end = Zone("end", 1, 0)

    graph = Graph()
    graph.add_zone(start)
    graph.add_zone(end)
    graph.add_connection(
        Connection(
            start,
            end,
            max_link_capacity=1,
        )
    )

    drones = [
        Drone(1, start),
        Drone(2, start),
    ]

    path = [start, end]

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
        "D1-end",
        "D2-end",
    ]


def test_simulator_restricted_zone_takes_two_turns() -> None:
    """Test that moving into a restricted zone takes two turns."""
    start = Zone("start", 0, 0)
    restricted = Zone("restricted", 1, 0, zone_type="restricted")
    end = Zone("end", 2, 0)

    graph = Graph()
    graph.add_zone(start)
    graph.add_zone(restricted)
    graph.add_zone(end)
    graph.add_connection(Connection(start, restricted))
    graph.add_connection(Connection(restricted, end))

    drone = Drone(1, start)
    path = [start, restricted, end]

    simulator = Simulator(
        graph=graph,
        drones=[drone],
        assignments={1: path},
    )

    output = simulator.run()

    assert output == [
        "D1-start-restricted",
        "D1-restricted",
        "D1-end",
    ]
