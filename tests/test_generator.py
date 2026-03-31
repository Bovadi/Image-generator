import os
import time
from unittest.mock import patch, MagicMock

import pytest

os.environ.setdefault("FAL_KEY", "test-fal-key")

from app.generator import generate_image, build_prompt, GenerationError
from app.characters import get_character


def test_build_prompt_includes_trigger_word_and_scenario():
    character = get_character("asian_boy_child")
    prompt = build_prompt(character, "crying after being told to wait")
    assert character["trigger_word"] in prompt
    assert "crying after being told to wait" in prompt
    assert "flat illustration" in prompt


def test_generate_image_returns_url_on_success():
    mock_result = {"images": [{"url": "https://fal.ai/result/image.png"}]}
    with patch("app.generator.fal_client.run", return_value=mock_result):
        url = generate_image("asian_boy_child", "waiting patiently")
    assert url == "https://fal.ai/result/image.png"


def test_generate_image_retries_on_failure_then_succeeds():
    mock_result = {"images": [{"url": "https://fal.ai/result/image.png"}]}
    call_count = 0

    def flaky_run(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise RuntimeError("rate limit")
        return mock_result

    with patch("app.generator.fal_client.run", side_effect=flaky_run), \
         patch("app.generator.time.sleep"):
        url = generate_image("black_girl_child", "taking deep breaths")
    assert url == "https://fal.ai/result/image.png"
    assert call_count == 3


def test_generate_image_raises_after_max_attempts():
    with patch("app.generator.fal_client.run", side_effect=RuntimeError("service down")), \
         patch("app.generator.time.sleep"):
        with pytest.raises(GenerationError, match="All 4 generation attempts failed"):
            generate_image("white_boy_teen", "asking for help")


def test_generate_image_raises_for_unknown_character():
    with pytest.raises(ValueError, match="Unknown character_id"):
        generate_image("nonexistent_character", "some scenario")


def test_generate_image_raises_when_no_images_returned():
    with patch("app.generator.fal_client.run", return_value={"images": []}):
        with pytest.raises(GenerationError):
            generate_image("hispanic_girl_child", "sharing with a friend")
