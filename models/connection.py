"""Connection model for the Fly-in project."""

from models.zone import Zone


class Connection:
    """Represent a bidirectional connection between two zones."""

    def __init__(
        self,
        zone_a: Zone,
        zone_b: Zone,
        max_link_capacity: int = 1,
    ) -> None:
        if max_link_capacity < 1:
            raise ValueError(
                "max_link_capacity must be greater than 0"
            )

        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

    def __repr__(self) -> str:
        return (
            f"Connection("
            f"{self.zone_a.name}-{self.zone_b.name}, "
            f"capacity={self.max_link_capacity}"
            f")"
        )
