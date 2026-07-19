"""
Dil Se - AI Mental Wellness Companion
Main Flask application
"""

from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect
from flask_cors import CORS
from config import config
from models import db, User, MoodEntry, JournalEntry, ChatHistory, ExerciseCompletion
from chatbot import DilSeChatbot
from exercises import get_exercises, get_exercise_by_id, get_all_exercise_names, get_mood_emoji
from predictor import predict_mood
import traceback


import sys
print("Python executable:", sys.executable)

try:
    from groq import Groq
    print("Groq imported successfully")
except Exception as e:
    print("Groq import failed:", e)
    Groq = None
    
# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

# Initialize chatbot
chatbot = None


def get_or_create_session_user(user_id=None):
    """Resolve the active user from the URL, session, or create an anonymous one."""
    if user_id is not None:
        user = db.session.get(User, user_id)
        if user:
            session['user_id'] = user.id
            return user

    session_user_id = session.get('user_id')
    if session_user_id:
        user = db.session.get(User, session_user_id)
        if user:
            return user

    user = User(language_preference='english')
    db.session.add(user)
    db.session.commit()
    session['user_id'] = user.id
    return user


@app.before_request
def before_request():
    """Initialize chatbot before request"""
    global chatbot
    if chatbot is None:
        try:
            chatbot = DilSeChatbot()
        except ValueError as e:
            print(f"Warning: {e}")


@app.shell_context_processor
def make_shell_context():
    """Make database models available in shell"""
    return {
        'db': db,
        'User': User,
        'MoodEntry': MoodEntry,
        'JournalEntry': JournalEntry,
        'ChatHistory': ChatHistory,
        'ExerciseCompletion': ExerciseCompletion
    }


# ==================== UI Routes ====================

@app.route('/')
def index():
    if not session.get('user_id'):
        return render_template('auth.html')
    return render_template('home.html')

@app.route('/auth')
def auth_page():
    return render_template('auth.html')

@app.route('/chat')
def chat_page():
    """Chat interface"""
    return render_template('chat.html')


@app.route('/exercises')
def exercises_page():
    """Exercises page"""
    return render_template('exercises.html')


@app.route('/journal')
def journal_page():
    """Journal page"""
    return render_template('journal.html')


# ==================== API Routes ====================

# ---- User Management ----

@app.route('/api/user', methods=['POST'])
def create_user():
    """Create or get user"""
    data = request.get_json()
    username = data.get('username')
    language = data.get('language', 'english')
    
    # For anonymous users, create without username
    if not username:
        user = User(language_preference=language)
    else:
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, language_preference=language)
    
    db.session.add(user)
    db.session.commit()
    
    # Store user ID in session
    session['user_id'] = user.id
    
    return jsonify({
        'success': True,
        'user_id': user.id,
        'username': user.username,
        'language': user.language_preference
    }), 201


