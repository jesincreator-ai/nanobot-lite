"""Optional HTTP interface for Nanobot Lite."""
from fastapi import FastAPI
from pydantic import BaseModel, Field

from .router import route_text

app = FastAPI(title="Nanobot Lite", version="0.1.0")


class RouteRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    session_id: str | None = Field(default=None, max_length=128)


@app.get("/health")
def health() -> dict[str, str]:
    return {"service": "nanobot-lite", "status": "ok", "mode": "deterministic"}


@app.post("/v1/route")
def route(request: RouteRequest) -> dict:
    return {"session_id": request.session_id, "decision": route_text(request.text).to_dict()}
