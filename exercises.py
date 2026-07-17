"""
Exercise data and utilities for Dil Se
"""

EXERCISES_ENGLISH = [
    {
        "id": "breathing_478",
        "name": "4-7-8 Breathing",
        "description": "A calming breathing technique that can help reduce anxiety and improve sleep.",
        "duration": 5,
        "how_it_works": "Breathe in for 4 counts, hold for 7, breathe out for 8. This activates your nervous system's calming response.",
        "steps": [
            "Sit or lie down in a comfortable position",
            "Close your eyes if it feels comfortable",
            "Breathe in quietly through your nose for a count of 4",
            "Hold your breath for a count of 7",
            "Exhale through your mouth for a count of 8",
            "Repeat 4 more times (5 cycles total)",
            "Notice how your body feels when done"
        ],
        "when_to_use": "When you feel anxious, overwhelmed, or can't sleep",
        "tips": "The exhale is the most important part - it tells your body it's safe to relax"
    },
    {
        "id": "grounding_5432",
        "name": "5-4-3-2-1 Grounding",
        "description": "A sensory technique to bring you back to the present moment when anxiety or panic feels overwhelming.",
        "duration": 5,
        "how_it_works": "Notice 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
        "steps": [
            "Notice 5 things you can SEE around you",
            "Notice 4 things you can TOUCH (texture, temperature)",
            "Notice 3 things you can HEAR",
            "Notice 2 things you can SMELL",
            "Notice 1 thing you can TASTE (or just name something you like)",
            "Take a deep breath and notice how grounded you feel"
        ],
        "when_to_use": "When you feel anxious, having a panic attack, or dissociating",
        "tips": "Go slow. Really feel and sense each thing. There's no rush."
    },
    {
        "id": "body_scan",
        "name": "Body Scan Meditation",
        "description": "Progressive relaxation technique to release physical tension and calm your mind.",
        "duration": 8,
        "how_it_works": "Slowly move attention through your body from head to toe, noticing and releasing tension.",
        "steps": [
            "Lie down or sit in a comfortable position",
            "Close your eyes and take 3 deep breaths",
            "Notice your head and face - any tension? Relax it",
            "Move to your neck and shoulders - let them drop",
            "Notice your chest and arms - let them feel heavy",
            "Notice your stomach - breath flowing naturally",
            "Notice your legs and feet - fully relaxed",
            "Take 3 more deep breaths and slowly open your eyes"
        ],
        "when_to_use": "For general relaxation, before bed, or when physically tense",
        "tips": "This isn't about forcing relaxation. Just notice what's there."
    },
    {
        "id": "gratitude_practice",
        "name": "Gratitude Practice",
        "description": "A simple way to shift your perspective and anchor yourself in what's good.",
        "duration": 3,
        "how_it_works": "Think of 3 things - one significant, one small, one something about yourself.",
        "steps": [
            "Think of one bigger thing you're grateful for (person, achievement, opportunity)",
            "Think of one small thing (a good meal, sunshine, a song)",
            "Think of one thing about yourself you're grateful for (a quality, skill, or how you handled something)",
            "Say them out loud or write them down if you can",
            "Notice how your mood shifts even slightly"
        ],
        "when_to_use": "When you're feeling low, stuck, or need perspective",
        "tips": "It's okay if this feels awkward at first. Gratitude is a practice."
    },
    {
        "id": "journaling_prompt",
        "name": "Guided Journaling",
        "description": "Free-write reflection to process emotions and gain clarity.",
        "duration": 10,
        "how_it_works": "Use a prompt to start writing without judging what comes out.",
        "steps": [
            "Get paper or open a blank document",
            "Set a timer for 10 minutes",
            "Use one of the prompts (see below)",
            "Write freely without editing - no one needs to see this",
            "When done, read back if you want to - sometimes insights appear"
        ],
        "prompts": [
            "What did I not say today that I wish I had?",
            "What am I carrying right now that I'm tired of carrying?",
            "If I could tell my parents something with no consequences, what would it be?",
            "What's one small thing that made me smile today?",
            "What am I scared of that no one knows?"
        ],
        "when_to_use": "Anytime you need to process emotions or gain clarity",
        "tips": "There are no rules. This is your private space."
    },
    {
        "id": "progressive_relax",
        "name": "Progressive Muscle Relaxation",
        "description": "Tense and release muscle groups to release physical and mental tension.",
        "duration": 6,
        "how_it_works": "Tense each muscle group for 5 seconds, then release and notice the difference.",
        "steps": [
            "Start with your hands - make tight fists for 5 seconds, then release",
            "Move to your arms - tense them for 5 seconds, then release",
            "Tense your shoulders up to your ears - hold, then drop them",
            "Tense your face and jaw - hold, then relax",
            "Tense your stomach - hold, then let it go soft",
            "Tense your legs - squeeze, then release",
            "Tense everything at once for 5 seconds, then let everything go"
        ],
        "when_to_use": "When you hold tension in your body, before sleep, or when stressed",
        "tips": "The point is noticing the difference between tension and relaxation"
    }
]

