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
        self.nb_drones: int = 0

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

    """Return all zones directly connected to the given zone."""
    def get_neighbors(self, zone: Zone) -> list[Zone]:

        neighbors: list[Zone] = []

        for connection in self.connections:
            if connection.zone_a.name == zone.name:
                neighbors.append(connection.zone_b)
            elif connection.zone_b.name == zone.name:
                neighbors.append(connection.zone_a)

        return neighbors
    
    """Set the start zone of the graph."""
    def set_start_zone(self, zone: Zone) -> None:

        if self.start_zone is not None:
            raise ValueError("Start zone is already defined")

        self.start_zone = zone
        self.add_zone(zone)

    """Set the end zone of the graph."""
    def set_end_zone(self, zone: Zone) -> None:
        
        if self.end_zone is not None:
            raise ValueError("End zone is already defined")

        self.end_zone = zone
        self.add_zone(zone)

    """Validate that the graph has the required structure."""
    def validate(self) -> None:

        if self.start_zone is None:
            raise ValueError("Graph does not have a start zone")

        if self.end_zone is None:
            raise ValueError("Graph does not have an end zone")

        if not self.connections:
            raise ValueError("Graph does not have any connections")

        if self.nb_drones < 1:
            raise ValueError("Graph does not have a valid number of drones")

    """Set the number of drones."""
    def set_nb_drones(self, nb_drones: int) -> None:
        if nb_drones < 1:
            raise ValueError("nb_drones must be greater than 0")

        self.nb_drones = nb_drones