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

        try:
            zone_content, metadata = self._split_metadata(content)
        except ValueError as error:
            raise ValueError(
                f"Line {line_number}: {error}"
            ) from error
        
        valid_zone_metadata = {
            "zone",
            "color",
            "max_drones",
        }

        for key in metadata:
            if key not in valid_zone_metadata:
                raise ValueError(
                    f"Line {line_number}: unknown zone metadata: {key}"
                )

        parts = zone_content.split()

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

        zone_type = metadata.get("zone", "normal")
        color = metadata.get("color", "none")

        try:
            max_drones = int(metadata.get("max_drones", "1"))
        except ValueError as error:
            raise ValueError(
                f"Line {line_number}: invalid max_drones value"
            ) from error

        try:
            zone = Zone(
                name=name,
                x=x,
                y=y,
                zone_type=zone_type,
                color=color,
                max_drones=max_drones,
            )
        except ValueError as error:
            raise ValueError(
                f"Line {line_number}: {error}"
            ) from error

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

        try:
            connection_content, metadata = self._split_metadata(content)
        except ValueError as error:
            raise ValueError(
                f"Line {line_number}: {error}"
            ) from error
        
        valid_connection_metadata = {
            "max_link_capacity",
        }

        for key in metadata:
            if key not in valid_connection_metadata:
                raise ValueError(
                    f"Line {line_number}: unknown connection metadata: {key}"
                )

        parts = connection_content.split("-")

        if len(parts) != 2:
            raise ValueError(
                f"Line {line_number}: invalid connection definition"
            )

        zone_a_name = parts[0]
        zone_b_name = parts[1]

        zone_a = graph.get_zone(zone_a_name)
        zone_b = graph.get_zone(zone_b_name)

        try:
            max_link_capacity = int(
                metadata.get("max_link_capacity", "1")
            )
        except ValueError as error:
            raise ValueError(
                f"Line {line_number}: invalid max_link_capacity value"
            ) from error

        try:
            connection = Connection(
                zone_a,
                zone_b,
                max_link_capacity=max_link_capacity,
            )
        except ValueError as error:
            raise ValueError(
                f"Line {line_number}: {error}"
            ) from error
        graph.add_connection(connection)
    
    def _split_metadata(self, content: str) -> tuple[str, dict[str, str]]:
        """Split line content into main content and metadata."""
        if "[" not in content:
            return content.strip(), {}

        before_metadata, metadata_part = content.split("[", 1)

        if not metadata_part.endswith("]"):
            raise ValueError("invalid metadata block")

        metadata_content = metadata_part.removesuffix("]").strip()
        metadata: dict[str, str] = {}

        if not metadata_content:
            return before_metadata.strip(), metadata

        for item in metadata_content.split():
            if "=" not in item:
                raise ValueError("invalid metadata item")

            key, value = item.split("=", 1)
            metadata[key] = value

        return before_metadata.strip(), metadata