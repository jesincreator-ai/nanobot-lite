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


## ESP32-WROOM MicroPython edition (new)
This repository also includes `esp32_nanobot.py`, a dependency-free MicroPython intent router for ESP32-WROOM. It is intentionally separate from the desktop package and uses SD knowledge files at `/sd/billi/knowledge.json`. Copy that module to the board and run it in the REPL. The mobile browser demo is `mobile_test.html`.


## SD-card wiring and database test
For a common SPI microSD module on ESP32-WROOM: SCK GPIO18, MOSI GPIO23, MISO GPIO19, CS GPIO5 (confirm your board/module; adjust pins as needed). Run `sd_mount.py` first in MicroPython. Place `knowledge.example.json` on the card as `/sd/billi/knowledge.json`. Use `esp32_nanobot.py` to query the JSON file. `mobile_test.html` lets a phone browser load the same JSON via file picker (choose the file on SD card) and search records; mobile file access is browser/OS dependent. The sample schema is a JSON array of records with `title`, `text`, `language`, and `source` fields.
