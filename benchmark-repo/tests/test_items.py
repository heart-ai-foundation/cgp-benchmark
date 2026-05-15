from src.api.routes.items import get_item, list_items


def test_list_items_omits_archived_items_by_default():
    items = list_items()
    assert all(not item["archived"] for item in items)


def test_get_item_returns_matching_item():
    assert get_item(1)["name"] == "Notebook"
