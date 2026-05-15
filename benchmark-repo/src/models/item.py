from dataclasses import dataclass


@dataclass
class Item:
    id: int
    owner_id: int
    name: str
    archived: bool = False

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "name": self.name,
            "archived": self.archived,
        }
