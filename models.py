from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """User model for storing user preferences"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    language_preference = db.Column(db.String(20), default='english')  # 'english' or 'hinglish'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    mood_entries = db.relationship('MoodEntry', backref='user', lazy=True, cascade='all, delete-orphan')
    journal_entries = db.relationship('JournalEntry', backref='user', lazy=True, cascade='all, delete-orphan')
    chat_history = db.relationship('ChatHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    exercise_completions = db.relationship('ExerciseCompletion', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username or self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'language_preference': self.language_preference,
            'created_at': self.created_at.isoformat()
        }


class MoodEntry(db.Model):
    """Mood tracking entries"""
    __tablename__ = 'mood_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood = db.Column(db.Integer, nullable=False)  # 1-5 scale
    date = db.Column(db.Date, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.String(500))  # Optional note with mood
    
    __table_args__ = (db.UniqueConstraint('user_id', 'date', name='unique_mood_per_day'),)
    
    def __repr__(self):
        return f'<MoodEntry user={self.user_id} mood={self.mood} date={self.date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'mood': self.mood,
            'date': self.date.isoformat(),
            'timestamp': self.timestamp.isoformat(),
            'note': self.note
        }


class JournalEntry(db.Model):
    """Journal entries for reflection"""
    __tablename__ = 'journal_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    mood_at_time = db.Column(db.Integer)  # Optional mood when journaling (1-5)
    prompt_used = db.Column(db.String(300))  # Which prompt was used, if any
    
    def __repr__(self):
        return f'<JournalEntry user={self.user_id} date={self.date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'date': self.date.isoformat(),
            'timestamp': self.timestamp.isoformat(),
            'mood_at_time': self.mood_at_time,
            'prompt_used': self.prompt_used
        }


class ChatHistory(db.Model):
    """Chat conversation history"""
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    language = db.Column(db.String(20), default='english')  # Language used for this chat
    
    def __repr__(self):
        return f'<ChatHistory user={self.user_id} timestamp={self.timestamp}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'timestamp': self.timestamp.isoformat(),
            'language': self.language
        }


class ExerciseCompletion(db.Model):
    """Track completed exercises"""
    __tablename__ = 'exercise_completions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exercise_name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    duration_seconds = db.Column(db.Integer)  # How long they spent on exercise
    
    def __repr__(self):
        return f'<ExerciseCompletion user={self.user_id} exercise={self.exercise_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'exercise_name': self.exercise_name,
            'timestamp': self.timestamp.isoformat(),
            'duration_seconds': self.duration_seconds
        }
