from flask_bcrypt import Bcrypt
from app import app
from models import db, User, Mode, Recording, Feedback, ActivityLog
from sqlalchemy import text
from datetime import datetime, timezone, date
import random, re, json

bcrypt = Bcrypt(app)

def execute_sql(sql):
    """Execute raw SQL."""
    with db.engine.begin() as connection:
        connection.execute(text(sql))

# Load C1/C2 vocabulary once
with open("C1_C2_words.txt", "r", encoding="utf-8") as f:
    c1_c2_vocab = set(w.strip().lower() for w in f.readlines())

with app.app_context():
    print("Clearing and creating tables...")
    db.drop_all()
    db.create_all()

    # Create Modes (all 4 at once)
    modes = [
        Mode(name="Explain a Concept", description="Pick a topic and break it down clearly — like teaching a friend. Improves clarity, structure, and confidence in speaking."),
        Mode(name="Read Aloud", description="Share a personal experience or create a short tale. Builds narrative flow, vocabulary, and expressive speaking."),
        Mode(name="Tell A Story", description="Practice pronunciation, pacing, and tone by reading from a provided text or your own material."),
        Mode(name="Random Word", description="Get a surprise word and speak about it for 1 - 2 minutes. Boosts quick thinking and creativity.")
    ]
    db.session.add_all(modes)
    db.session.commit()

    # Create Users with encrypted passwords
    user1 = User(
        name="Alice Johnson",
        email="alice@example.com",
        password=bcrypt.generate_password_hash("liam.123!").decode('utf-8'),
        image=None
    )
    user2 = User(
        name="Bob Smith",
        email="bob@example.com",
        password=bcrypt.generate_password_hash("liam.123!").decode('utf-8'),
        image=None
    )
    db.session.add_all([user1, user2])
    db.session.commit()

    # Create Recordings + Feedback for each user
    for user in [user1, user2]:
        for i, mode in enumerate(modes, start=1):  # loop through all 4 modes
            transcription = f"This is the transcription for recording {i} by {user.name}. It contains words like abundance, accountability, and absurd."

            recording = Recording(
                video_url=f"https://example.com/video_{user.id}_{i}.mp4",
                transcription=transcription,
                created_at=datetime.now(timezone.utc),
                user_id=user.id,
                mode_id=mode.id,
                duration_minutes=random.randint(1, 10)
            )
            db.session.add(recording)
            db.session.commit()

            # Extract words from transcription
            words = re.findall(r"\w+", transcription.lower())
            used_advanced_words = [w for w in words if w in c1_c2_vocab]

            # Feedback
            feedback = Feedback(
                filler_words=random.randint(2, 10),
                pace_wpm=random.uniform(100, 150),
                 vocabulary_count=json.dumps(list(set(used_advanced_words))), 
                notes="Great effort, try reducing filler words and add more advanced vocabulary.",
                created_at=datetime.now(timezone.utc),
                recording_id=recording.id
            )
            db.session.add(feedback)

        # Activity Log
        activity_log = ActivityLog(
            user_id=user.id,
            date=date.today(),
            time_spent_minutes=random.randint(10, 60)
        )
        db.session.add(activity_log)

    db.session.commit()
    print("✅ Database seeded successfully with advanced vocabulary tracking!")
