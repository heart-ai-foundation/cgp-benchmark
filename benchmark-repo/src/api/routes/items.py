from src.models.item import Item


ITEMS = [
    Item(id=1, owner_id=1, name="Notebook"),
    Item(id=2, owner_id=1, name="Pen"),
    Item(id=3, owner_id=2, name="Backpack"),
]


def list_items(include_archived: bool = False) -> list[dict]:
    return [
        item.as_dict()
        for item in ITEMS
        if include_archived or not item.archived
    ]


def get_item(item_id: int) -> dict | None:
    for item in ITEMS:
        if item.id == item_id:
            return item.as_dict()
    return None
