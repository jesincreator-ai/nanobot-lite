# Nanobot Lite

A small, deterministic, multilingual intent router for BILLI R-20. It converts text into a **safe routing decision**; it does not execute motors, GPIO, shell commands, or arbitrary tools.

## Features
- English, Tamil and Sinhala script detection and starter phrase matching.
- Explicit intent, confidence, extracted slots and confirmation requirement.
- Emergency-stop intent is classified before ordinary movement commands.
- Optional FastAPI service with health and routing endpoints.
- No model/API key required; deterministic fallback when a cloud model is unavailable.

## Install
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
```

## Use as a library
```python
from nanobot_lite import route_text

decision = route_text("stop now")
print(decision.to_dict())
# {'intent': 'emergency_stop', ...}
```

Tamil and Sinhala examples:
```python
route_text("வணக்கம்")
route_text("නවත්වන්න")
```

## Run the API
```bash
uvicorn nanobot_lite.api:app --host 127.0.0.1 --port 8781
```
- `GET /health`
- `POST /v1/route` with JSON `{"text":"stop now","session_id":"demo"}`

## Safety boundary
A route is only a recommendation for the host application. Hardware controllers must independently validate commands, enforce limits, implement a physical emergency stop, and require confirmation before motion. Never connect this router directly to an unrestricted shell or motor driver.

## BILLI integration
Call `route_text(user_text)` from the chat orchestration layer. For remote hosting, call `POST /v1/route`. Keep provider API keys and hardware credentials in the host's secret manager, not in this package.

## Tests
```bash
pytest
```

MIT licensed. See [LICENSE](LICENSE).
