"""Drone model for the Fly-in project."""

from models.zone import Zone


class Drone:
    """Represent a drone moving through the graph."""

    def __init__(self, drone_id: int, current_zone: Zone) -> None:
        if drone_id < 1:
            raise ValueError("drone_id must be greater than 0")

        self.drone_id = drone_id
        self.current_zone = current_zone
        self.is_delivered = False   ##ha llegado a end_hub?

    def __repr__(self) -> str:
        return (
            f"Drone("
            f"id=D{self.drone_id}, "
            f"zone={self.current_zone.name}, "
            f"delivered={self.is_delivered}"
            f")"
        )
