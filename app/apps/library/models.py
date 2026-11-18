"""
MYTHOS Resource Library & Knowledge Engine Data Models.
Re-exports User and UserActivityLog models and provides foundation for digital product tracking.
"""

from app.apps.courses.models import User, UserActivityLog

__all__ = ["User", "UserActivityLog"]
