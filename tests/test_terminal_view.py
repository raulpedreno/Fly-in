"""Tests for the TerminalView."""

from visualization.terminal_view import TerminalView
from pytest import CaptureFixture


def test_colorize_supported_color() -> None:
    """Test colorizing text with a supported color."""
    view = TerminalView()

    result = view.colorize("hello", "green")

    assert result == "\033[32mhello\033[0m"


def test_colorize_unknown_color_returns_plain_text() -> None:
    """Test unknown colors return plain text."""
    view = TerminalView()

    result = view.colorize("hello", "unknown")

    assert result == "hello"


def test_format_normal_movement() -> None:
    """Test formatting a normal movement."""
    view = TerminalView()

    result = view._format_movement("D1-A")

    assert "D1" in result
    assert "A" in result
    assert "►" in result


def test_format_end_movement() -> None:
    """Test formatting an end movement."""
    view = TerminalView()

    result = view._format_movement("D1-end")

    assert "D1" in result
    assert "ARRIVED AT END" in result


def test_format_connection_movement() -> None:
    """Test formatting a connection movement."""
    view = TerminalView()

    result = view._format_movement("D1-start-restricted")

    assert "D1" in result
    assert "start-restricted" in result
    assert "⇢" in result

def test_display_turns_outputs_mission_format(capsys) -> None:
    """Test display_turns prints mission formatted turns."""
    view = TerminalView()

    view.display_turns(["D1-A D2-end"])

    captured = capsys.readouterr()

    assert "MISSION ELAPSED TIME : T+01" in captured.out
    assert "D1" in captured.out
    assert "A" in captured.out
    assert "D2" in captured.out
    assert "ARRIVED AT END" in captured.out


def test_display_summary_outputs_final_stats(capsys) -> None:
    """Test display_summary prints final mission stats."""
    view = TerminalView()

    view.display_summary(
        turns=["D1-A", "D1-end"],
        nb_drones=1,
        routes_count=2,
    )

    captured = capsys.readouterr()

    assert "MISSION COMPLETED" in captured.out
    assert "Delivered drones : 1" in captured.out
    assert "Total turns      : 2" in captured.out
    assert "Routes computed  : 2" in captured.out

def test_display_raw_turns_outputs_subject_format(
    capsys: CaptureFixture[str],
) -> None:
    """Test raw turns are printed exactly in subject format."""
    view = TerminalView()

    view.display_raw_turns(
        [
            "D1-A D2-B",
            "D1-end D2-end",
        ]
    )

    captured = capsys.readouterr()

    assert captured.out == (
        "D1-A D2-B\n"
        "D1-end D2-end\n"
    )