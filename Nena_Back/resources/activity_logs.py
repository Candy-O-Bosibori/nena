from datetime import datetime, timedelta, timezone

from flask import make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from models import db, ActivityLog, Recording


class ActivityLogResource(Resource):
    @jwt_required()
    def get(self):
        """
        Get the last 7 days of activity log for the logged-in user.
        If a day has no activity, it is filled with 0 minutes.
        Ordered from oldest to newest.
        """
        user_id = get_jwt_identity()

        today = datetime.now(timezone.utc).date()
        start_date = today - timedelta(days=6)  # last 7 days including today

        dates_list = [start_date + timedelta(days=i) for i in range(7)]
        response = []

        for date in dates_list:
            log = ActivityLog.query.filter_by(user_id=user_id, date=date).first()

            if log:
                recordings_today = Recording.query.filter_by(user_id=user_id).filter(
                    db.func.date(Recording.created_at) == date
                ).all()
                total_minutes = sum([r.duration_minutes for r in recordings_today])
                log.time_spent_minutes = total_minutes
            else:
                log = ActivityLog(user_id=user_id, date=date, time_spent_minutes=0)
                db.session.add(log)

            db.session.commit()
            response.append({
                "date": date.isoformat(),
                "time_spent_minutes": log.time_spent_minutes
            })

        return make_response(response, 200)


def register(api):
    api.add_resource(ActivityLogResource, '/activity_logs')
