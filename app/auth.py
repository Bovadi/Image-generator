import os


def validate_inbound_token(authorization_header: str | None) -> bool:
    """Validate the bearer token sent by Rails on inbound requests."""
    expected = os.environ.get("INBOUND_BEARER_TOKEN")
    if not expected:
        raise RuntimeError("INBOUND_BEARER_TOKEN env var is not set")
    if not authorization_header:
        return False
    parts = authorization_header.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return False
    return parts[1] == expected


def callback_auth_header() -> str:
    """Return the Authorization header value to include in callback POSTs to Rails."""
    token = os.environ.get("CALLBACK_BEARER_TOKEN")
    if not token:
        raise RuntimeError("CALLBACK_BEARER_TOKEN env var is not set")
    return f"Bearer {token}"
