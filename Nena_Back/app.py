import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from extensions import bcrypt, jwt
from models import db

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.json.compact = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(
    minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_MINUTES', 15))
)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(
    days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES_DAYS', 7))
)

migrate = Migrate(app, db)
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

from resources import auth, users, modes, topics, recordings, activity_logs, feedback, words, coaching_stream, adaptive_selection, frameworks

auth.register(api)
users.register(api)
modes.register(api)
topics.register(api)
recordings.register(api, app)
activity_logs.register(api)
feedback.register(api)
words.register(api)
coaching_stream.register(api)
adaptive_selection.register(api)
frameworks.register(api)


if __name__ == '__main__':
    app.run(debug=True)
