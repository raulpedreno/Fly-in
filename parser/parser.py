"""Parser for Fly-in map files."""

from models.graph import Graph
from models.zone import Zone
from models.connection import Connection


class Parser:
    """Parse a Fly-in map file into a Graph object."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def parse(self) -> Graph:
        """Parse the input file."""
        graph = Graph()

        with open(self.file_path, "r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()

                if not line or line.startswith("#"):
                    continue

                if line.startswith("nb_drones:"):
                    value = line.removeprefix("nb_drones:").strip()

                    try:
                        nb_drones = int(value)
                    except ValueError as error:
                        raise ValueError(
                            f"Line {line_number}: invalid nb_drones value"
                        ) from error

                    graph.set_nb_drones(nb_drones)
                    continue
                
                if (
                    line.startswith("start_hub:")
                    or line.startswith("end_hub:")
                    or line.startswith("hub:")
                ):
                    self._parse_zone_line(line, line_number, graph)
                    continue

                if line.startswith("connection:"):
                    self._parse_connection_line(line, line_number, graph)
                    continue

                raise ValueError(
                    f"Line {line_number}: unknown instruction: {line}"
                )
        graph.validate()
        return graph
    
    def _parse_zone_line(
        self,
        line: str,
        line_number: int,
        graph: Graph,
    ) -> None:
        """Parse a zone definition line."""
        prefix, content = line.split(":", 1)
        parts = content.strip().split()

        if len(parts) != 3:
            raise ValueError(
                f"Line {line_number}: invalid zone definition"
            )

        name = parts[0]

        try:
            x = int(parts[1])
            y = int(parts[2])
        except ValueError as error:
            raise ValueError(
                f"Line {line_number}: invalid zone coordinates"
            ) from error

        zone = Zone(name=name, x=x, y=y)

        if prefix == "start_hub":
            graph.set_start_zone(zone)
        elif prefix == "end_hub":
            graph.set_end_zone(zone)
        else:
            graph.add_zone(zone)

    def _parse_connection_line(
        self,
        line: str,
        line_number: int,
        graph: Graph,
    ) -> None:
        """Parse a connection definition line."""
        content = line.removeprefix("connection:").strip()
        parts = content.split("-")

        if len(parts) != 2:
            raise ValueError(
                f"Line {line_number}: invalid connection definition"
            )

        zone_a_name = parts[0]
        zone_b_name = parts[1]

        zone_a = graph.get_zone(zone_a_name)
        zone_b = graph.get_zone(zone_b_name)

        connection = Connection(zone_a, zone_b)
        graph.add_connection(connection)