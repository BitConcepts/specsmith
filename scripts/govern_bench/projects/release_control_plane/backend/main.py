"""Starter release API with deliberate fresh-repository gaps."""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="Release Control Plane")


@app.get("/health")
def health() -> dict[str, str]:
    """Return the stable liveness contract."""
    return {"status": "ok"}


# T29 intentionally starts without the release model, store, or product routes.
