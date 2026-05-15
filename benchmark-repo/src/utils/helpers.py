def compact_whitespace(value: str) -> str:
    return " ".join(value.split())


def index_by_id(rows: list[dict]) -> dict[int, dict]:
    return {row["id"]: row for row in rows}
