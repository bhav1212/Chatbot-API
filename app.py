from fastapi import FastAPI, HTTPException, status

from auth import StaticUIDVerifier
from backend import generate_response
from models import ChatRequest, ChatResponse, EndSessionRequest
from session_store import SessionStore

app = FastAPI(title="Chatbot API", version="1.0.0")

verifier = StaticUIDVerifier()
store = SessionStore()


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    if not verifier.verify(payload.uid):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UID missing or verification failed",
        )

    history = store.get_history(payload.uid, payload.session_id)
    answer = generate_response(payload.query, payload.uid, payload.session_id, history)
    store.append_turn(payload.uid, payload.session_id, payload.query, answer)

    return ChatResponse(uid=payload.uid, session_id=payload.session_id, answer=answer)


@app.post("/session/end")
def end_session(payload: EndSessionRequest) -> dict[str, str]:
    if not verifier.verify(payload.uid):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UID missing or verification failed",
        )

    cleared = store.clear_session(payload.uid, payload.session_id)
    if not cleared:
        return {"status": "session_not_found"}
    return {"status": "session_cleared"}


@app.get("/health")
def health() -> dict[str, str | int]:
    return {"status": "ok", "active_sessions": store.active_session_count()}
