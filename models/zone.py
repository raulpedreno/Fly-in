"""Zone model for the Fly-in project."""


class Zone:
    """Represent a zone in the drone network graph."""

    VALID_ZONE_TYPES = {
        "normal",
        "blocked",
        "restricted",
        "priority",
    }

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: str = "normal",
        color: str = "none",
        max_drones: int = 1,
    ) -> None:

        if zone_type not in self.VALID_ZONE_TYPES:
            raise ValueError(
                f"Invalid zone type: {zone_type}"
            )

        if max_drones < 1:
            raise ValueError(
                "max_drones must be greater than 0"
            )

        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones

    def __repr__(self) -> str:
        return (
            f"Zone("
            f"name='{self.name}', "
            f"type='{self.zone_type}', "
            f"capacity={self.max_drones}"
            f")"
        )
