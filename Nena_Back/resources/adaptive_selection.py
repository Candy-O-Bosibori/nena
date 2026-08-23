"""Adaptive selection endpoints for next practice and trends."""
from datetime import datetime, timedelta, timezone

from flask import make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from sqlalchemy import func, and_

from models import db, Recording, Feedback, Topic, Mode


class NextPractice(Resource):
    """Recommend next practice topic based on recent performance."""

    # Map focus areas to human-readable reason phrases
    FOCUS_REASONS = {
        "structure": "Targeting: improve organization and flow",
        "concision": "Targeting: get to your point faster",
        "conviction": "Targeting: speak with more confidence",
        "concreteness": "Targeting: use more specific examples",
        "pacing": "Targeting: slow down and let ideas land",
        "storytelling": "Targeting: build a stronger narrative",
        "technical-clarity": "Targeting: explain complex ideas more clearly",
    }

    @jwt_required()
    def get(self):
        """Get recommended next practice topic.

        Returns:
            {
                "topic": { topic data },
                "mode": { mode data },
                "reason": "Targeting: ...",
                "is_random": false  # true if no recommendation yet
            }
        """
        user_id = get_jwt_identity()

        # Find most recent feedback with next_topic_id
        recent_feedback = (
            Feedback.query.join(Recording)
            .filter(Recording.user_id == user_id)
            .filter(Feedback.next_topic_id.isnot(None))
            .order_by(Feedback.created_at.desc())
            .first()
        )

        if recent_feedback and recent_feedback.next_topic_id:
            topic = Topic.query.get(recent_feedback.next_topic_id)
            if topic:
                mode = Mode.query.get(topic.mode_id)
                reason = self.FOCUS_REASONS.get(
                    recent_feedback.focus_area,
                    "Targeting: improve your speaking skills"
                )
                return make_response({
                    "topic": topic.to_dict(),
                    "mode": mode.to_dict() if mode else None,
                    "reason": reason,
                    "is_random": False
                }, 200)

        # No targeted recommendation yet - return random topic
        random_topic = Topic.query.filter_by(active=True).order_by(func.random()).first()
        if random_topic:
            mode = Mode.query.get(random_topic.mode_id)
            return make_response({
                "topic": random_topic.to_dict(),
                "mode": mode.to_dict() if mode else None,
                "reason": "No specific recommendation yet — here's a random prompt to practice",
                "is_random": True
            }, 200)

        return make_response({"error": "No topics available"}, 404)


class Trends(Resource):
    """Get 30-day performance trends."""

    @jwt_required()
    def get(self):
        """Get user's 30-day trends grouped by day.

        Returns:
            {
                "trends": [
                    {
                        "date": "2026-08-15",
                        "pace_wpm_avg": 145.5,
                        "filler_words_avg": 1.2,
                        "hedge_count_avg": 1.8,
                        "time_to_point_seconds_avg": 1.5,
                        "concreteness_ratio_avg": 0.42,
                        "recording_count": 3
                    },
                    ...
                ],
                "summary": {
                    "pace_wpm_avg": 142.3,
                    "filler_words_avg": 1.1,
                    "hedge_count_avg": 1.9,
                    "time_to_point_seconds_avg": 1.4,
                    "concreteness_ratio_avg": 0.41
                }
            }
        """
        user_id = get_jwt_identity()

        # Query last 30 days
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

        trends_query = (
            db.session.query(
                func.date(Recording.created_at).label('date'),
                func.avg(Feedback.pace_wpm).label('pace_wpm_avg'),
                func.avg(Feedback.filler_words).label('filler_words_avg'),
                func.avg(Feedback.hedge_count).label('hedge_count_avg'),
                func.avg(Feedback.time_to_point_seconds).label('time_to_point_seconds_avg'),
                func.avg(Feedback.concreteness_ratio).label('concreteness_ratio_avg'),
                func.count(Recording.id).label('recording_count'),
            )
            .join(Feedback, Recording.id == Feedback.recording_id)
            .filter(
                and_(
                    Recording.user_id == user_id,
                    Recording.created_at >= thirty_days_ago
                )
            )
            .group_by(func.date(Recording.created_at))
            .order_by(func.date(Recording.created_at))
            .all()
        )

        # Convert to dicts
        trends = []
        all_metrics = {
            'pace_wpm': [],
            'filler_words': [],
            'hedge_count': [],
            'time_to_point_seconds': [],
            'concreteness_ratio': []
        }

        # func.avg() over an Integer column returns Decimal, which Flask serializes
        # as a JSON *string* ("1.10"). The frontend then calls .toFixed() on it and
        # crashes. Coerce every average to a real float so the API always emits
        # JSON numbers.
        def num(value):
            return round(float(value), 2) if value is not None else 0

        for row in trends_query:
            trend_dict = {
                "date": row.date.isoformat() if row.date else None,
                "pace_wpm_avg": num(row.pace_wpm_avg),
                "filler_words_avg": num(row.filler_words_avg),
                "hedge_count_avg": num(row.hedge_count_avg),
                "time_to_point_seconds_avg": num(row.time_to_point_seconds_avg),
                "concreteness_ratio_avg": num(row.concreteness_ratio_avg),
                "recording_count": int(row.recording_count or 0),
            }
            trends.append(trend_dict)

            # Accumulate for summary
            if row.pace_wpm_avg:
                all_metrics['pace_wpm'].append(row.pace_wpm_avg)
            if row.filler_words_avg:
                all_metrics['filler_words'].append(row.filler_words_avg)
            if row.hedge_count_avg:
                all_metrics['hedge_count'].append(row.hedge_count_avg)
            if row.time_to_point_seconds_avg:
                all_metrics['time_to_point_seconds'].append(row.time_to_point_seconds_avg)
            if row.concreteness_ratio_avg:
                all_metrics['concreteness_ratio'].append(row.concreteness_ratio_avg)

        # Compute summary (overall average)
        def avg(values):
            return round(float(sum(values)) / len(values), 2) if values else 0

        summary = {
            "pace_wpm_avg": avg(all_metrics['pace_wpm']),
            "filler_words_avg": avg(all_metrics['filler_words']),
            "hedge_count_avg": avg(all_metrics['hedge_count']),
            "time_to_point_seconds_avg": avg(all_metrics['time_to_point_seconds']),
            "concreteness_ratio_avg": avg(all_metrics['concreteness_ratio']),
        }

        return make_response({
            "trends": trends,
            "summary": summary
        }, 200)


def register(api):
    """Register adaptive selection endpoints."""
    api.add_resource(NextPractice, '/next-practice')
    api.add_resource(Trends, '/trends')
