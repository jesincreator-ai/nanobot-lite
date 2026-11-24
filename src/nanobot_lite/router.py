"""Deterministic, safe-by-default intent classification."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any


@dataclass(frozen=True)
class RouteDecision:
    intent: str
    language: str
    confidence: float
    action: str | None = None
    requires_confirmation: bool = False
    slots: dict[str, str] | None = None
    reply: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_PATTERNS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("emergency_stop", "en", (r"\bstop\b", r"\bemergency stop\b", r"\bhalt\b", r"\bfreeze\b")),
    ("emergency_stop", "ta", ("நிறுத்து", "நிறுத்துங்கள்", "அவசரமாக நிறுத்து")),
    ("emergency_stop", "si", ("නවත්වන්න", "නවත්වන්නකෝ", "හදිසි නවත්වන්න")),
    ("greeting", "en", (r"\b(hello|hi|hey|good morning|good evening)\b",)),
    ("greeting", "ta", ("வணக்கம்", "ஹலோ")),
    ("greeting", "si", ("ආයුබෝවන්", "හෙලෝ")),
    ("status", "en", (r"\b(status|battery|how are you|diagnostic)\b",)),
    ("status", "ta", ("நிலை", "மின்கலம்", "பேட்டரி")),
    ("status", "si", ("තත්ත්වය", "බැටරි")),
    ("motion", "en", (r"\b(move|go|forward|backward|turn left|turn right)\b",)),
    ("motion", "ta", ("முன்னால் செல்", "பின்னால் செல்", "இடது பக்கம் திரும்பு", "வலது பக்கம் திரும்பு")),
    ("motion", "si", ("ඉදිරියට යන්න", "පස්සට යන්න", "වමට හැරෙන්න", "දකුණට හැරෙන්න")),
    ("device_control", "en", (r"\b(turn on|turn off|switch on|switch off|open|close)\b",)),
    ("device_control", "ta", ("இயக்கு", "அணை", "திற", "மூடு")),
    ("device_control", "si", ("ක්‍රියාත්මක කරන්න", "නිවා දමන්න", "අරින්න", "වහන්න")),
)


def detect_language(text: str) -> str:
    """Best-effort script detection; returns en when no supported script is found."""
    if re.search(r"[\u0B80-\u0BFF]", text):
        return "ta"
    if re.search(r"[\u0D80-\u0DFF]", text):
        return "si"
    return "en"


def _reply(intent: str, language: str) -> str:
    replies = {
        "greeting": {"en": "Hello! How can I help?", "ta": "வணக்கம்! நான் எப்படி உதவலாம்?", "si": "ආයුබෝවන්! මම කෙසේ උදව් කරන්නද?"},
        "emergency_stop": {"en": "Stop request recognized. Hardware safety stop must still be enforced by the controller.", "ta": "நிறுத்தும் கோரிக்கை அடையாளம் காணப்பட்டது.", "si": "නැවැත්වීමේ ඉල්ලීම හඳුනාගත්තා."},
        "status": {"en": "I can check status when the hardware status service is connected.", "ta": "வன்பொருள் சேவை இணைக்கப்பட்டால் நிலையைச் சரிபார்க்கலாம்.", "si": "දෘඩාංග සේවාව සම්බන්ධ කළ විට තත්ත්වය පරීක්ෂා කළ හැක."},
        "motion": {"en": "Motion request recognized. Confirm it in the hardware controller before moving.", "ta": "இயக்கக் கோரிக்கை அடையாளம் காணப்பட்டது; இயக்குவதற்கு முன் உறுதிப்படுத்தவும்.", "si": "චලන ඉල්ලීම හඳුනාගත්තා; චලනයට පෙර තහවුරු කරන්න."},
        "device_control": {"en": "Device-control request recognized. A trusted controller must validate it.", "ta": "சாதனக் கட்டுப்பாட்டு கோரிக்கை அடையாளம் காணப்பட்டது.", "si": "උපාංග පාලන ඉල්ලීම හඳුනාගත්තා."},
        "chat": {"en": "I understand. Tell me a little more.", "ta": "புரிகிறது. இன்னும் கொஞ்சம் விளக்குங்கள்.", "si": "මට තේරෙනවා. තව ටිකක් කියන්න."},
    }
    return replies[intent][language]


def route_text(text: str) -> RouteDecision:
    """Classify a user utterance without executing any external action."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    cleaned = " ".join(text.strip().split())
    if not cleaned:
        raise ValueError("text must not be empty")
    if len(cleaned) > 2000:
        raise ValueError("text must be 2000 characters or fewer")

    language = detect_language(cleaned)
    folded = cleaned.casefold()

    for intent, lang, patterns in _PATTERNS:
        if lang != language:
            continue
        if any(re.search(pattern, folded, flags=re.IGNORECASE) for pattern in patterns):
            confirmation = intent in {"motion", "device_control"}
            confidence = 0.98 if intent == "emergency_stop" else 0.88
            action = "stop" if intent == "emergency_stop" else None
            return RouteDecision(
                intent=intent, language=language, confidence=confidence,
                action=action, requires_confirmation=confirmation,
                slots={}, reply=_reply(intent, language),
            )

    return RouteDecision(
        intent="chat", language=language, confidence=0.5,
        requires_confirmation=False, slots={}, reply=_reply("chat", language),
    )