@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@app.route('/api/user/<int:user_id>/language', methods=['PUT'])
def update_language(user_id):
    """Update user language preference"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    language = data.get('language', 'english')
    user.language_preference = language
    db.session.commit()
    
    return jsonify({
        'success': True,
        'language': user.language_preference
    }), 200


# ---- Mood Tracking ----

@app.route('/api/user/<int:user_id>/mood', methods=['POST'])
def create_mood_entry(user_id):
    """Create a mood entry for today"""
    user = get_or_create_session_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    mood = data.get('mood')
    note = data.get('note', '')
    
    if not mood or mood < 1 or mood > 5:
        return jsonify({'error': 'Mood must be between 1 and 5'}), 400
    
    today = datetime.now().date()
    active_user_id = user.id
    
    # Check if mood already exists for today
    existing = MoodEntry.query.filter_by(user_id=active_user_id, date=today).first()
    if existing:
        existing.mood = mood
        existing.note = note
        existing.timestamp = datetime.utcnow()
    else:
        entry = MoodEntry(user_id=active_user_id, mood=mood, date=today, note=note)
        db.session.add(entry)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'mood': mood,
        'date': today.isoformat(),
        'note': note
    }), 201


@app.route('/api/user/<int:user_id>/mood', methods=['GET'])
def get_mood_history(user_id):
    """Get mood history for user"""
    user = get_or_create_session_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    days = request.args.get('days', 7, type=int)
    since_date = datetime.now().date() - timedelta(days=days)
    
    moods = MoodEntry.query.filter(
        MoodEntry.user_id == user.id,
        MoodEntry.date >= since_date
    ).order_by(MoodEntry.date).all()
    
    return jsonify({
        'moods': [m.to_dict() for m in moods],
        'count': len(moods)
    }), 200


@app.route('/api/user/<int:user_id>/streak', methods=['GET'])
def get_streak(user_id):
    """Get user's current streak of mood check-ins"""
    user = get_or_create_session_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    today = datetime.now().date()
    streak = 0
    current_date = today
    
    while True:
        mood = MoodEntry.query.filter_by(user_id=user.id, date=current_date).first()
        if not mood:
            break
        streak += 1
        current_date -= timedelta(days=1)
    
    return jsonify({'streak': streak}), 200


# ---- Chat ----

@app.route('/api/chat', methods=['POST'])
def handle_chat(user_id=None):
    """Handle chat message"""
    # Get user_id from request data or session
    data = request.get_json()
    user_id = data.get('user_id') or session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400
    
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    # Get language preference
    language = user.language_preference
    
    try:
        # Get recent chat history for context
        recent_chats = ChatHistory.query.filter_by(user_id=user_id).order_by(
            ChatHistory.timestamp.desc()
        ).limit(10).all()
        
        # Build conversation history (oldest first)
        conversation = []
        for chat in reversed(recent_chats):
            conversation.append({
                "role": "user",
                "content": chat.user_message
            })
            conversation.append({
                "role": "assistant",
                "content": chat.bot_response
            })
        
        # Get response from chatbot
        response = chatbot.get_response(message, language=language, conversation_history=conversation)
        
        # Store in database
        chat_entry = ChatHistory(
            user_id=user_id,
            user_message=message,
            bot_response=response,
            language=language
        )
        db.session.add(chat_entry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'response': response,
            'language': language
        }), 200
    
    except Exception as e:
        traceback.print_exc()

        return jsonify({
            "error": str(e)}), 500


@app.route('/api/chat/quick-replies', methods=['GET'])
def get_quick_replies():
    """Get quick reply suggestions"""
    user_id = request.args.get('user_id') or session.get('user_id')
    language = request.args.get('language', 'english')
    
    if user_id:
        user = db.session.get(User, user_id)
        if user:
            language = user.language_preference
    
    replies = chatbot.get_quick_replies(language)
    
    return jsonify({
        'quick_replies': replies,
        'language': language
    }), 200


# ---- Exercises ----

@app.route('/api/exercises', methods=['GET'])
def list_exercises():
    user_id = request.args.get('user_id') or session.get('user_id')
    language = request.args.get('language', 'english')
    
    # Fix: handle "null" string from frontend
    if user_id and user_id != 'null':
        user = db.session.get(User, int(user_id))
        if user:
            language = user.language_preference
    
    exercises = get_exercises(language)
    
    return jsonify({
        'exercises': exercises,
        'count': len(exercises)
    }), 200

