"""Graph model for the Fly-in project."""

from models.connection import Connection
from models.zone import Zone


class Graph:
    """Represent the complete drone network graph."""

    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start_zone: Zone | None = None
        self.end_zone: Zone | None = None

        """Add a zone to the graph."""
        def add_zone(self, zone: Zone) -> None:
            if zone.name in self.zones:
                raise ValueError(
                    f"Duplicate zone name: {zone.name}"
                )

            self.zones[zone.name] = zone

        """Return a zone by its name."""
        def get_zone(self, name: str) -> Zone:
        
            if name not in self.zones:
                raise ValueError(
                    f"Unknown zone: {name}"
                )

            return self.zones[name]

        """Add a connection to the graph."""
        def add_connection(self, connection: Connection) -> None:
        
            zone_a_name = connection.zone_a.name
            zone_b_name = connection.zone_b.name

            for existing_connection in self.connections:
                same_direction = (
                    existing_connection.zone_a.name == zone_a_name
                    and existing_connection.zone_b.name == zone_b_name
                )
                opposite_direction = (
                    existing_connection.zone_a.name == zone_b_name
                    and existing_connection.zone_b.name == zone_a_name
                )

                if same_direction or opposite_direction:
                    raise ValueError(
                        f"Duplicate connection: {zone_a_name}-{zone_b_name}"
                    )

            self.connections.append(connection)


        def get_neighbors(self, zone: Zone):
            try:
                get_zone(zone.name)
                self.
            except:
