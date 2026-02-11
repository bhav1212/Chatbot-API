# Multi-user Chatbot API (FastAPI)

This is a stack-agnostic starting design with a Python API layer.

## What this API does
- Accepts `uid`, `session_id`, and `query` from your frontend.
- Proceeds only if `uid` is present and verifiable.
- Routes query processing to `backend.py` (`generate_response`).
- Keeps memory separated per `uid + session_id`.
- Deletes memory when the frontend ends the session (`/session/end`).

## Endpoints
### `POST /chat`
Request:
```json
{
  "uid": "user-123",
  "session_id": "session-abc",
  "query": "How do I reset my password?"
}
```

Response:
```json
{
  "uid": "user-123",
  "session_id": "session-abc",
  "answer": "..."
}
```

### `POST /session/end`
Request:
```json
{
  "uid": "user-123",
  "session_id": "session-abc"
}
```

Response:
```json
{
  "status": "session_cleared"
}
```

### `GET /health`
Returns health and active in-memory session count.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Production notes
- Replace `StaticUIDVerifier` with your real auth verification (JWT/OAuth/Firebase/etc).
- Move session memory to Redis if you run multiple API instances.
- Add TTL auto-expiry and rate limiting.
- Keep `backend.py` as the integration boundary for your LLM stack.
