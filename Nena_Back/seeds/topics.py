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

        # --- Hot takes / opinions (easy-medium, everyday low-stakes) ---
        Topic(mode_id=random_topic_mode.id, text="Homework should be doubled for every student.", difficulty='easy', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Naps are more productive than coffee.", difficulty='easy', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Using a map app is cheating at navigation.", difficulty='easy', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Cereal is a soup.", difficulty='easy', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Pineapple belongs on pizza and the debate is over.", difficulty='easy', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Everyone should be required to learn one dead language.", difficulty='medium', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Weekends should be three days and workdays ten hours.", difficulty='medium', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Children should be allowed to vote at twelve.", difficulty='medium', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Autocorrect has made us better writers.", difficulty='easy', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Handwriting should be removed from school entirely.", difficulty='medium', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Talking to yourself in public should be normalized.", difficulty='easy', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Movie spoilers make films better.", difficulty='easy', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Elevators should have no buttons -- they just go where they want.", difficulty='easy', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Birthdays should be celebrated once every five years.", difficulty='medium', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="All sports should ban scorekeeping.", difficulty='medium', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Socks with sandals is the peak of footwear engineering.", difficulty='easy', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Cities should ban all clocks in public spaces.", difficulty='medium', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Reading the last page first is the correct way to read a novel.", difficulty='easy', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Group projects prepare you for life better than exams do.", difficulty='medium', tags=['opinion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Everyone should have to give a public speech once a year by law.", difficulty='medium', tags=['opinion', 'conviction', 'structure'], meta={}),

        # --- Explain it clearly (medium-hard, technical-clarity) ---
        Topic(mode_id=random_topic_mode.id, text="Explain what a glass child is.", difficulty='medium', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text='Explain why the sky is blue, without using the word "light."', difficulty='hard', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain how a refrigerator makes cold.", difficulty='medium', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain what inflation actually is, to a ten-year-old.", difficulty='medium', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain why leap years exist.", difficulty='medium', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text='Explain what "the algorithm" means when people say it.', difficulty='medium', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain how to tie shoelaces -- with no hand gestures.", difficulty='hard', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain what a black hole is, in under 90 seconds.", difficulty='hard', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain why bread rises.", difficulty='medium', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain what imposter syndrome feels like.", difficulty='easy', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain how the internet physically moves information.", difficulty='hard', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain what a credit score is and why anyone should care.", difficulty='medium', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain why we get hiccups.", difficulty='medium', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain what sarcasm is, to someone who has never encountered it.", difficulty='medium', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain how vaccines work, using only a metaphor.", difficulty='hard', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain what deja vu is.", difficulty='medium', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain why the ocean is salty but rivers aren't.", difficulty='medium', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text='Explain what "opportunity cost" means, using your own morning as the example.', difficulty='hard', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain how a search engine decides what to show you.", difficulty='hard', tags=['technical-clarity', 'concision', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain what phantom vibration syndrome is.", difficulty='easy', tags=['technical-clarity', 'concision', 'structure'], meta={}),

        # --- Sell it (medium-hard, persuasion) ---
        Topic(mode_id=random_topic_mode.id, text="Sell a dog walking service where the dog walks you.", difficulty='medium', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Sell umbrellas to people who live in the desert.", difficulty='hard', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Sell a blank notebook, for $200.", difficulty='hard', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Sell silence, as a paid subscription.", difficulty='hard', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Pitch a restaurant with only one item on the menu -- you pick the item and pitch it.", difficulty='medium', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Sell winter, to someone who has only lived in the tropics.", difficulty='medium', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Sell a haunted house as a family home.", difficulty='hard', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Pitch your childhood hometown to a tourist board.", difficulty='medium', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Sell a rock as a pet.", difficulty='medium', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Sell yourself, as a contestant on a reality show you invent on the spot.", difficulty='hard', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Sell a gym that's only open between 3 and 5 a.m.", difficulty='medium', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Sell boredom, as a wellness product.", difficulty='hard', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Sell a time machine that only goes back four minutes.", difficulty='hard', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Sell left-handed scissors to a right-handed audience.", difficulty='medium', tags=['persuasion', 'conviction', 'structure'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Sell a cookbook with no recipes.", difficulty='hard', tags=['persuasion', 'conviction', 'structure'], meta={}),

        # --- Tell a story (easy-medium, storytelling) ---
        Topic(mode_id=random_topic_mode.id, text="Tell the story of the worst haircut you ever had.", difficulty='easy', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Tell a story about a time you were completely, confidently wrong.", difficulty='easy', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Tell the story of the last time you laughed until you couldn't breathe.", difficulty='easy', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Describe your morning as a nature documentary narrator.", difficulty='medium', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Tell the story of a meal you'll never forget -- good or bad.", difficulty='easy', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Tell the story of an object in the room you're in right now.", difficulty='medium', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Tell the story of a time you got lost.", difficulty='easy', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Retell a fairy tale from the villain's point of view.", difficulty='medium', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Tell the story of the most boring day of your life, made to sound thrilling.", difficulty='medium', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Tell the story of a conversation you overheard and couldn't stop thinking about.", difficulty='medium', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Describe a photograph you've never seen.", difficulty='medium', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Tell the story of the first time you were trusted with something important.", difficulty='easy', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Tell the story of a rule you broke and don't regret.", difficulty='easy', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Narrate a sports match between two household appliances.", difficulty='medium', tags=['storytelling', 'pacing', 'concreteness'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Tell the origin story of your own name -- real or invented.", difficulty='easy', tags=['storytelling', 'pacing', 'concreteness'], meta={}),

        # --- Hot takes and open questions (medium, nuance) ---
        Topic(mode_id=random_topic_mode.id, text="Is it ever okay to lie to a friend?", difficulty='medium', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Should tipping be abolished?", difficulty='medium', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Is being on time a moral issue?", difficulty='medium', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="What's overrated that everyone loves?", difficulty='easy', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Does anyone actually need more than 500 words of vocabulary?", difficulty='medium', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Should schools teach cooking instead of calculus?", difficulty='medium', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Is nostalgia dangerous?", difficulty='hard', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="What's the most useless invention of the last century?", difficulty='easy', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Can a machine be creative?", difficulty='hard', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Is it rude to cancel plans by text?", difficulty='easy', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Should famous people have privacy?", difficulty='medium', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="What's a tradition worth ending?", difficulty='medium', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Is patience actually a virtue or just slow decision-making?", difficulty='hard', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Do we owe strangers politeness?", difficulty='medium', tags=['opinion', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="What's something you changed your mind about?", difficulty='easy', tags=['opinion', 'nuance', 'conviction'], meta={}),

        # --- Strange scenarios (hard, improvisation) ---
        Topic(mode_id=random_topic_mode.id, text="You must explain to aliens why humans keep pets.", difficulty='hard', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="You're a lawyer defending a cat accused of knocking a glass off a table.", difficulty='hard', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Give a eulogy for a pair of shoes.", difficulty='medium', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="You're a tour guide for a completely empty room.", difficulty='medium', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Give a wedding toast for two people you've never met.", difficulty='hard', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="You've just invented the wheel -- pitch it to your village.", difficulty='hard', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Congratulate someone on an achievement you don't understand.", difficulty='medium', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text='Talk for two minutes without using the letter "s."', difficulty='hard', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="You're a weather forecaster for a planet with no weather.", difficulty='medium', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Apologize for something you didn't do, convincingly.", difficulty='medium', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Give a motivational speech to a houseplant that's dying.", difficulty='medium', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="You're a museum guide describing the contents of your own pockets.", difficulty='medium', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Deliver breaking news about a very small event.", difficulty='medium', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="You're a translator between two people who speak the same language.", difficulty='hard', tags=['improvisation', 'pacing', 'conviction'], meta={}),
        Topic(mode_id=random_topic_mode.id, text="Explain today's date to someone who has never encountered a calendar.", difficulty='hard', tags=['improvisation', 'pacing', 'conviction'], meta={}),
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

        # --- Walk me through your work (12) ---
        Topic(mode_id=interview_prep_mode.id, text="Tell me about a project you're proud of. Start with what it does, not how you built it.", difficulty='medium', tags=['walk-through-work', 'structure', 'concreteness'], meta={'suggested_framework': 'PREP'}),
        Topic(mode_id=interview_prep_mode.id, text="Explain your most recent project to someone non-technical.", difficulty='medium', tags=['walk-through-work', 'technical-clarity', 'concision'], meta={'suggested_framework': 'PREP'}),
        Topic(mode_id=interview_prep_mode.id, text="Now explain the same project to the engineer who'd maintain it.", difficulty='medium', tags=['walk-through-work', 'technical-clarity', 'structure'], meta={'suggested_framework': 'PREP'}),
        Topic(mode_id=interview_prep_mode.id, text="What was the hardest technical decision on that project, and what did you choose against?", difficulty='hard', tags=['walk-through-work', 'conviction', 'concreteness'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Why did you pick that stack?", difficulty='medium', tags=['walk-through-work', 'conviction', 'concreteness'], meta={'suggested_framework': 'PREP'}),
        Topic(mode_id=interview_prep_mode.id, text="What part of that project did you not build? Be precise about your contribution.", difficulty='hard', tags=['walk-through-work', 'concreteness', 'structure'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="Describe the architecture out loud, with no whiteboard.", difficulty='hard', tags=['walk-through-work', 'technical-clarity', 'structure'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="What's in that codebase you'd rewrite today?", difficulty='medium', tags=['walk-through-work', 'conviction', 'concreteness'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="What did you cut to ship it?", difficulty='medium', tags=['walk-through-work', 'conviction', 'concreteness'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="What broke in production, or would have if it had gotten there?", difficulty='hard', tags=['walk-through-work', 'concreteness', 'structure'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="What's the largest amount of data or traffic you've personally dealt with?", difficulty='medium', tags=['walk-through-work', 'concreteness', 'technical-clarity'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="Tell me about a side project that went nowhere. What killed it?", difficulty='medium', tags=['walk-through-work', 'storytelling', 'concreteness'], meta={'suggested_framework': 'STAR'}),

        # --- Failure and being wrong (9) ---
        Topic(mode_id=interview_prep_mode.id, text="Tell me about a bug that took you an embarrassingly long time to find.", difficulty='medium', tags=['failure', 'storytelling', 'concreteness'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Describe a time you shipped something that broke.", difficulty='medium', tags=['failure', 'storytelling', 'concreteness'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Tell me about a time you were confident in a diagnosis and were completely wrong.", difficulty='hard', tags=['failure', 'storytelling', 'conviction'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Describe a production incident you were part of. What was your actual role?", difficulty='hard', tags=['failure', 'structure', 'concreteness'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Tell me about technical debt you created on purpose.", difficulty='medium', tags=['failure', 'conviction', 'concreteness'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="Describe a time you missed a deadline.", difficulty='medium', tags=['failure', 'storytelling', 'concreteness'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Tell me about feedback that stung and turned out to be right.", difficulty='medium', tags=['failure', 'storytelling', 'conviction'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text='When did you last say "I don\'t know" at work? What happened next?', difficulty='medium', tags=['failure', 'storytelling', 'conviction'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="Describe debugging someone else's code with no documentation and no author available.", difficulty='hard', tags=['failure', 'structure', 'concreteness'], meta={'suggested_framework': 'STAR'}),

        # --- Conflict and people (10) ---
        Topic(mode_id=interview_prep_mode.id, text="Tell me about a disagreement with a teammate over a technical decision.", difficulty='medium', tags=['conflict', 'nuance', 'storytelling'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Describe a time you had to push back on a manager or a PM.", difficulty='hard', tags=['conflict', 'nuance', 'conviction'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="You think the approach is wrong, you get overruled, and it ships. What do you do?", difficulty='hard', tags=['conflict', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="Tell me about working with someone difficult -- without making them the villain.", difficulty='hard', tags=['conflict', 'nuance', 'storytelling'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Describe a time you gave critical feedback in a code review.", difficulty='medium', tags=['conflict', 'nuance', 'concreteness'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Tell me about a time you convinced a team to change direction.", difficulty='medium', tags=['conflict', 'conviction', 'storytelling'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="When have you explained a technical constraint to someone who didn't want to hear it?", difficulty='hard', tags=['conflict', 'technical-clarity', 'nuance'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="Tell me about a time you were the least experienced person in the room.", difficulty='medium', tags=['conflict', 'storytelling', 'nuance'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Describe mentoring or unblocking someone junior.", difficulty='medium', tags=['conflict', 'storytelling', 'concreteness'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="When did you last change your mind because of something a colleague said?", difficulty='medium', tags=['conflict', 'nuance', 'storytelling'], meta={}),

        # --- Ownership and judgment (9) ---
        Topic(mode_id=interview_prep_mode.id, text="Tell me about something you fixed that nobody asked you to fix.", difficulty='medium', tags=['ownership', 'conviction', 'storytelling'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Describe a time you had incomplete requirements and shipped anyway.", difficulty='hard', tags=['ownership', 'conviction', 'concreteness'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Tell me about choosing between doing it fast and doing it right.", difficulty='medium', tags=['ownership', 'conviction', 'nuance'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Describe a time you escalated something. What was the threshold?", difficulty='hard', tags=['ownership', 'structure', 'conviction'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="Tell me about a time you had to say no to a request.", difficulty='medium', tags=['ownership', 'conviction', 'nuance'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="When did you decide something wasn't worth doing?", difficulty='medium', tags=['ownership', 'conviction', 'nuance'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="How do you decide what to work on when everything is priority one?", difficulty='hard', tags=['ownership', 'structure', 'conviction'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="Tell me about a decision you made with the wrong information.", difficulty='medium', tags=['ownership', 'storytelling', 'concreteness'], meta={'suggested_framework': 'STAR'}),
        Topic(mode_id=interview_prep_mode.id, text="Describe a time you took on work outside your defined role.", difficulty='medium', tags=['ownership', 'storytelling', 'conviction'], meta={'suggested_framework': 'STAR'}),

        # --- Learning (4) ---
        Topic(mode_id=interview_prep_mode.id, text="What's the most recent technical thing you learned, and why that thing?", difficulty='easy', tags=['learning', 'concreteness', 'structure'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="How do you get up to speed in an unfamiliar codebase? Use a real example.", difficulty='medium', tags=['learning', 'structure', 'concreteness'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="What's something you believed about engineering two years ago that you no longer believe?", difficulty='medium', tags=['learning', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="What's a technology everyone likes that you don't? Defend the position.", difficulty='medium', tags=['learning', 'conviction', 'nuance'], meta={}),

        # --- The framing questions (5) ---
        Topic(mode_id=interview_prep_mode.id, text="Tell me about yourself. Two minutes, not chronological.", difficulty='easy', tags=['framing', 'structure', 'pacing'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="Why are you leaving your current role? Honest without bitter.", difficulty='hard', tags=['framing', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="Why this company? Give a reason that couldn't apply to five other companies.", difficulty='medium', tags=['framing', 'conviction', 'concreteness'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="What's your biggest weakness -- answered like an adult.", difficulty='hard', tags=['framing', 'nuance', 'conviction'], meta={}),
        Topic(mode_id=interview_prep_mode.id, text="Where do you want to be technically in three years?", difficulty='easy', tags=['framing', 'structure', 'conviction'], meta={}),
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
        Topic(
            mode_id=learn_vocab_mode.id,
            text="arrogant",
            difficulty='medium',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'having an exaggerated sense of one\'s own importance',
                'example_sentence': 'His arrogant tone made it hard for the team to offer feedback.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="stubborn",
            difficulty='easy',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'refusing to change one\'s mind despite good reasons',
                'example_sentence': 'She was too stubborn to admit the plan had failed.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="charismatic",
            difficulty='medium',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'having a compelling charm that inspires devotion in others',
                'example_sentence': 'The charismatic new manager won the team over in a single meeting.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="reserved",
            difficulty='easy',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'slow to reveal emotion or opinions',
                'example_sentence': 'He stayed reserved during the debate, waiting until everyone else had spoken.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="ruthless",
            difficulty='medium',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'having no pity; willing to harm others to get what one wants',
                'example_sentence': 'The company took a ruthless approach to cutting costs.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="conscientious",
            difficulty='medium',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'careful and thorough in doing one\'s work',
                'example_sentence': 'Her conscientious note-taking made the audit much easier.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="cynical",
            difficulty='medium',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'believing that people are motivated purely by self-interest',
                'example_sentence': 'He\'d grown cynical after years of broken promises from leadership.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="complacent",
            difficulty='medium',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'smugly satisfied, unaware of danger or shortcomings',
                'example_sentence': 'The team became complacent after their early success and stopped testing.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="aloof",
            difficulty='medium',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'distant and uninvolved; emotionally cool',
                'example_sentence': 'She seemed aloof in meetings, though she cared deeply about the outcome.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="tenacious",
            difficulty='medium',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'holding firmly to a purpose; persistent',
                'example_sentence': 'His tenacious follow-up eventually got the vendor to respond.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="obsequious",
            difficulty='hard',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'excessively eager to please; fawning',
                'example_sentence': 'The obsequious intern agreed with everything the director said.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="truculent",
            difficulty='hard',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'aggressively defiant; eager to fight',
                'example_sentence': 'The truculent customer refused every solution the agent offered.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="punctilious",
            difficulty='hard',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'showing great attention to correct behaviour and detail',
                'example_sentence': 'He was punctilious about crediting every source in the report.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="mercurial",
            difficulty='hard',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'subject to sudden, unpredictable mood changes',
                'example_sentence': 'Her mercurial moods made it hard to know which version of her would show up.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="phlegmatic",
            difficulty='hard',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'calm and unemotional, even under pressure',
                'example_sentence': 'He stayed phlegmatic while the rest of the room panicked about the outage.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="sanctimonious",
            difficulty='hard',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'making a show of being morally superior',
                'example_sentence': 'His sanctimonious lecture about punctuality came from the one person who was late.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="diffident",
            difficulty='hard',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'modest or shy from a lack of self-confidence',
                'example_sentence': 'She gave a diffident answer, unsure if her idea was any good.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="officious",
            difficulty='hard',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'asserting authority in an intrusive, unwanted way',
                'example_sentence': 'The officious hall monitor stopped students for the smallest infractions.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="taciturn",
            difficulty='hard',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'reserved; habitually saying little',
                'example_sentence': 'The taciturn engineer let his code speak for him.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="magnanimous",
            difficulty='medium',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'generous or forgiving, especially toward a rival',
                'example_sentence': 'She was magnanimous in victory, praising her opponent\'s campaign.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="indefatigable",
            difficulty='hard',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'tireless; never giving up',
                'example_sentence': 'His indefatigable effort kept the project alive long after others had quit.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="recalcitrant",
            difficulty='hard',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'stubbornly resistant to authority or control',
                'example_sentence': 'The recalcitrant committee ignored every recommendation from the review board.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="venal",
            difficulty='hard',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'open to bribery; corruptible',
                'example_sentence': 'The venal official approved the permit only after receiving a bribe.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="insouciant",
            difficulty='medium',
            tags=['vocabulary', 'character'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'casually unconcerned; carefree',
                'example_sentence': 'He gave an insouciant shrug when told the deadline had passed.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="compelling",
            difficulty='easy',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'convincing; commanding attention',
                'example_sentence': 'She made a compelling case for switching vendors.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="coherent",
            difficulty='easy',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'logical and consistent; hanging together',
                'example_sentence': 'His argument wasn\'t coherent -- each point contradicted the last.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="concede",
            difficulty='medium',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to admit that a point is true, often reluctantly',
                'example_sentence': 'She conceded that the other team\'s data was more reliable.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="refute",
            difficulty='medium',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to prove a statement or theory wrong',
                'example_sentence': 'The study refuted the earlier claim about the drug\'s side effects.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="undermine",
            difficulty='medium',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to weaken gradually, often indirectly',
                'example_sentence': 'Constant scope changes undermined the team\'s confidence in the plan.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="substantiate",
            difficulty='medium',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to provide evidence to support a claim',
                'example_sentence': 'He couldn\'t substantiate the accusation when asked for details.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="contentious",
            difficulty='medium',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'likely to cause disagreement',
                'example_sentence': 'Pricing was the most contentious topic in the negotiation.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="nuanced",
            difficulty='medium',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'containing subtle distinctions',
                'example_sentence': 'Her nuanced take avoided the black-and-white framing of the debate.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="rhetoric",
            difficulty='medium',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'persuasive language, sometimes lacking real substance',
                'example_sentence': 'The speech was full of rhetoric but short on specifics.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="premise",
            difficulty='medium',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'a statement assumed to be true as the basis of an argument',
                'example_sentence': 'The whole argument rests on a premise that hasn\'t been proven.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="specious",
            difficulty='hard',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'superficially plausible but actually wrong',
                'example_sentence': 'The specious reasoning convinced no one who checked the numbers.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="tendentious",
            difficulty='hard',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'expressing a strong, often controversial bias',
                'example_sentence': 'The article\'s tendentious framing left out any opposing view.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="disingenuous",
            difficulty='hard',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'insincere; pretending not to know something',
                'example_sentence': 'It felt disingenuous for him to ask what went wrong when he\'d caused it.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="equivocate",
            difficulty='hard',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to use ambiguous language in order to avoid committing to a position',
                'example_sentence': 'The spokesperson equivocated instead of answering the question directly.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="polemic",
            difficulty='hard',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'a strong verbal or written attack on an opinion or belief',
                'example_sentence': 'His essay read less like analysis and more like a polemic.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="sophistry",
            difficulty='hard',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'clever but fallacious reasoning',
                'example_sentence': 'The lawyer\'s closing argument was sophistry dressed up as logic.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="tautology",
            difficulty='hard',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'saying the same thing twice in different words',
                'example_sentence': '"Free gift" is a tautology -- gifts are free by definition.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="corroborate",
            difficulty='medium',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to confirm or give support to a statement with independent evidence',
                'example_sentence': 'Two other witnesses corroborated her account of the meeting.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="vindicate",
            difficulty='medium',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to clear of blame; to prove someone right after doubt',
                'example_sentence': 'The test results vindicated his original hypothesis.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="caveat",
            difficulty='medium',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'a warning or qualification attached to a statement',
                'example_sentence': 'She agreed to the plan, with the caveat that budget could change.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="ostensible",
            difficulty='hard',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'apparent, but perhaps not genuine',
                'example_sentence': 'The ostensible reason for the meeting was scheduling, but layoffs were the real topic.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="tacit",
            difficulty='medium',
            tags=['vocabulary', 'persuasion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'understood or implied without being directly stated',
                'example_sentence': 'There was a tacit agreement not to bring up the failed launch.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="inevitable",
            difficulty='easy',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'certain to happen; unavoidable',
                'example_sentence': 'Given the trends, the price increase felt inevitable.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="precarious",
            difficulty='medium',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'unstable; likely to collapse or fail',
                'example_sentence': 'The startup\'s finances were in a precarious state after the funding fell through.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="volatile",
            difficulty='medium',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'liable to change suddenly and unpredictably',
                'example_sentence': 'The market has been volatile all week.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="contingent",
            difficulty='medium',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'dependent on something else happening',
                'example_sentence': 'The offer was contingent on passing a background check.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="detrimental",
            difficulty='medium',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'causing harm or damage',
                'example_sentence': 'Skipping tests turned out to be detrimental to the release quality.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="feasible",
            difficulty='easy',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'possible to do easily or conveniently',
                'example_sentence': 'Is it feasible to finish this by Friday?'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="redundant",
            difficulty='medium',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'no longer needed; superfluous',
                'example_sentence': 'Half the steps in the old process became redundant after automation.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="imminent",
            difficulty='medium',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'about to happen',
                'example_sentence': 'Layoffs felt imminent after the third round of budget cuts.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="widespread",
            difficulty='easy',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'found or distributed over a large area',
                'example_sentence': 'The outage caused widespread confusion among customers.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="untenable",
            difficulty='hard',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'impossible to defend or maintain',
                'example_sentence': 'Her position became untenable once the numbers were made public.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="tenuous",
            difficulty='hard',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'very weak or slight; barely holding together',
                'example_sentence': 'The connection between the two events is tenuous at best.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="auspicious",
            difficulty='hard',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'showing signs of future success',
                'example_sentence': 'The team\'s first sprint was an auspicious start to the project.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="fortuitous",
            difficulty='hard',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'happening by lucky chance',
                'example_sentence': 'It was fortuitous that she checked her email right before the deadline.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="egregious",
            difficulty='hard',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'outstandingly bad; shockingly wrong',
                'example_sentence': 'The report contained an egregious error in the revenue total.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="insidious",
            difficulty='hard',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'proceeding in a harmful way that is gradual or hidden',
                'example_sentence': 'The bug was insidious -- it corrupted data slowly, with no visible errors.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="endemic",
            difficulty='hard',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'regularly found in a particular place or group',
                'example_sentence': 'Burnout had become endemic across the whole department.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="nascent",
            difficulty='hard',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'just coming into existence; beginning to develop',
                'example_sentence': 'The nascent industry attracted investors before it had any real revenue.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="moribund",
            difficulty='hard',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'at the point of death; no longer active or progressing',
                'example_sentence': 'The moribund project was quietly shelved after months of inaction.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="intractable",
            difficulty='hard',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'hard to control or solve',
                'example_sentence': 'The scheduling conflict turned out to be an intractable problem.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="inexorable",
            difficulty='hard',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'impossible to stop or prevent',
                'example_sentence': 'The inexorable rise in costs forced the company to raise prices.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="ubiquitous",
            difficulty='medium',
            tags=['vocabulary', 'situations'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'present, appearing, or found everywhere',
                'example_sentence': 'Smartphones have become ubiquitous in the last decade.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="perceive",
            difficulty='easy',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to become aware of something; to interpret it in a particular way',
                'example_sentence': 'She perceived the silence as agreement, though it wasn\'t.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="presume",
            difficulty='medium',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to suppose that something is true without proof',
                'example_sentence': 'I presumed the meeting was cancelled since no one showed up.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="discern",
            difficulty='medium',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to recognise or distinguish something, often with difficulty',
                'example_sentence': 'It was hard to discern which changes actually improved performance.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="rationale",
            difficulty='medium',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'the set of reasons or logical basis for a decision',
                'example_sentence': 'The rationale for the redesign wasn\'t clear to most of the team.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="bias",
            difficulty='easy',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'an inclination or prejudice for or against something, usually unfair',
                'example_sentence': 'The survey questions had an obvious bias built into them.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="assumption",
            difficulty='easy',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'something accepted as true or certain without proof',
                'example_sentence': 'We built the whole plan on an assumption that turned out to be false.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="insight",
            difficulty='easy',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'deep, accurate understanding of a person or thing',
                'example_sentence': 'Her insight into the user\'s real problem changed the whole design.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="intuitive",
            difficulty='medium',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'understood instinctively, without the need for conscious reasoning',
                'example_sentence': 'The new interface felt intuitive from the first click.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="speculate",
            difficulty='medium',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to form a theory or guess without firm evidence',
                'example_sentence': 'Analysts speculated about the reason for the sudden price drop.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="cognisant",
            difficulty='hard',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'aware of; having knowledge of something',
                'example_sentence': 'He was fully cognisant of the risks before signing the contract.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="empirical",
            difficulty='hard',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'based on observation or experience rather than theory',
                'example_sentence': 'The team wanted empirical evidence before changing the pricing model.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="erudite",
            difficulty='hard',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'having or showing great knowledge or learning',
                'example_sentence': 'Her erudite footnotes referenced sources most readers had never heard of.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="esoteric",
            difficulty='hard',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'understood by only a small, specialised group',
                'example_sentence': 'The talk got too esoteric for anyone outside the research team.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="epistemic",
            difficulty='hard',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'relating to knowledge and how we come to know things',
                'example_sentence': 'The debate was really an epistemic one -- how do we know what we know?'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="extrapolate",
            difficulty='hard',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to extend known information or experience into an area not known',
                'example_sentence': 'It\'s risky to extrapolate from three data points to a full-year forecast.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="conjecture",
            difficulty='hard',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'an opinion or conclusion formed on the basis of incomplete information',
                'example_sentence': 'Without the source code, any explanation is just conjecture.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="axiomatic",
            difficulty='hard',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'self-evident; taken as needing no proof',
                'example_sentence': 'It\'s axiomatic in this field that faster isn\'t always better.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="antithetical",
            difficulty='hard',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'directly opposed to; incompatible with',
                'example_sentence': 'His management style was antithetical to how the previous lead worked.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="salient",
            difficulty='medium',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'most noticeable or important',
                'example_sentence': 'The salient point got lost under ten minutes of background detail.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="germane",
            difficulty='medium',
            tags=['vocabulary', 'thought'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'relevant to the matter at hand',
                'example_sentence': 'Let\'s stick to points that are germane to today\'s decision.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="blunt",
            difficulty='easy',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'direct and plain-spoken, to the point of rudeness',
                'example_sentence': 'His blunt feedback stung, but it was accurate.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="articulate",
            difficulty='medium',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'able to express oneself clearly and effectively',
                'example_sentence': 'She gave an articulate summary of a very messy situation.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="concise",
            difficulty='easy',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'giving information clearly and in a few words',
                'example_sentence': 'The report was concise enough to read in five minutes.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="candid",
            difficulty='easy',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'honest and straightforward, sometimes uncomfortably so',
                'example_sentence': 'He gave a candid answer about why the project failed.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="understated",
            difficulty='medium',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'presented in a restrained, low-key way',
                'example_sentence': 'Her understated delivery made the joke land even harder.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="condescending",
            difficulty='medium',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'treating someone as if they are less intelligent or important',
                'example_sentence': 'The reply came across as condescending, even if that wasn\'t the intent.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="verbose",
            difficulty='medium',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'using or containing more words than needed',
                'example_sentence': 'The email was so verbose that most people stopped reading halfway through.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="eloquent",
            difficulty='medium',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'fluent and persuasive in speech or writing',
                'example_sentence': 'Her eloquent closing argument won over the jury.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="laconic",
            difficulty='hard',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'using very few words',
                'example_sentence': 'His laconic reply -- "noted" -- said everything and nothing.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="glib",
            difficulty='hard',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'fluent and voluble but insincere or shallow',
                'example_sentence': 'His glib apology didn\'t convince anyone he meant it.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="vociferous",
            difficulty='hard',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'expressing opinions or feelings in a loud and forceful way',
                'example_sentence': 'The vociferous crowd made it impossible to finish the announcement.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="circumlocution",
            difficulty='hard',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'the use of many words where fewer would do',
                'example_sentence': 'He buried the bad news in so much circumlocution that no one noticed.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="euphemism",
            difficulty='medium',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'a mild or indirect word substituted for one considered harsh',
                'example_sentence': '"Restructuring" was the euphemism everyone used instead of "layoffs."'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="innuendo",
            difficulty='medium',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'an indirect remark, usually suggestive or critical',
                'example_sentence': 'The comment was framed as a joke but carried an obvious innuendo.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="platitude",
            difficulty='medium',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'a dull, obvious remark presented as if it were meaningful',
                'example_sentence': '"Everything happens for a reason" felt like a platitude in that moment.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="bombastic",
            difficulty='hard',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'high-sounding but with little real meaning',
                'example_sentence': 'The bombastic press release promised far more than the product delivered.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="trenchant",
            difficulty='hard',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'sharply perceptive; incisive',
                'example_sentence': 'Her trenchant review pointed out exactly where the plan fell apart.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="perfunctory",
            difficulty='hard',
            tags=['vocabulary', 'speech'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'carried out with minimal effort or reflection, as a mere formality',
                'example_sentence': 'The manager gave a perfunctory nod and moved on to the next item.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="apprehensive",
            difficulty='easy',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'anxious or fearful about something that may happen',
                'example_sentence': 'She felt apprehensive about presenting to the board for the first time.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="indifferent",
            difficulty='easy',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'having no particular interest or concern',
                'example_sentence': 'He seemed indifferent to the outcome of the vote.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="resentful",
            difficulty='medium',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'feeling bitter about unfair treatment',
                'example_sentence': 'She stayed resentful about being passed over for the promotion.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="elated",
            difficulty='easy',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'extremely happy and excited',
                'example_sentence': 'The team was elated when the launch went smoothly.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="overwhelmed",
            difficulty='easy',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'overpowered by too much emotion or too much to do',
                'example_sentence': 'He felt overwhelmed by the number of messages waiting for him.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="reluctant",
            difficulty='easy',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'unwilling and hesitant',
                'example_sentence': 'She was reluctant to volunteer for the extra project.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="wary",
            difficulty='medium',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'cautious about possible dangers or problems',
                'example_sentence': 'Investors grew wary after the second delayed earnings report.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="poignant",
            difficulty='medium',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'evoking a keen sense of sadness or regret',
                'example_sentence': 'His farewell speech was more poignant than anyone expected.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="visceral",
            difficulty='medium',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'felt in or as if in the body, rather than reasoned or intellectual',
                'example_sentence': 'Her visceral reaction to the news surprised even her.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="ambivalent",
            difficulty='medium',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'having mixed or contradictory feelings about something',
                'example_sentence': 'He was ambivalent about the offer -- excited, but also uneasy.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="disconsolate",
            difficulty='hard',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'unable to be comforted; very unhappy',
                'example_sentence': 'She was disconsolate after losing the notebook with all her notes.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="incredulous",
            difficulty='hard',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'unwilling or unable to believe something',
                'example_sentence': 'He was incredulous when told the deadline had moved up a week.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="jaded",
            difficulty='medium',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'worn out and unenthusiastic, especially from overexposure',
                'example_sentence': 'Years of bad demos had made the investors jaded.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="vicarious",
            difficulty='hard',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'experienced through the feelings or actions of another person',
                'example_sentence': 'She got a vicarious thrill watching her mentee close the deal.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="wistful",
            difficulty='medium',
            tags=['vocabulary', 'emotion'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'having or showing a feeling of gentle longing or regret',
                'example_sentence': 'He gave a wistful look back at the office on his last day.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="streamline",
            difficulty='easy',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to make a process more efficient by simplifying it',
                'example_sentence': 'They streamlined the approval process from five steps to two.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="leverage",
            difficulty='medium',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to use something to maximum advantage',
                'example_sentence': 'The startup leveraged its early customers to attract investors.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="mitigate",
            difficulty='medium',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to make something less severe or serious',
                'example_sentence': 'The team added checks to mitigate the risk of duplicate charges.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="delegate",
            difficulty='easy',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to assign responsibility or authority to someone else',
                'example_sentence': 'She learned to delegate instead of doing everything herself.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="incentive",
            difficulty='easy',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'something that motivates or encourages someone to act',
                'example_sentence': 'The bonus was a strong incentive to hit the deadline.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="viable",
            difficulty='easy',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'capable of working successfully',
                'example_sentence': 'Is this business model actually viable at scale?'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="consolidate",
            difficulty='medium',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to combine multiple things into a single, more effective whole',
                'example_sentence': 'They consolidated three tools into one shared dashboard.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="scrutiny",
            difficulty='medium',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'close, critical examination',
                'example_sentence': 'The budget came under heavy scrutiny after the overrun.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="autonomy",
            difficulty='medium',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'the right or ability to self-govern; independence',
                'example_sentence': 'Engineers were given more autonomy over their own roadmaps.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="bureaucratic",
            difficulty='medium',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'excessively concerned with rigid procedure at the expense of efficiency',
                'example_sentence': 'Getting sign-off took weeks because of the bureaucratic approval chain.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="attrition",
            difficulty='hard',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'a gradual reduction in strength or numbers',
                'example_sentence': 'The company lost half its senior staff to attrition over two years.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="nepotism",
            difficulty='medium',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'favouring relatives or friends, especially in hiring or promotion',
                'example_sentence': 'Employees complained about nepotism after the CEO\'s nephew was promoted.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="precedent",
            difficulty='medium',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'an earlier case or decision used as a guide for later ones',
                'example_sentence': 'Approving this exception would set a precedent for every future request.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="prerogative",
            difficulty='hard',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'an exclusive right belonging to a particular person or role',
                'example_sentence': 'Final sign-off was the director\'s prerogative alone.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="remuneration",
            difficulty='hard',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'noun',
                'definition': 'payment made for work or services rendered',
                'example_sentence': 'The contract outlined remuneration for the full six-month term.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="stringent",
            difficulty='medium',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'strict and demanding, especially with rules or requirements',
                'example_sentence': 'The new security policy is far more stringent than the old one.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="onerous",
            difficulty='hard',
            tags=['vocabulary', 'work'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'involving a heavy or burdensome amount of effort or duty',
                'example_sentence': 'The compliance paperwork became an onerous part of every launch.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="substantial",
            difficulty='easy',
            tags=['vocabulary', 'change'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'considerable in size, importance, or degree',
                'example_sentence': 'They made a substantial investment in the new platform.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="marginal",
            difficulty='medium',
            tags=['vocabulary', 'change'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'small and of limited significance',
                'example_sentence': 'The update made only a marginal difference to load times.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="gradual",
            difficulty='easy',
            tags=['vocabulary', 'change'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'happening slowly over a period of time',
                'example_sentence': 'Adoption of the new tool was gradual but steady.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="drastic",
            difficulty='easy',
            tags=['vocabulary', 'change'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'extreme and sudden or having a far-reaching effect',
                'example_sentence': 'They took drastic measures to stop the outage from spreading.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="fluctuate",
            difficulty='medium',
            tags=['vocabulary', 'change'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to rise and fall irregularly in number or amount',
                'example_sentence': 'Traffic tends to fluctuate a lot during the holidays.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="escalate",
            difficulty='medium',
            tags=['vocabulary', 'change'],
            meta={
                'part_of_speech': 'verb',
                'definition': 'to increase rapidly in intensity or seriousness',
                'example_sentence': 'The disagreement escalated into a full-blown dispute.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="negligible",
            difficulty='medium',
            tags=['vocabulary', 'change'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'so small or unimportant as to be not worth considering',
                'example_sentence': 'The performance hit from the change was negligible.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="exponential",
            difficulty='medium',
            tags=['vocabulary', 'change'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'increasing at an accelerating, ever-faster rate',
                'example_sentence': 'User growth has been exponential since the redesign.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="incremental",
            difficulty='medium',
            tags=['vocabulary', 'change'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'increasing gradually in small, regular stages',
                'example_sentence': 'They shipped the redesign through a series of incremental updates.'
            }
        ),
        Topic(
            mode_id=learn_vocab_mode.id,
            text="precipitous",
            difficulty='hard',
            tags=['vocabulary', 'change'],
            meta={
                'part_of_speech': 'adjective',
                'definition': 'dangerously steep, or happening very suddenly',
                'example_sentence': 'Revenue took a precipitous drop after the biggest client left.'
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
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What was the best fifteen minutes of today?",
            difficulty='easy',
            tags=['reflection', 'looking-back'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What drained you most, and was it avoidable?",
            difficulty='medium',
            tags=['reflection', 'looking-back'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What did you do today that you'll still remember in a year?",
            difficulty='medium',
            tags=['reflection', 'looking-back'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="When did you feel most like yourself today?",
            difficulty='medium',
            tags=['reflection', 'looking-back'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What's one thing that went better than expected?",
            difficulty='easy',
            tags=['reflection', 'looking-back'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What did you avoid today, and why?",
            difficulty='medium',
            tags=['reflection', 'looking-back'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="Where did your attention actually go, versus where you meant it to go?",
            difficulty='hard',
            tags=['reflection', 'looking-back'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What was the first thing you thought about when you woke up?",
            difficulty='easy',
            tags=['reflection', 'looking-back'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="If today were a chapter title, what would it be?",
            difficulty='medium',
            tags=['reflection', 'looking-back'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What's one small thing that made today easier?",
            difficulty='easy',
            tags=['reflection', 'looking-back'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What did you learn today that you didn't know yesterday?",
            difficulty='easy',
            tags=['reflection', 'learning'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What did you get wrong, and how did you find out?",
            difficulty='medium',
            tags=['reflection', 'learning'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What did you assume without checking?",
            difficulty='medium',
            tags=['reflection', 'learning'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What question are you still sitting with?",
            difficulty='medium',
            tags=['reflection', 'learning'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What advice did you give today that you should take yourself?",
            difficulty='medium',
            tags=['reflection', 'learning'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What did you do the hard way when there was an easier way?",
            difficulty='medium',
            tags=['reflection', 'learning'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What mistake did you repeat?",
            difficulty='medium',
            tags=['reflection', 'learning'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What surprised you?",
            difficulty='easy',
            tags=['reflection', 'learning'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What did you almost say and decide not to?",
            difficulty='hard',
            tags=['reflection', 'learning'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What would you do differently if today restarted right now?",
            difficulty='medium',
            tags=['reflection', 'learning'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="Who did you help today, and did they know it?",
            difficulty='medium',
            tags=['reflection', 'people'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="Who helped you?",
            difficulty='easy',
            tags=['reflection', 'people'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="Who did you think about but not contact?",
            difficulty='medium',
            tags=['reflection', 'people'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What conversation do you wish had gone differently?",
            difficulty='medium',
            tags=['reflection', 'people'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="Were you generous with attention today, or stingy with it?",
            difficulty='hard',
            tags=['reflection', 'people'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="Who did you judge quickly? What might you be missing?",
            difficulty='hard',
            tags=['reflection', 'people'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What did someone say today that stuck with you?",
            difficulty='easy',
            tags=['reflection', 'people'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="Where were you a better listener than usual?",
            difficulty='medium',
            tags=['reflection', 'people'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="Who deserves a thank-you you haven't given?",
            difficulty='medium',
            tags=['reflection', 'people'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What relationship needs maintenance this week?",
            difficulty='medium',
            tags=['reflection', 'people'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="Did today move you toward something, or just past something?",
            difficulty='hard',
            tags=['reflection', 'values'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What did you say yes to that you should have declined?",
            difficulty='medium',
            tags=['reflection', 'values'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What are you doing out of habit rather than choice?",
            difficulty='hard',
            tags=['reflection', 'values'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What would the version of you from five years ago think of today?",
            difficulty='medium',
            tags=['reflection', 'values'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What matters to you that got no time today?",
            difficulty='hard',
            tags=['reflection', 'values'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="Are you working toward a life you actually want, or one you were handed?",
            difficulty='hard',
            tags=['reflection', 'values'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What are you tolerating that you shouldn't be?",
            difficulty='hard',
            tags=['reflection', 'values'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What's the smallest step you could take tomorrow toward something that matters?",
            difficulty='medium',
            tags=['reflection', 'values'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What are you pretending not to know?",
            difficulty='hard',
            tags=['reflection', 'values'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="If nothing changed for the next year, would that be okay?",
            difficulty='hard',
            tags=['reflection', 'values'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What emotion showed up most today, and what triggered it?",
            difficulty='medium',
            tags=['reflection', 'emotion'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What are you anxious about that you can't control?",
            difficulty='medium',
            tags=['reflection', 'emotion'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What are you anxious about that you can control?",
            difficulty='medium',
            tags=['reflection', 'emotion'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="When did you feel calm today, and what conditions made that possible?",
            difficulty='medium',
            tags=['reflection', 'emotion'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What are you carrying that isn't yours to carry?",
            difficulty='hard',
            tags=['reflection', 'emotion'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What are you grateful for that you usually overlook?",
            difficulty='easy',
            tags=['reflection', 'emotion'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="Were you kind to yourself today? How would you know?",
            difficulty='medium',
            tags=['reflection', 'emotion'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What does your body feel like right now?",
            difficulty='easy',
            tags=['reflection', 'emotion'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What do you need more of, and what do you need less of?",
            difficulty='medium',
            tags=['reflection', 'emotion'],
            meta={}
        ),
        Topic(
            mode_id=daily_reflection_mode.id,
            text="What's one thing you can let go of before sleeping?",
            difficulty='easy',
            tags=['reflection', 'emotion'],
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
