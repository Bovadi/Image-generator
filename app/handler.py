import json
import logging
import threading

import requests

from app.auth import validate_inbound_token, callback_auth_header
from app.moderation import check_scenario, ModerationError
from app.generator import generate_image, GenerationError
from app.storage import upload_from_url
from app.characters import get_character

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _json_response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def _post_callback(callback_url: str, payload: dict) -> None:
    try:
        requests.post(
            callback_url,
            json=payload,
            headers={
                "Authorization": callback_auth_header(),
                "Content-Type": "application/json",
            },
            timeout=15,
        )
    except Exception as exc:
        logger.error("Failed to POST callback to %s: %s", callback_url, exc)


def _process(character_id: str, scenario: str, callback_url: str) -> None:
    """Generate image and fire callback. Runs inline (sync) or in a thread (async)."""
    try:
        fal_url = generate_image(character_id, scenario)
        s3_url = upload_from_url(fal_url)
        _post_callback(callback_url, {"status": "success", "image_url": s3_url})
    except GenerationError as exc:
        logger.error("Generation failed for character=%s: %s", character_id, exc)
        _post_callback(callback_url, {"status": "error", "message": str(exc)})
    except Exception as exc:
        logger.error("Unexpected error for character=%s: %s", character_id, exc)
        _post_callback(callback_url, {"status": "error", "message": "Unexpected server error"})


def handler(event: dict, context) -> dict:
    """
    AWS Lambda entrypoint.

    Expected request body:
        {
            "character_id": "asian_boy_child",
            "scenario": "crying after being told to wait",
            "callback_url": "https://app.bipvisualized.com/webhooks/image_ready",
            "sync": false  // optional, defaults to false; set true for demo/testing
        }

    Headers:
        Authorization: Bearer <INBOUND_BEARER_TOKEN>
    """
    # Auth
    auth_header = (event.get("headers") or {}).get("Authorization") or \
                  (event.get("headers") or {}).get("authorization")
    if not validate_inbound_token(auth_header):
        return _json_response(401, {"error": "Unauthorized"})

    # Parse body
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _json_response(400, {"error": "Invalid JSON body"})

    character_id = body.get("character_id", "").strip()
    scenario = body.get("scenario", "").strip()
    callback_url = body.get("callback_url", "").strip()
    sync_mode = bool(body.get("sync", False))

    # Validate required fields
    if not character_id:
        return _json_response(400, {"error": "Missing required field: character_id"})
    if not scenario:
        return _json_response(400, {"error": "Missing required field: scenario"})
    if not callback_url and not sync_mode:
        return _json_response(400, {"error": "Missing required field: callback_url"})

    # Validate character exists
    try:
        get_character(character_id)
    except ValueError as exc:
        return _json_response(400, {"error": str(exc)})

    # Moderation check — reject early before incurring generation cost
    try:
        check_scenario(scenario)
    except ModerationError as exc:
        return _json_response(422, {"error": "Scenario failed content moderation", "categories": exc.categories})

    # Sync mode: process inline and return result directly (for demo/testing)
    if sync_mode:
        try:
            fal_url = generate_image(character_id, scenario)
            s3_url = upload_from_url(fal_url)
            return _json_response(200, {"status": "success", "image_url": s3_url})
        except GenerationError as exc:
            return _json_response(500, {"status": "error", "message": str(exc)})
        except Exception as exc:
            logger.error("Sync generation error: %s", exc)
            return _json_response(500, {"status": "error", "message": "Unexpected server error"})

    # Async mode: acknowledge immediately, process in background thread
    thread = threading.Thread(
        target=_process,
        args=(character_id, scenario, callback_url),
        daemon=True,
    )
    thread.start()

    return _json_response(202, {"status": "accepted", "message": "Image generation started"})
