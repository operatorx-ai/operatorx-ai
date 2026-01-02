from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MemoryRecord:
    """
    Represents request-scoped memory for OperatorX AI.

    Why this exists (Phase 2):
    - Provides a shared "context container" for the engine/agents
    - Enables traceability (what happened during a request)
    - Scaffolds future persistent memory layers (Redis/Postgres/etc.)

    Important:
    - This is NOT long-term memory yet
    - This is a lightweight foundation to support later phases
    """
    # Unique request identifier (comes from RequestIdMiddleware)
    request_id: str

    # Deployment tier for this request (personal/business/government)
    tier: str

    # Creation/update timestamps for debugging + future audit usefulness
    created_at: float = field(default_factory=lambda: time.time())
    updated_at: float = field(default_factory=lambda: time.time())

    # Arbitrary structured memory payload
    # Example future keys: last_agent, last_output, errors, metrics, etc.
    data: Dict[str, Any] = field(default_factory=dict)


class InMemoryStore:
    """
    Tiny in-memory store keyed by request_id.

    Why it exists (Phase 2):
    - Fast and simple
    - Allows us to prove end-to-end context flow
    - Keeps architecture clean while the platform is early-stage

    Limitations (known + acceptable for now):
    - Not persistent (restarts lose memory)
    - Not safe for multi-process or multi-server deployments
    - Intended for local development + scaffolding only
    """

    def __init__(self) -> None:
        # Internal storage: request_id -> MemoryRecord
        self._store: Dict[str, MemoryRecord] = {}

    def get(self, request_id: str) -> Optional[MemoryRecord]:
        """
        Fetch a memory record by request_id.

        Returns None if not found.
        """
        return self._store.get(request_id)

    def upsert(self, record: MemoryRecord) -> MemoryRecord:
        """
        Insert or update a MemoryRecord.

        We update updated_at every time to track changes over time.
        """
        record.updated_at = time.time()
        self._store[record.request_id] = record
        return record

    def ensure(self, request_id: str, tier: str) -> MemoryRecord:
        """
        Ensure a record exists for this request_id.

        If it exists, return it.
        If it does not exist, create it and store it.
        """
        existing = self.get(request_id)
        if existing:
            return existing

        # Create a new record if nothing exists yet
        return self.upsert(MemoryRecord(request_id=request_id, tier=tier))


# ------------------------------------------------------------
# Singleton Store (shared across the backend process)
# ------------------------------------------------------------
# The engine and routes import and use this shared instance.
# In future phases, this can be swapped for a persistent store
# without changing the API layer.
memory_store = InMemoryStore()
