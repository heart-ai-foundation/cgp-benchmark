from dataclasses import dataclass, field


@dataclass
class User:
    id: int
    email: str
    name: str
    active: bool = True
    item_ids: list[int] = field(default_factory=list)

    def can_login(self) -> bool:
        return self.active and "@" in self.email

    def owns_item(self, item_id: int) -> bool:
        return item_id in self.item_ids
