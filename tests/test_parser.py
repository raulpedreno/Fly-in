"""Tests for the Parser."""

from parser.parser import Parser
import pytest
from pathlib import Path


def test_parse_valid_basic_map(tmp_path: Path) -> None:
    """Test parsing a valid basic map."""
    map_file = tmp_path / "map.txt"
    map_file.write_text(
        "\n".join(
            [
                "nb_drones: 2",
                "start_hub: start 0 0",
                "end_hub: end 10 10",
                "connection: start-end",
            ]
        ),
        encoding="utf-8",
    )

    parser = Parser(str(map_file))
    graph = parser.parse()

    assert graph.nb_drones == 2
    assert graph.start_zone is not None
    assert graph.end_zone is not None
    assert graph.start_zone.name == "start"
    assert graph.end_zone.name == "end"
    assert len(graph.connections) == 1


def test_parse_zone_metadata(tmp_path: Path) -> None:
    """Test parsing zone metadata."""
    map_file = tmp_path / "map.txt"
    map_file.write_text(
        "\n".join(
            [
                "nb_drones: 2",
                "start_hub: start 0 0 [color=green]",
                "end_hub: end 10 10 [color=yellow]",
                "hub: A 1 1 [zone=restricted color=red max_drones=2]",
                "connection: start-A",
                "connection: A-end",
            ]
        ),
        encoding="utf-8",
    )

    parser = Parser(str(map_file))
    graph = parser.parse()

    zone = graph.get_zone("A")

    assert zone.zone_type == "restricted"
    assert zone.color == "red"
    assert zone.max_drones == 2


def test_parse_connection_metadata(tmp_path: Path) -> None:
    """Test parsing connection metadata."""
    map_file = tmp_path / "map.txt"
    map_file.write_text(
        "\n".join(
            [
                "nb_drones: 2",
                "start_hub: start 0 0",
                "end_hub: end 10 10",
                "connection: start-end [max_link_capacity=3]",
            ]
        ),
        encoding="utf-8",
    )

    parser = Parser(str(map_file))
    graph = parser.parse()

    assert graph.connections[0].max_link_capacity == 3


def test_parse_unknown_zone_metadata_raises_error(tmp_path: Path) -> None:
    """Test that unknown zone metadata raises an error."""
    map_file = tmp_path / "map.txt"
    map_file.write_text(
        "\n".join(
            [
                "nb_drones: 2",
                "start_hub: start 0 0",
                "end_hub: end 10 10",
                "hub: A 1 1 [banana=yes]",
                "connection: start-A",
                "connection: A-end",
            ]
        ),
        encoding="utf-8",
    )

    parser = Parser(str(map_file))

    with pytest.raises(ValueError):
        parser.parse()


def test_parse_invalid_zone_type_raises_error(tmp_path: Path) -> None:
    """Test that invalid zone type raises an error."""
    map_file = tmp_path / "map.txt"
    map_file.write_text(
        "\n".join(
            [
                "nb_drones: 2",
                "start_hub: start 0 0",
                "end_hub: end 10 10",
                "hub: A 1 1 [zone=invalid]",
                "connection: start-A",
                "connection: A-end",
            ]
        ),
        encoding="utf-8",
    )

    parser = Parser(str(map_file))

    with pytest.raises(ValueError):
        parser.parse()


def test_parse_connection_to_unknown_zone_raises_error(tmp_path: Path) -> None:
    """Test that connection to unknown zone raises an error."""
    map_file = tmp_path / "map.txt"
    map_file.write_text(
        "\n".join(
            [
                "nb_drones: 2",
                "start_hub: start 0 0",
                "end_hub: end 10 10",
                "connection: start-A",
            ]
        ),
        encoding="utf-8",
    )

    parser = Parser(str(map_file))

    with pytest.raises(ValueError):
        parser.parse()
