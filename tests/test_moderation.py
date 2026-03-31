import os
from unittest.mock import patch, MagicMock

import pytest

os.environ.setdefault("OPENAI_API_KEY", "test-openai-key")

from app.moderation import check_scenario, ModerationError


def _make_moderation_response(flagged: bool, flagged_categories: list[str] = None):
    """Build a mock OpenAI moderation response."""
    categories = {
        "hate": False,
        "hate/threatening": False,
        "harassment": False,
        "harassment/threatening": False,
        "self-harm": False,
        "self-harm/intent": False,
        "self-harm/instructions": False,
        "sexual": False,
        "sexual/minors": False,
        "violence": False,
        "violence/graphic": False,
    }
    if flagged_categories:
        for cat in flagged_categories:
            if cat in categories:
                categories[cat] = True

    mock_result = MagicMock()
    mock_result.flagged = flagged
    mock_result.categories.model_dump.return_value = categories

    mock_response = MagicMock()
    mock_response.results = [mock_result]
    return mock_response


def test_safe_scenario_does_not_raise():
    with patch("app.moderation._get_client") as mock_client:
        mock_client.return_value.moderations.create.return_value = \
            _make_moderation_response(flagged=False)
        check_scenario("crying after being told to wait")  # should not raise


def test_flagged_scenario_raises_moderation_error():
    with patch("app.moderation._get_client") as mock_client:
        mock_client.return_value.moderations.create.return_value = \
            _make_moderation_response(flagged=True, flagged_categories=["violence"])
        with pytest.raises(ModerationError) as exc_info:
            check_scenario("something violent")
        assert "violence" in exc_info.value.categories


def test_moderation_error_includes_all_flagged_categories():
    with patch("app.moderation._get_client") as mock_client:
        mock_client.return_value.moderations.create.return_value = \
            _make_moderation_response(flagged=True, flagged_categories=["hate", "harassment"])
        with pytest.raises(ModerationError) as exc_info:
            check_scenario("hateful harassment")
        assert "hate" in exc_info.value.categories
        assert "harassment" in exc_info.value.categories
