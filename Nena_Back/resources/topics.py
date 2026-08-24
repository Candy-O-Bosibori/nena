import hashlib
from datetime import datetime, timedelta, timezone

from flask import request, make_response
from flask_restful import Resource
from sqlalchemy import func

from models import db, Topic, Mode, Recording


class Topics(Resource):
    def get(self):
        """Get all active topics"""
        topics = Topic.query.filter_by(active=True).all()
        response_dict = [t.to_dict() for t in topics]
        return make_response(response_dict, 200)


class TopicsRandom(Resource):
    def get(self):
        """Get a random topic with optional filters

        Query params:
        - mode: mode slug (e.g., 'random-topic')
        - difficulty: 'easy', 'medium', 'hard', or 'random'
        - tags: comma-separated tag filters (e.g., 'pacing,structure')
        """
        mode_slug = request.args.get('mode')
        difficulty = request.args.get('difficulty', 'random')
        tags_param = request.args.get('tags', '')

        # Start with active topics
        query = Topic.query.filter_by(active=True)

        # Filter by mode if provided
        if mode_slug:
            mode = Mode.query.filter_by(slug=mode_slug).first()
            if not mode:
                return {"error": f"Mode '{mode_slug}' not found"}, 404
            query = query.filter_by(mode_id=mode.id)

        # Filter by difficulty if not 'random'
        if difficulty != 'random':
            query = query.filter_by(difficulty=difficulty)

        # Filter by tags if provided
        if tags_param:
            tags_list = [t.strip() for t in tags_param.split(',')]
            # Use Postgres JSON containment operator
            for tag in tags_list:
                query = query.filter(Topic.tags.contains([tag]))

        # Random order and pick first
        topic = query.order_by(func.random()).first()

        if not topic:
            return {"error": "No matching topics found"}, 404

        return make_response(topic.to_dict(), 200)


class TopicsToday(Resource):
    def get(self):
        """Get today's Daily Reflection prompt

        Query params:
        - mode: should be 'daily-reflection' (required for this endpoint)
        """
        mode_slug = request.args.get('mode', 'daily-reflection')

        # Get the daily-reflection mode
        mode = Mode.query.filter_by(slug=mode_slug).first()
        if not mode:
            return {"error": f"Mode '{mode_slug}' not found"}, 404

        # Get all active daily-reflection topics
        topics = Topic.query.filter_by(mode_id=mode.id, active=True).all()

        if not topics:
            return {"error": "No Daily Reflection topics available"}, 404

        # Hash today's date to get a stable index
        today_str = datetime.now(timezone.utc).date().isoformat()
        hash_input = f"{today_str}:{mode.id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        index = hash_value % len(topics)

        topic = topics[index]

        return make_response(topic.to_dict(), 200)


def register(api):
    api.add_resource(Topics, '/topics')
    api.add_resource(TopicsRandom, '/topics/random')
    api.add_resource(TopicsToday, '/topics/today')
