from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.mode import Mode
from models.topic import Topic
from models.recording import Recording
from models.feedback import Feedback
from models.activity_log import ActivityLog
from models.word import Word

__all__ = ["db", "User", "Mode", "Topic", "Recording", "Feedback", "ActivityLog", "Word"]
