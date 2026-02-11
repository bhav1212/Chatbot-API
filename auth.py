"""Authentication and UID verification helpers."""

from typing import Protocol


class UIDVerifier(Protocol):
    """Protocol for pluggable UID verification providers."""

    def verify(self, uid: str) -> bool: ...


class StaticUIDVerifier:
    """Simple verifier.

    Replace this with JWT/OAuth/Firebase/etc. verification for production.
    """

    def verify(self, uid: str) -> bool:
        return bool(uid and uid.strip())
