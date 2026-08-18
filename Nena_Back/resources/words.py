from flask import request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from models import db, Word


class Words(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        words = Word.query.filter_by(user_id=user_id).all()
        response_dict = [{"id": w.id, "word": w.word} for w in words]
        return make_response(response_dict, 200)

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data.get("word"):
            return {"error": "Word cannot be empty"}, 400

        new_word = Word(word=data["word"], user_id=user_id)

        try:
            db.session.add(new_word)
            db.session.commit()
            return {
                "message": "Word created successfully",
                "word": {"id": new_word.id, "word": new_word.word}
            }, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error", "details": str(e)}, 500
        except Exception as e:
            db.session.rollback()
            return {"error": "Unexpected error", "details": str(e)}, 500


class WordById(Resource):
    @jwt_required()
    def get(self, id):
        word = Word.query.get(id)
        if not word:
            return {"error": "Word not found"}, 404
        return {"id": word.id, "word": word.word}, 200

    @jwt_required()
    def patch(self, id):
        try:
            word = Word.query.get(id)
            if not word:
                return {"error": "Word not found"}, 404

            data = request.get_json()
            if "word" in data:
                word.word = data["word"]

            db.session.commit()
            return {"message": "Word updated successfully", "word": {"id": word.id, "word": word.word}}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error", "details": str(e)}, 500
        except Exception as e:
            return {"error": "Unexpected error", "details": str(e)}, 500

    @jwt_required()
    def delete(self, id):
        word = Word.query.get(id)
        if not word:
            return {"error": "Word not found"}, 404

        db.session.delete(word)
        db.session.commit()
        return {"message": "Word deleted successfully"}, 200


def register(api):
    api.add_resource(Words, '/words')
    api.add_resource(WordById, '/wordsById/<int:id>')
