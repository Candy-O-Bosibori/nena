import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models import db, Topic, Mode

with app.app_context():
    print("Seeding topics...")

    # Get modes
    random_topic_mode = Mode.query.filter_by(slug='random-topic').first()
    interview_prep_mode = Mode.query.filter_by(slug='interview-prep').first()
    learn_vocab_mode = Mode.query.filter_by(slug='learn-vocab').first()
    read_aloud_mode = Mode.query.filter_by(slug='read-aloud').first()
    daily_reflection_mode = Mode.query.filter_by(slug='daily-reflection').first()

    # Random Topic (10 prompts)
    random_topics = [
        Topic(
            mode_id=random_topic_mode.id,
            text="What's a skill you'd like to learn in the next year and why?",
            difficulty='easy',
            tags=['general', 'structure', 'pacing'],
            meta={}
        ),
        Topic(
            mode_id=random_topic_mode.id,
            text="Explain how you would design a coffee shop from scratch.",
            difficulty='easy',
            tags=['general', 'structure', 'concreteness'],
            meta={}
        ),
        Topic(
            mode_id=random_topic_mode.id,
            text="What's the most interesting thing you learned this week?",
            difficulty='easy',
            tags=['general', 'storytelling', 'conviction'],
            meta={}
        ),
        Topic(
            mode_id=random_topic_mode.id,
            text="If you could have dinner with anyone, who would it be and what would you ask?",
            difficulty='easy',
            tags=['general', 'storytelling', 'pacing'],
            meta={}
        ),
        Topic(
            mode_id=random_topic_mode.id,
            text="How would you explain artificial intelligence to someone who's never heard of it?",
            difficulty='medium',
            tags=['tech', 'technical-clarity', 'concision'],
            meta={}
        ),
        Topic(
            mode_id=random_topic_mode.id,
            text="What's the biggest challenge in your current work or studies?",
            difficulty='medium',
            tags=['work', 'structure', 'conviction'],
            meta={}
        ),
        Topic(
            mode_id=random_topic_mode.id,
            text="Describe a time when you had to solve a problem creatively.",
            difficulty='medium',
            tags=['work', 'storytelling', 'concreteness'],
            meta={}
        ),
        Topic(
            mode_id=random_topic_mode.id,
            text="What ethical issue concerns you most in technology?",
            difficulty='hard',
            tags=['tech', 'conviction', 'structure'],
            meta={}
        ),
        Topic(
            mode_id=random_topic_mode.id,
            text="How would you convince someone that remote work is effective?",
            difficulty='hard',
            tags=['work', 'technical-clarity', 'conviction'],
            meta={}
        ),
        Topic(
            mode_id=random_topic_mode.id,
            text="Discuss how you approach learning new technologies.",
            difficulty='hard',
            tags=['tech', 'structure', 'conciseness'],
            meta={}
        ),
    ]

    # Interview Prep (10 questions)
    interview_topics = [
        Topic(
            mode_id=interview_prep_mode.id,
            text="Tell me about a time you had to work with a difficult team member.",
            difficulty='easy',
            tags=['behavioral', 'structure', 'pacing'],
            meta={'suggested_framework': 'STAR'}
        ),
        Topic(
            mode_id=interview_prep_mode.id,
            text="Describe a project you're proud of and what your role was.",
            difficulty='easy',
            tags=['project', 'storytelling', 'concreteness'],
            meta={'suggested_framework': 'STAR'}
        ),
        Topic(
            mode_id=interview_prep_mode.id,
            text="How do you prioritize tasks when everything feels urgent?",
            difficulty='medium',
            tags=['behavioral', 'technical-clarity', 'conviction'],
            meta={'suggested_framework': 'STAR'}
        ),
        Topic(
            mode_id=interview_prep_mode.id,
            text="Walk me through the architecture of a system you built.",
            difficulty='medium',
            tags=['project', 'technical-clarity', 'structure'],
            meta={'suggested_framework': 'PREP'}
        ),
        Topic(
            mode_id=interview_prep_mode.id,
            text="Tell me about a time you failed and what you learned.",
            difficulty='medium',
            tags=['behavioral', 'storytelling', 'conviction'],
            meta={'suggested_framework': 'STAR'}
        ),
        Topic(
            mode_id=interview_prep_mode.id,
            text="Explain your most complex technical achievement to a non-engineer.",
            difficulty='hard',
            tags=['project', 'technical-clarity', 'concision'],
            meta={'suggested_framework': 'PREP'}
        ),
        Topic(
            mode_id=interview_prep_mode.id,
            text="Describe a conflict with a colleague and how you resolved it.",
            difficulty='hard',
            tags=['behavioral', 'structure', 'concreteness'],
            meta={'suggested_framework': 'STAR'}
        ),
        Topic(
            mode_id=interview_prep_mode.id,
            text="What would you do differently in your last major project?",
            difficulty='hard',
            tags=['project', 'conviction', 'storytelling'],
            meta={'suggested_framework': 'PREP'}
        ),
        Topic(
            mode_id=interview_prep_mode.id,
            text="How do you stay current with new technologies?",
            difficulty='medium',
            tags=['behavioral', 'pacing', 'conviction'],
            meta={'suggested_framework': 'STAR'}
        ),
        Topic(
            mode_id=interview_prep_mode.id,
            text="Tell me about a time you had to learn something quickly under pressure.",
            difficulty='hard',
            tags=['behavioral', 'storytelling', 'structure'],
            meta={'suggested_framework': 'STAR'}
        ),
    ]

    # Learn Vocabulary (10 words)
    vocab_topics = [
        Topic(
            mode_id=learn_vocab_mode.id,
            text="pragmatic",
            difficulty='easy',
            tags=['vocabulary', 'concision'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'dealing with things in a practical, realistic way based on actual circumstances',
                'example_sentence': 'We took a pragmatic approach to solving the budget issue.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="substantive",
            difficulty='easy',
            tags=['vocabulary', 'concreteness'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'of real importance or value; having solid basis in reality',
                'example_sentence': 'The team made substantive progress on the project this quarter.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="meticulous",
            difficulty='medium',
            tags=['vocabulary', 'structure'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'showing great attention to detail; very careful and precise',
                'example_sentence': 'Her meticulous planning ensured the event ran smoothly.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="articulate",
            difficulty='medium',
            tags=['vocabulary', 'pacing'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to express clearly and effectively in speech',
                'example_sentence': 'She was able to articulate the team\'s concerns to management.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="juxtapose",
            difficulty='medium',
            tags=['vocabulary', 'technical-clarity'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to place two things side by side, usually for contrast',
                'example_sentence': 'The designer juxtaposed traditional and modern styles in the layout.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="circumvent",
            difficulty='hard',
            tags=['vocabulary', 'concision'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to find a way around an obstacle or rule',
                'example_sentence': 'They tried to circumvent the policy by finding a loophole.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="reciprocal",
            difficulty='hard',
            tags=['vocabulary', 'structure'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'given or done by each side to the other; mutual',
                'example_sentence': 'The two companies established a reciprocal agreement to share resources.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="efficacious",
            difficulty='hard',
            tags=['vocabulary', 'conviction'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'successful in producing the desired result; effective',
                'example_sentence': 'The new training program proved efficacious in reducing errors.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="ambiguous",
            difficulty='easy',
            tags=['vocabulary', 'clarity'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'open to more than one interpretation; not clear',
                'example_sentence': 'The instructions were so ambiguous that no one understood them.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="resilient",
            difficulty='medium',
            tags=['vocabulary', 'conviction'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'able to recover quickly from difficulties; tough',
                'example_sentence': 'The resilient team bounced back from the project setback.'
            }
        ),
    ]

    # Read Aloud (10 original passages)
    read_aloud_topics = [
        Topic(
            mode_id=read_aloud_mode.id,
            text="The morning light filtered through the tall windows, casting long shadows across the wooden floor. Sarah sat at her desk, reviewing the proposal one more time. Every detail mattered today. The deadline was noon, and she had exactly three hours to send it.",
            difficulty='easy',
            tags=['narrative', 'pacing'],
            meta={
                'word_count': 50,
                'target_seconds': 21
            }
        ),
        Topic(
            mode_id=read_aloud_mode.id,
            text="\"Are you ready?\" he asked, checking his watch. \"Almost,\" she replied, gathering her notes. The presentation was in five minutes, but she felt prepared. All those late nights of practice had paid off. She took a deep breath and stood up.",
            difficulty='easy',
            tags=['dialogue', 'pacing'],
            meta={
                'word_count': 47,
                'target_seconds': 19
            }
        ),
        Topic(
            mode_id=read_aloud_mode.id,
            text="The system processes data in three distinct phases: collection, analysis, and reporting. First, raw data enters through multiple API endpoints. Next, the data is cleaned and normalized. Finally, reports are generated for stakeholder review. This pipeline runs automatically every four hours.",
            difficulty='medium',
            tags=['technical', 'clarity'],
            meta={
                'word_count': 55,
                'target_seconds': 22
            }
        ),
        Topic(
            mode_id=read_aloud_mode.id,
            text="The project timeline is as follows: Phase One runs from January through March, covering design and planning. Phase Two, spanning April to June, handles development and testing. Phase Three, July through August, focuses on deployment and refinement. We anticipate completion by September 30th.",
            difficulty='medium',
            tags=['numeric', 'structure'],
            meta={
                'word_count': 53,
                'target_seconds': 21
            }
        ),
        Topic(
            mode_id=read_aloud_mode.id,
            text="She had visited three countries that year: Japan in spring, Portugal in summer, and Iceland in fall. Each trip taught her something new about herself. Japan showed her the value of precision. Portugal revealed her love for spontaneity. Iceland reminded her to appreciate silence.",
            difficulty='medium',
            tags=['narrative', 'storytelling'],
            meta={
                'word_count': 50,
                'target_seconds': 20
            }
        ),
        Topic(
            mode_id=read_aloud_mode.id,
            text="The warm breeze carried the scent of jasmine through the courtyard. Children played in the fountain's spray, their laughter echoing off the stone walls. An elderly man sat in the shade, reading a newspaper. Time moved slowly here, as though the world outside didn't exist. It was perfect.",
            difficulty='easy',
            tags=['descriptive', 'warmth'],
            meta={
                'word_count': 52,
                'target_seconds': 21
            }
        ),
        Topic(
            mode_id=read_aloud_mode.id,
            text="The algorithm processes 50,000 transactions per second. Each transaction is validated against 15 separate criteria. Invalid transactions are flagged immediately and logged for review. Approximately 0.03 percent of all transactions fail validation. The system alerts administrators when this rate exceeds 0.1 percent.",
            difficulty='hard',
            tags=['technical', 'numeric'],
            meta={
                'word_count': 51,
                'target_seconds': 20
            }
        ),
        Topic(
            mode_id=read_aloud_mode.id,
            text="The meeting ran later than expected, which meant missing lunch entirely. By three o'clock, exhaustion had set in. The conference room felt stuffy. Despite the challenges, the team had made real progress. Tomorrow would bring new obstacles, but today felt like a small victory.",
            difficulty='hard',
            tags=['narrative', 'reflection'],
            meta={
                'word_count': 49,
                'target_seconds': 20
            }
        ),
        Topic(
            mode_id=read_aloud_mode.id,
            text="She instructed without emotion, clearly and directly. \"First, disconnect the power. Second, remove the three bolts from the back panel. Third, carefully extract the old component. Finally, install the replacement unit and verify operation before reassembling.\" Her precision left no room for misunderstanding.",
            difficulty='hard',
            tags=['instructional', 'clarity'],
            meta={
                'word_count': 54,
                'target_seconds': 22
            }
        ),
        Topic(
            mode_id=read_aloud_mode.id,
            text="The decision came down to three factors: cost, timeline, and quality. We couldn't optimize all three simultaneously. We chose to prioritize quality and timeline over cost. This meant the budget would increase by twenty percent. The stakeholders agreed this was the right trade-off.",
            difficulty='medium',
            tags=['decision', 'structure'],
            meta={
                'word_count': 50,
                'target_seconds': 20
            }
        ),
    ]

    # Daily Reflection (10 prompts)
    daily_reflection_topics = [
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What was one thing that went better than expected today?",
            difficulty='easy',
            tags=['reflection', 'pacing'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What skill did you use today that you're proud of?",
            difficulty='easy',
            tags=['reflection', 'conviction'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What decision did you make today, and would you make it again?",
            difficulty='medium',
            tags=['reflection', 'structure'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="If you could change one thing about today, what would it be?",
            difficulty='medium',
            tags=['reflection', 'storytelling'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What conversation did you have today that meant something to you?",
            difficulty='easy',
            tags=['reflection', 'pacing'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="How did you show up authentically today?",
            difficulty='hard',
            tags=['reflection', 'conviction'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What challenged you today, and what did you learn from it?",
            difficulty='medium',
            tags=['reflection', 'structure'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What moment of joy or humor did you experience today?",
            difficulty='easy',
            tags=['reflection', 'pacing'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="Who did you help today, and how did it make you feel?",
            difficulty='medium',
            tags=['reflection', 'conviction'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What are you grateful for at the end of this day?",
            difficulty='easy',
            tags=['reflection', 'pacing'],
            meta={}
        ),
    ]

    # Combine all topics
    all_topics = random_topics + interview_topics + vocab_topics + read_aloud_topics + daily_reflection_topics

    # Check if topics already exist to make this idempotent
    existing_count = Topic.query.count()
    if existing_count == 0:
        print(f"Inserting {len(all_topics)} topics...")
        db.session.add_all(all_topics)
        db.session.commit()
        print(f"✅ Successfully seeded {len(all_topics)} topics!")
    else:
        print(f"Topics already exist ({existing_count} found). Skipping seed to avoid duplicates.")

    # Verify by mode
    for mode in [random_topic_mode, interview_prep_mode, learn_vocab_mode, read_aloud_mode, daily_reflection_mode]:
        count = Topic.query.filter_by(mode_id=mode.id).count()
        print(f"  {mode.name}: {count} topics")