EXERCISES_HINGLISH = [
    {
        "id": "breathing_478",
        "name": "4-7-8 Breathing",
        "description": "Ek aaram dene wali breathing technique jo anxiety aur sleep problems mein madad karती है।",
        "duration": 5,
        "how_it_works": "4 count par saanss lo, 7 par rokho, 8 par nikalo। Isse tumhara nervous system calm ho jata hai।",
        "steps": [
            "Comfort se baito ya let jao",
            "Aankhen band karo agar comfortable ho",
            "Naak se 4 count ke liye saanss lo",
            "7 count ke liye rokho",
            "Munh se 8 count ke liye nikalo",
            "5 baar repeat karo",
            "Mahsoos karo ke tum kaisa feel kar rahe ho"
        ],
        "when_to_use": "Jab anxiety mahsoos ho, ya neend nahi aa rahi",
        "tips": "Exhale sabse important hai - isse body ko signal milta hai safe ho"
    },
    {
        "id": "grounding_5432",
        "name": "5-4-3-2-1 Grounding",
        "description": "Anxiety mein present moment par wapas aane ka technique।",
        "duration": 5,
        "how_it_works": "5 cheezein dekho, 4 ko touch karo, 3 suno, 2 mehko, 1 swaad।",
        "steps": [
            "5 cheezein dekho jo around tum dekh sakte ho",
            "4 cheezein touch karo - unka texture feel karo",
            "3 cheezein suno",
            "2 cheezein mehko",
            "1 cheez swaad lo ya soch lo",
            "Deep breath lo"
        ],
        "when_to_use": "Jab panic attack ya anxiety feel ho",
        "tips": "Slow chalo। Har cheez ko truly feel karo।"
    }
]


def get_exercises(language='english'):
    """Get exercises in the specified language"""
    if language.lower() == 'hinglish':
        return EXERCISES_HINGLISH
    return EXERCISES_ENGLISH


def get_exercise_by_id(exercise_id, language='english'):
    """Get a specific exercise by ID"""
    exercises = get_exercises(language)
    for exercise in exercises:
        if exercise['id'] == exercise_id:
            return exercise
    return None


def get_all_exercise_names(language='english'):
    """Get list of all exercise names"""
    exercises = get_exercises(language)
    return [{'id': ex['id'], 'name': ex['name']} for ex in exercises]


def get_mood_emoji(mood_level):
    """Get emoji for mood level (1-5)"""
    emojis = {
        1: "😢",  # Very sad
        2: "😞",  # Sad
        3: "😐",  # Neutral
        4: "🙂",  # Happy
        5: "😊"   # Very happy
    }
    return emojis.get(mood_level, "🙂")


def get_mood_label(mood_level, language='english'):
    """Get label for mood level"""
    if language.lower() == 'hinglish':
        labels = {
            1: "Bilkul Bura",
            2: "Bura",
            3: "Theek Hai",
            4: "Accha",
            5: "Bahut Accha"
        }
    else:
        labels = {
            1: "Terrible",
            2: "Bad",
            3: "Okay",
            4: "Good",
            5: "Great"
        }
    return labels.get(mood_level, "Okay")
