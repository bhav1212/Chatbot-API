"""In-memory multi-user session store."""

from collections import defaultdict
from threading import RLock


class SessionStore:
    """Thread-safe store keyed by uid+session_id.

    Data lifecycle:
    - messages are retained while session is active
    - deleting a session removes its memory immediately
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._sessions: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(dict)

    def get_history(self, uid: str, session_id: str) -> list[dict[str, str]]:
        with self._lock:
            if session_id not in self._sessions[uid]:
                self._sessions[uid][session_id] = []
            return list(self._sessions[uid][session_id])

    def append_turn(self, uid: str, session_id: str, user_query: str, bot_answer: str) -> None:
        with self._lock:
            if session_id not in self._sessions[uid]:
                self._sessions[uid][session_id] = []
            self._sessions[uid][session_id].append({"role": "user", "content": user_query})
            self._sessions[uid][session_id].append({"role": "assistant", "content": bot_answer})

    def clear_session(self, uid: str, session_id: str) -> bool:
        with self._lock:
            user_sessions = self._sessions.get(uid)
            if not user_sessions or session_id not in user_sessions:
                return False
            del user_sessions[session_id]
            if not user_sessions:
                del self._sessions[uid]
            return True

    def active_session_count(self) -> int:
        with self._lock:
            return sum(len(sessions) for sessions in self._sessions.values())
