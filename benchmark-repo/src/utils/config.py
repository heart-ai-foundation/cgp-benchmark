def parse_config(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raise TypeError("config must be a dictionary")

    parsed = {
        "debug": False,
        "page_size": 25,
        "features": [],
    }

    if "debug" in raw:
        parsed["debug"] = bool(raw["debug"])

    if "page_size" in raw:
        page_size = int(raw["page_size"])
        if page_size < 1 or page_size > 100:
            raise ValueError("page_size must be between 1 and 100")
        parsed["page_size"] = page_size

    if "features" in raw:
        features = raw["features"]
        if isinstance(features, str):
            parsed["features"] = [features]
        elif isinstance(features, list):
            parsed["features"] = [str(feature) for feature in features]
        else:
            raise ValueError("features must be a string or list")

    return parsed
