# Dil Se - AI-Powered Mental Wellness Companion

A culturally-tailored mental wellness app for Pakistani teens and young adults, built with Flask, Python, and a compassionate AI chatbot.

![Status](https://img.shields.io/badge/status-in%20development-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Flask](https://img.shields.io/badge/flask-3.0+-blue)

---

## 🎯 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- An Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))

### Installation

1. **Clone or download the project**
```bash
cd /Users/rabeeahussain/Documents/AI
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=sk-ant-...
```

5. **Initialize the database**
```bash
flask db init
# Or manually in Python shell:
# python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

6. **Run the development server**
```bash
python app.py
```

The app will be available at: **http://localhost:5000**

## 🔁 Recent Changes

- **Auth-first startup**: The app now opens the authentication screen by default when no session user exists. An anonymous session user is created automatically if you continue without signing up.
- **Dashboard layout**: Home dashboard now uses a wider left column for mood check-in and streak/history, with a narrower right column for the mood forecast — this gives the prediction card more breathing room.
- **Mood prediction UX**: Mood prediction requests are more resilient to stale local state and will be skipped until a valid session user is available.
- **Tests added**: Basic unit tests were added for the mood predictor and route fallback behavior, helping prevent regressions.


---

## 📱 Features Overview

### 🏠 Home Screen
- **Daily Mood Check-in** - Quick 5-point mood selector (😢😞😐🙂😊)
- **7-Day Mood History** - Visual mood tracking
- **Streak Counter** - Track consecutive days of engagement
- **Quick Access Cards** - Navigation to Chat, Exercises, and Journal

### 💬 Chat Screen
- **Conversational AI Chatbot** - Powered by Anthropic Claude
- **Context-Aware Responses** - Tailored to Pakistani youth experiences
- **Quick Reply Suggestions** - Pre-set options for common situations
- **Language Toggle** - English (default) or Hinglish
- **Conversation History** - Maintains context within session

### 🧘 Exercises Screen
- **4-7-8 Breathing** - Calming breathing technique (5 min)
- **5-4-3-2-1 Grounding** - Sensory grounding for anxiety (5 min)
- **Body Scan Meditation** - Progressive relaxation (8 min)
- **Gratitude Practice** - Perspective shift exercise (3 min)
- **Progressive Muscle Relaxation** - Tension release (6 min)
- **Guided Journaling** - Reflection with prompts

### 📝 Journal Screen
- **Private Journaling** - Encrypted local storage
- **Conversational Prompts** - Friendly, relatable questions
- **Mood Tracking** - Optional mood logging with entries
- **Search & Filter** - View past entries
- **Edit & Delete** - Full control over entries

---

## 🔧 Project Structure

```
dilse/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── models.py                   # Database models
├── chatbot.py                  # AI chatbot logic
├── exercises.py                # Exercise data
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create from .env.example)
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navbar
│   ├── home.html              # Home screen
│   ├── chat.html              # Chat interface
│   ├── exercises.html         # Exercises screen
│   └── journal.html           # Journal screen
│
└── static/                     # Frontend assets
    ├── css/
    │   └── style.css          # Main stylesheet (calm colors)
    └── js/
        ├── main.js            # App initialization
        ├── api.js             # API helper functions
        ├── home.js            # Home screen logic
        ├── chat.js            # Chat interaction
        ├── exercises.js       # Exercise functionality
        └── journal.js         # Journal management
