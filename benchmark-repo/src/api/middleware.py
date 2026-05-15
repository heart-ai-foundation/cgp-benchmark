def attach_request_id(headers: dict, request_id: str) -> dict:
    updated = dict(headers)
    updated["x-request-id"] = request_id
    return updated


def require_auth(headers: dict) -> bool:
    token = headers.get("authorization", "")
    return token.startswith("Bearer ")
