import json
import os
from unittest.mock import patch, MagicMock

import pytest

os.environ.setdefault("INBOUND_BEARER_TOKEN", "test-inbound-token")
os.environ.setdefault("CALLBACK_BEARER_TOKEN", "test-callback-token")
os.environ.setdefault("AWS_BUCKET_NAME", "test-bucket")
os.environ.setdefault("FAL_KEY", "test-fal-key")
os.environ.setdefault("OPENAI_API_KEY", "test-openai-key")

from app.handler import handler


def make_event(body: dict, token: str = "test-inbound-token") -> dict:
    return {
        "headers": {"Authorization": f"Bearer {token}"},
        "body": json.dumps(body),
    }


VALID_BODY = {
    "character_id": "asian_boy_child",
    "scenario": "waiting patiently for his turn",
    "callback_url": "https://example.com/callback",
}


# --- Auth ---

def test_missing_auth_header_returns_401():
    event = {"headers": {}, "body": json.dumps(VALID_BODY)}
    response = handler(event, None)
    assert response["statusCode"] == 401


def test_wrong_token_returns_401():
    response = handler(make_event(VALID_BODY, token="wrong-token"), None)
    assert response["statusCode"] == 401


# --- Input validation ---

def test_missing_character_id_returns_400():
    body = {**VALID_BODY, "character_id": ""}
    response = handler(make_event(body), None)
    assert response["statusCode"] == 400
    assert "character_id" in json.loads(response["body"])["error"]


def test_missing_scenario_returns_400():
    body = {**VALID_BODY, "scenario": ""}
    response = handler(make_event(body), None)
    assert response["statusCode"] == 400
    assert "scenario" in json.loads(response["body"])["error"]


def test_unknown_character_id_returns_400():
    body = {**VALID_BODY, "character_id": "nonexistent_character"}
    response = handler(make_event(body), None)
    assert response["statusCode"] == 400
    assert "character_id" in json.loads(response["body"])["error"].lower() or \
           "unknown" in json.loads(response["body"])["error"].lower()


def test_missing_callback_url_in_async_mode_returns_400():
    body = {"character_id": "asian_boy_child", "scenario": "waiting for a turn"}
    response = handler(make_event(body), None)
    assert response["statusCode"] == 400
    assert "callback_url" in json.loads(response["body"])["error"]


# --- Moderation ---

def test_flagged_scenario_returns_422():
    from app.moderation import ModerationError
    with patch("app.handler.check_scenario", side_effect=ModerationError(["hate"])):
        response = handler(make_event(VALID_BODY), None)
    assert response["statusCode"] == 422
    body = json.loads(response["body"])
    assert "moderation" in body["error"].lower()
    assert "hate" in body["categories"]


# --- Async mode ---

def test_async_mode_returns_202():
    with patch("app.handler.check_scenario"), \
         patch("app.handler.threading.Thread") as mock_thread:
        mock_thread.return_value = MagicMock()
        response = handler(make_event(VALID_BODY), None)
    assert response["statusCode"] == 202
    assert json.loads(response["body"])["status"] == "accepted"


# --- Sync mode ---

def test_sync_mode_returns_200_with_image_url():
    body = {**VALID_BODY, "sync": True}
    with patch("app.handler.check_scenario"), \
         patch("app.handler.generate_image", return_value="https://fal.ai/image.png"), \
         patch("app.handler.upload_from_url", return_value="https://s3.example.com/image.png"):
        response = handler(make_event(body), None)
    assert response["statusCode"] == 200
    result = json.loads(response["body"])
    assert result["status"] == "success"
    assert result["image_url"] == "https://s3.example.com/image.png"


def test_sync_mode_generation_error_returns_500():
    from app.generator import GenerationError
    body = {**VALID_BODY, "sync": True}
    with patch("app.handler.check_scenario"), \
         patch("app.handler.generate_image", side_effect=GenerationError("fal.ai down")):
        response = handler(make_event(body), None)
    assert response["statusCode"] == 500
    assert "error" in json.loads(response["body"])["status"]
