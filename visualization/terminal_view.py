"""Terminal visualization for the Fly-in project."""


class TerminalView:
    """Display simulation output in the terminal."""

    def display_turns(self, turns: list[str]) -> None:
        """Display all simulation turns.

        Args:
            turns: Simulation output lines.
        """
        for turn in turns:
            print(turn)