```

---

## 🎨 Design System

### Color Palette
```
Primary Blue:      #E8F4F8  (calm background)
Primary Purple:    #F0E8F8  (secondary accent)
Deep Blue:         #4A7C8C  (text, buttons)
Off-white:         #FAFAFA  (main background)
Light Gray:        #E8E8E8  (borders)
Dark Gray:         #333333  (primary text)
Accent Green:      #A8D5BA  (positive actions)
Accent Orange:     #F4B860  (warnings)
Accent Red:        #E8A9A9  (gentle alerts)
```

### Typography
- **Font Family:** System fonts (Inter, Segoe UI, Roboto)
- **Headings:** Bold, 24-32px
- **Body:** Regular, 14-16px
- **Line Height:** 1.6 (breathing room)

---

## 🤖 Chatbot Configuration

The chatbot uses Anthropic's Claude API with a specialized system prompt for Pakistani youth mental wellness.

### Key Features:
- **Non-judgmental** - No shame-based language
- **Culturally aware** - Understands specific stressors (exam pressure, family expectations, rishta stress)
- **Emotionally intelligent** - Validates feelings without dismissing
- **Safe escalation** - Provides crisis resources when needed
- **Language support** - English (default) and Hinglish

### Crisis Resources Built-in:
- Pakistan Crisis Helpline: 0345-5000-500
- Befrienders Pakistan: 0300-5000-500
- AASRA: 022-2754-6669

---

## 💾 Database Schema

### Users Table
- `id` - User ID
- `username` - Optional username
- `language_preference` - 'english' or 'hinglish'
- `created_at` - Account creation date

### Mood Entries
- `id` - Entry ID
- `user_id` - FK to users
- `mood` - 1-5 scale
- `date` - Date of entry
- `note` - Optional note

### Journal Entries
- `id` - Entry ID
- `user_id` - FK to users
- `content` - Journal text
- `date` - Date written
- `mood_at_time` - Optional mood (1-5)
- `prompt_used` - Which prompt was used

### Chat History
- `id` - Message ID
- `user_id` - FK to users
- `user_message` - User's message
- `bot_response` - Chatbot response
- `language` - Language used
- `timestamp` - When sent

### Exercise Completions
- `id` - Completion ID
- `user_id` - FK to users
- `exercise_name` - Which exercise
- `duration_seconds` - How long spent
- `timestamp` - When completed

---

## 🔐 Privacy & Security

### Data Protection
- **Journal entries** are stored securely (consider implementing encryption)
- **No data sharing** with third parties
- **Optional accounts** - works anonymously or with username
- **Local storage** for user ID and preferences
- **No tracking pixels** or external analytics

### API Security
- Environment variables for sensitive keys
- CORS enabled for frontend requests
- Input validation on all endpoints
- Error handling without exposing internals

---

## 🚀 Deployment

### Local Testing
```bash
python app.py
```

### Production Deployment Options

**Option 1: Heroku**
```bash
heroku login
heroku create dilse-app
git push heroku main
```

**Option 2: Railway**
- Connect GitHub repo
- Railway auto-deploys on push

**Option 3: PythonAnywhere**
- Upload files
- Configure WSGI
- Set environment variables

**Option 4: DigitalOcean/AWS**
```bash
# Use Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📊 API Endpoints

### User Management
- `POST /api/user` - Create/get user
- `GET /api/user/<id>` - Get user details
- `PUT /api/user/<id>/language` - Update language

### Mood Tracking
- `POST /api/user/<id>/mood` - Create mood entry
- `GET /api/user/<id>/mood` - Get mood history
- `GET /api/user/<id>/streak` - Get streak count

### Chat
- `POST /api/chat` - Send message to chatbot
- `GET /api/chat/quick-replies` - Get quick reply suggestions

### Exercises
- `GET /api/exercises` - List all exercises
- `GET /api/exercises/<id>` - Get exercise details
- `POST /api/user/<id>/exercise-completion` - Log completion
- `GET /api/user/<id>/exercise-history` - View history

### Journal
- `POST /api/user/<id>/journal` - Create entry
- `GET /api/user/<id>/journal` - Get entries
- `GET /api/journal/<id>` - Get specific entry
- `PUT /api/journal/<id>` - Update entry
- `DELETE /api/journal/<id>` - Delete entry
- `GET /api/journal/prompts` - Get writing prompts

---

## 🛠 Development

### Running Tests
```bash
# Currently no automated tests; add pytest for testing
pip install pytest
pytest
```

### Database Migrations
```bash
# Using Flask-Migrate (optional)
pip install Flask-Migrate
flask db init
flask db migrate
flask db upgrade
```

### Adding New Features
1. Add database model in `models.py`
2. Add API endpoint in `app.py`
3. Create/update HTML template in `templates/`
4. Add JavaScript logic in `static/js/`
5. Update CSS in `static/css/style.css`

---

## 📈 Future Enhancements

- **User accounts** with cloud sync
- **Mood pattern analysis** using ML
- **Community features** (anonymous peer support)
- **Integration with professional resources**
- **Offline mode** (service worker)
- **Mobile app** (React Native)
- **Multi-language support** (Urdu, Sindhi, etc.)
- **Video tutorials** for exercises
- **Habit tracking** (meditation streak, etc.)
- **Integration with mental health organizations**

---

## 🤝 Contributing

This is an educational project. To contribute:
1. Fork the project
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## ⚠️ Important Notes

### This is NOT a Replacement for Professional Help
Dil Se is a wellness companion, not a therapy platform. If you or someone you know is experiencing:
- Suicidal thoughts
- Severe mental health crisis
- Self-harm urges
- Substance abuse

**Please reach out to:**
- **Pakistan Crisis Helpline:** 0345-5000-500
- **Befrienders Pakistan:** 0300-5000-500
- **AASRA:** 022-2754-6669
- **International Crisis:** Find local resources

### API Rate Limits
Anthropic API has rate limits. Monitor usage in your dashboard.

---

## 📝 License

This project is created for educational purposes. 

---

## 👤 Author

**Rabeea Hussain**  
AI Mental Wellness Project  
Created: May 2026

---

## 🙏 Acknowledgments

- Anthropic for the Claude API
- Pakistani mental health communities
- All resources on cultural competency in mental health

---

## 📞 Support

For issues or questions:
1. Check the [Project Documentation](PROJECT_DOCUMENTATION.md)
2. Review API endpoints above
3. Check browser console for JavaScript errors
4. Review Flask logs in terminal

---

**Built with ❤️ for Pakistani youth mental wellness**
