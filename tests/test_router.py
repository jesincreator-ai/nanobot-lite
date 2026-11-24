import pytest

from nanobot_lite import route_text
from nanobot_lite.router import detect_language


def test_emergency_stop_has_priority_and_no_confirmation():
    result = route_text("STOP now")
    assert result.intent == "emergency_stop"
    assert result.action == "stop"
    assert result.requires_confirmation is False


def test_motion_requires_confirmation():
    result = route_text("move forward")
    assert result.intent == "motion"
    assert result.requires_confirmation is True


def test_tamil_and_sinhala_detection():
    assert detect_language("வணக்கம்") == "ta"
    assert detect_language("ආයුබෝවන්") == "si"
    assert route_text("வணக்கம்").intent == "greeting"
    assert route_text("නවත්වන්න").intent == "emergency_stop"


def test_empty_and_oversized_input_rejected():
    with pytest.raises(ValueError):
        route_text(" ")
    with pytest.raises(ValueError):
        route_text("x" * 2001)


def test_unknown_text_falls_back_to_chat():
    assert route_text("tell me a story").intent == "chat"
