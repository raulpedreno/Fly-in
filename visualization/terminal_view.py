"""Terminal visualization for the Fly-in project."""
from time import sleep

class TerminalView:
    """Display simulation output in the terminal."""

    COLORS = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "gray": "\033[90m",
        "cyan": "\033[96m",
        "none": "",
    }

    RESET = "\033[0m"

    def colorize(self, text: str, color: str) -> str:
        """Return colored text using ANSI escape codes.

        Args:
            text: Text to colorize.
            color: Color name.

        Returns:
            Colored text if the color is supported.
        """
        ansi_color = self.COLORS.get(color, "")

        if not ansi_color:
            return text

        return f"{ansi_color}{text}{self.RESET}"

    def display_banner(self) -> None:
        """Display the Fly-in mission banner."""
        banner = r"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ███████╗██╗     ██╗   ██╗      ██╗███╗   ██╗             ║
║     ██╔════╝██║     ╚██╗ ██╔╝      ██║████╗  ██║             ║
║     █████╗  ██║      ╚████╔╝ █████╗██║██╔██╗ ██║             ║
║     ██╔══╝  ██║       ╚██╔╝  ╚════╝██║██║╚██╗██║             ║
║     ██║     ███████╗   ██║         ██║██║ ╚████║             ║
║     ╚═╝     ╚══════╝   ╚═╝         ╚═╝╚═╝  ╚═══╝             ║
║                                                              ║
║        Autonomous Drone Routing Simulator v1.0               ║
║                                                              ║
║                                                     rpedreno ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(self.colorize(banner, "cyan"))
        sleep(0.5)

    def display_loading_sequence(self) -> None:
        """Display mission loading sequence."""
        steps = [
            "Loading map...",
            "Parsing zones...",
            "Computing optimal routes...",
            "Launching swarm...",
        ]

        for step in steps:
            print(self.colorize(f"► {step}", "green"))
            sleep(0.5)

    def _format_movement(self, movement: str) -> str:
        """Format a raw simulator movement into mission-control style.

        Args:
            movement: Raw movement like D1-A.

        Returns:
            Formatted movement line.
        """
        drone_id, destination = movement.split("-", 1)

        drone_label = self.colorize(f"[🚁 {drone_id}]", "blue")

        if destination == "end":
            arrived_label = self.colorize(f"[✅ {drone_id}]", "green")
            return f"{arrived_label} ARRIVED AT END"

        if "-" in destination:
            return f"{drone_label} ⇢ {self.colorize(destination, 'yellow')}"

        return f"{drone_label} ► {destination}"

    def display_turns(self, turns: list[str]) -> None:
        """Display all simulation turns in mission-control style.

        Args:
            turns: Simulation output lines.
        """
        separator = self.colorize(
            "═" * 62,
            "cyan",
        )

        for index, turn in enumerate(turns, start=1):
            print()
            print(separator)
            print(
                self.colorize(
                    f"MISSION ELAPSED TIME : T+{index:02d}",
                    "yellow",
                )
            )
            print()

            movements = turn.split()

            for movement in movements:
                print(self._format_movement(movement))
            
            sleep(0.5)

    def simple_display_turns(self, turns: list[str]) -> None:
        for turn in turns:
            print (turn)
    
    def display_summary(
        self,
        turns: list[str],
        nb_drones: int,
        routes_count: int,
    ) -> None:
        """Display final mission summary."""

        separator = self.colorize(
            "═" * 62,
            "cyan",
        )

        print()
        print(separator)
        completed_banner = r"""
╔═════════════════════════════════════════════════════════╗
║                                                         ║
║   ███╗   ███╗██╗███████╗███████╗██╗ ██████╗ ███╗   ██╗  ║
║   ████╗ ████║██║██╔════╝██╔════╝██║██╔═══██╗████╗  ██║  ║
║   ██╔████╔██║██║███████╗███████╗██║██║   ██║██╔██╗ ██║  ║
║   ██║╚██╔╝██║██║╚════██║╚════██║██║██║   ██║██║╚██╗██║  ║
║   ██║ ╚═╝ ██║██║███████║███████║██║╚██████╔╝██║ ╚████║  ║
║   ╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝  ║
║                                                         ║
║                ✅ MISSION COMPLETED ✅                  ║
║                                                         ║
╚═════════════════════════════════════════════════════════╝
"""
        print(self.colorize(completed_banner, "green"))
        print()
        print(f"Delivered drones : {nb_drones}")
        print(f"Total turns      : {len(turns)}")
        print(f"Routes computed  : {routes_count}")
        print()
        print(self.colorize("All drones successfully reached destination.", "green"))
        print(separator)
        print()

    def display_raw_turns(self, turns: list[str]) -> None:
        """Display raw simulation output required by the subject.

        Args:
            turns: Simulation output lines.
        """
        for turn in turns:
            print(turn)