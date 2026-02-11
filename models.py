from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    uid: str = Field(..., description="User id; must be present and verifiable")
    session_id: str = Field(..., description="Client session id")
    query: str = Field(..., min_length=1, description="User message text")


class ChatResponse(BaseModel):
    uid: str
    session_id: str
    answer: str


class EndSessionRequest(BaseModel):
    uid: str
    session_id: str
