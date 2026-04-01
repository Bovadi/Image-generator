import os
import time
import logging

import fal_client

from app.characters import get_character

logger = logging.getLogger(__name__)

FAL_MODEL = "fal-ai/flux-lora"
IMAGE_SIZE = "square_hd"  # 1024x1024
MAX_ATTEMPTS = 4
BACKOFF_SECONDS = [2, 4, 8]

STYLE_SUFFIX = (
    "flat illustration style, clean lines, minimal shading, solid flat colors, "
    "educational illustration, child-friendly, friendly cartoon, simple background, no text, no words"
)

NEGATIVE_PROMPT = (
    "realistic, photographic, 3D render, complex shading, dark, scary, violent, "
    "sexual, text, watermark, logo, signature"
)


class GenerationError(Exception):
    """Raised when all retry attempts are exhausted."""
    pass


def build_prompt(character: dict, scenario: str) -> str:
    return (
        f"{character['trigger_word']}, {character['description']}, "
        f"actively {scenario}, full body, dynamic action pose, appropriate setting and background. "
        f"{STYLE_SUFFIX}."
    )


def generate_image(character_id: str, scenario: str) -> str:
    """
    Generate an image for the given character and scenario using fal.ai FLUX + LoRA.
    Returns the image URL from fal.ai (caller is responsible for uploading to S3).
    Retries up to MAX_ATTEMPTS times with exponential backoff.
    Raises GenerationError if all attempts fail.
    """
    os.environ.setdefault("FAL_KEY", os.environ.get("FAL_KEY", ""))

    character = get_character(character_id)
    prompt = build_prompt(character, scenario)

    last_error = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            logger.info("fal.ai generation attempt %d for character=%s", attempt + 1, character_id)
            result = fal_client.run(
                FAL_MODEL,
                arguments={
                    "prompt": prompt,
                    "negative_prompt": NEGATIVE_PROMPT,
                    "loras": [{"path": character["lora_url"], "scale": 1.0}],
                    "image_size": IMAGE_SIZE,
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                    "num_images": 1,
                    "enable_safety_checker": True,
                },
            )
            images = result.get("images", [])
            if not images:
                raise GenerationError("fal.ai returned no images")
            return images[0]["url"]

        except GenerationError:
            raise
        except Exception as exc:
            last_error = exc
            logger.warning("fal.ai attempt %d failed: %s", attempt + 1, exc)
            if attempt < len(BACKOFF_SECONDS):
                time.sleep(BACKOFF_SECONDS[attempt])

    raise GenerationError(f"All {MAX_ATTEMPTS} generation attempts failed: {last_error}") from last_error
