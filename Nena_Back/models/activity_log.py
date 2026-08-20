from datetime import datetime, timezone

from sqlalchemy_serializer import SerializerMixin

from models import db


class ActivityLog(db.Model, SerializerMixin):
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    time_spent_minutes = db.Column(db.Integer, default=0)  # total time spent on app that day

    # Relationship
    user = db.relationship('User', back_populates='activity_logs')

    def update_time(self):
        """Update time_spent_minutes based on recordings for this user on this date"""
        from models.recording import Recording
        recordings_today = Recording.query.filter_by(user_id=self.user_id).filter(
            db.func.date(Recording.created_at) == self.date
        ).all()
        total_seconds = sum([r.duration_minutes for r in recordings_today])  # duration_minutes stores seconds
        self.time_spent_minutes = int(total_seconds / 60)  # Convert seconds to minutes (9k)

    serialize_rules = ('-user.activity_logs',)