@app.route('/api/exercises/<exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    """Get specific exercise details"""
    language = request.args.get('language', 'english')
    exercise = get_exercise_by_id(exercise_id, language)
    
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    
    return jsonify(exercise), 200


@app.route('/api/user/<int:user_id>/exercise-completion', methods=['POST'])
def log_exercise_completion(user_id):
    """Log that user completed an exercise"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    exercise_name = data.get('exercise_name')
    duration = data.get('duration_seconds', 0)
    
    if not exercise_name:
        return jsonify({'error': 'Exercise name required'}), 400
    
    completion = ExerciseCompletion(
        user_id=user_id,
        exercise_name=exercise_name,
        duration_seconds=duration
    )
    db.session.add(completion)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'exercise': exercise_name,
        'duration': duration
    }), 201


@app.route('/api/user/<int:user_id>/exercise-history', methods=['GET'])
def get_exercise_history(user_id):
    """Get user's exercise completion history"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
@app.route('/api/user/<int:user_id>/journal', methods=['POST'])
def create_journal_entry(user_id):
    """Create a journal entry"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    content = data.get('content', '').strip()
    mood = data.get('mood')
    prompt = data.get('prompt_used')
    
    if not content:
        return jsonify({'error': 'Content required'}), 400
    
    entry = JournalEntry(
        user_id=user_id,
        content=content,
        date=datetime.now().date(),
        mood_at_time=mood,
        prompt_used=prompt
    )
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'entry': entry.to_dict()
    }), 201


@app.route('/api/user/<int:user_id>/journal', methods=['GET'])
def get_journal_entries(user_id):
    """Get journal entries for user"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    days = request.args.get('days', 90, type=int)
    since_date = datetime.now().date() - timedelta(days=days)
    
    entries = JournalEntry.query.filter(
        JournalEntry.user_id == user_id,
        JournalEntry.date >= since_date
    ).order_by(JournalEntry.date.desc()).all()
    
    return jsonify({
        'entries': [e.to_dict() for e in entries],
        'count': len(entries)
    }), 200


@app.route('/api/journal/<int:entry_id>', methods=['GET'])
def get_journal_entry(entry_id):
    """Get specific journal entry"""
    entry = JournalEntry.query.get(entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    return jsonify(entry.to_dict()), 200


@app.route('/api/journal/<int:entry_id>', methods=['PUT'])
def update_journal_entry(entry_id):
    """Update a journal entry"""
    entry = JournalEntry.query.get(entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    data = request.get_json()
    entry.content = data.get('content', entry.content)
    entry.mood_at_time = data.get('mood', entry.mood_at_time)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'entry': entry.to_dict()
    }), 200


@app.route('/api/journal/<int:entry_id>', methods=['DELETE'])
def delete_journal_entry(entry_id):
    """Delete a journal entry"""
    entry = JournalEntry.query.get(entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    db.session.delete(entry)
    db.session.commit()
    
    return jsonify({'success': True}), 200


# ---- Journal Prompts ----

@app.route('/api/journal/prompts', methods=['GET'])
def get_journal_prompts():
    """Get journal prompts"""
    language = request.args.get('language', 'english')
    
    if language == 'hinglish':
        prompts = [
            "Aaj aap ne kya nahi kaha jo keh sakte the?",
            "Kya dar ho raha hai aapko jo kisi ko nahi pata?",
            "Apne parents ko kya bolna pasand hoga consequences ke bina?",
            "Aaj ka sabse chhota khushi ka moment kya tha?",
            "Ab aap kya carry kar rahe ho jo thak gaye ho carry karne se?"
        ]
    else:
        prompts = [
            "What did you not say today but wish you had?",
            "What's one thing you're scared of that no one knows?",
            "What would you tell your parents if there were no consequences?",
            "What was the smallest thing that made you smile today?",
            "What are you carrying right now that you're tired of carrying?"
        ]
    
    return jsonify({
        'prompts': prompts,
        'language': language
    }), 200

# ==================== Prediction ====================

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'error': 'User not found. Please create an account first.'}), 200
    session['user_id'] = user.id
    return jsonify({
        'success': True,
        'user_id': user.id,
        'username': user.username,
        'language': user.language_preference
    })


@app.route('/api/user/<int:user_id>/mood-prediction', methods=['GET'])
def get_mood_prediction(user_id):
    user = get_or_create_session_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    prediction = predict_mood(user.id)
    return jsonify(prediction), 200


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500



# ==================== Initialization ====================

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Initialized the database.')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)

