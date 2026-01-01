# OperatorX AI — API Reference (Phase 1)
Base URL: `http://127.0.0.1:8000`
## Health
- `GET /api/v1/health` → `{ "status": "ok" }`
## Meta
- `GET /api/v1/meta` → service metadata
## Tier Debug
- `GET /api/v1/tier`
 - Optional header: `X-OperatorX-Tier: personal|business|government`
## Agents
- `GET /api/v1/agents` → list registered agents
- `POST /api/v1/agents/orchestrate`
 - Header: `X-OperatorX-Tier` (optional)
 - Body:
   ```json
   {"goal":"...","constraints":["..."]}
   ```
 - Returns:
   ```json
   {"plan":["..."]}
   ```
## Request ID
All responses include `X-Request-Id`.
Clients may provide `X-Request-Id` to reuse an existing trace id.
