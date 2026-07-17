# Dil Se - AI-Powered Mental Wellness Companion
## Project Documentation

### 📌 Project Overview
**Dil Se** (From the Heart) is a culturally-tailored mental wellness companion app designed specifically for Pakistani teens and young adults. It addresses the unique mental health barriers faced by this demographic through relatable, shame-free conversations in a language (English) that feels emotionally safe and accessible.

---

## 🎯 Why This Project Matters

**The Core Problem:** In Pakistan, the biggest barrier to mental health isn't access—it's shame. Young people avoid seeking help due to:
- Fear of being called "pagal" (crazy)
- Worry about being a burden on family
- Cultural and religious expectations around emotions
- Lack of relatable, non-clinical resources

**The Solution:** Dil Se provides:
- ✅ English-first interface (the language of emotional introspection for many Pakistani Gen Z)
- ✅ Optional Hinglish/Urdu toggle for those who prefer it
- ✅ Conversational tone (like a trusted friend, not a therapist)
- ✅ Relatable scenarios (exam pressure, family expectations, rishta stress, career anxiety)
- ✅ Evidence-based wellness techniques explained simply
- ✅ Private journaling without judgment
- ✅ Mood tracking over time to visualize patterns

---

## 🎨 Design Philosophy

**Minimal & Calm:**
- Clean, spacious interface
- Calming color palette: soft light blues and purples
- No overwhelming options or clinical language
- Smooth, intuitive navigation
- Accessibility-first (clear typography, high contrast)

**Culturally Attuned:**
- Understands emotional code-switching (using English for vulnerable conversations)
- Journal prompts written like a friend asking, not a therapist
- Chatbot responses avoid corporate wellness speak ("I hear you")
- Quick-reply options address real Pakistan-specific stressors

---

## 📱 Four Core Screens

### 1. **Home Screen**
**Purpose:** Daily mood check-in and quick access to tools

**Elements:**
- Large mood check-in button ("How are you feeling today?")
- Visual mood history (mini chart of the past 7 days)
- Weekly streak counter (motivational indicator)
- Quick-access cards for:
  - "Talk to Dil Se" (Chatbot)
  - "Do an Exercise" (Breathing, grounding techniques)
  - "Journal" (Private reflection)
- Helpful tip of the day

**Functionality:**
- Tracks mood on a 5-point scale with emoji representation
- Stores mood data for historical analysis
- Encourages daily engagement without pressure

---

### 2. **AI Chat Screen**
**Purpose:** Have a judgment-free conversation with an AI companion

**Elements:**
- Conversational chat interface
- Pre-set quick replies for common situations:
  - "I'm stressed about exams"
  - "Parents are pressuring me"
  - "I don't know what career I want"
  - "I feel alone"
  - "I'm anxious about something"
  - "I just need to vent"
- Full free-text message input
- Language toggle (English/Hinglish)
- Conversation history maintained during session

**Functionality:**
- Uses Anthropic Claude API for intelligent, empathetic responses
- Tailored system prompt for Pakistani youth context
- Avoids clinical jargon
- Never suggests to "just be positive" or dismissive platitudes
- Can escalate to professional resources if needed
- Responses change dynamically based on language selection

**Sample Bot Behavior:**
- User: "I failed my exam"
- Bot: "That's really tough. Exams can feel like everything sometimes, but one exam doesn't define you. What's going through your head right now—is it more about the exam itself, or what people might think?"

---

### 3. **Exercises Screen**
**Purpose:** Learn and practice evidence-based wellness techniques

**Elements:**
- Exercise library with:
  - **4-7-8 Breathing:** Guided breathing with timer (4 count inhale, 7 count hold, 8 count exhale)
  - **5-4-3-2-1 Grounding:** Sensory grounding technique to manage anxiety
  - **Body Scan Meditation:** Progressive relaxation
  - **Journaling Prompts:** Guided reflection
  - **Gratitude Practice:** Simple positivity anchor
- Interactive progress bar during exercises
- Timer/counter
- Brief explanation of why each technique works
- "Completed" badges for motivation

**Functionality:**
- Each exercise includes:
  - Simple, non-jargon explanation
  - Step-by-step instructions
  - Visual/audio guidance (if available)
  - Time commitment (most are 3-5 minutes)
- Tracks completed exercises
- Can bookmark favorites

---

### 4. **Journal Screen**
**Purpose:** Private, judgment-free space for reflection

**Elements:**
- Private journal entries (stored locally/encrypted)
- Daily prompts (written conversationally):
  - "What did you not say today but wish you had?"
  - "What's one thing you're scared of that no one knows?"
  - "If you could talk to your parents with no consequences, what would you say?"
  - "What's the smallest thing that made you smile today?"
  - "What are you carrying right now that you're tired of carrying?"
- Free-write option (no prompt)
- Date-tagged entries
- Search/filter by date or mood
- Dark mode option for nighttime journaling
- Export option (private data)

**Functionality:**
- All entries are private (client-side encrypted or stored securely)
- Entries tagged with date and optional mood at time of writing
- Supports long-form writing (not limited to character count)
- No judgment or feedback—purely reflection space
- Optional mood tracking alongside writing

---

## 💻 Technical Architecture

### Backend (Flask + Python)
```
dilse/
├── app.py                 # Flask main application
├── config.py              # Configuration (API keys, database)
├── models.py              # Database models (User, MoodEntry, JournalEntry, etc.)
├── chatbot.py             # Chatbot logic (Anthropic API integration)
├── exercises.py           # Exercise data and logic
├── auth.py                # User authentication (optional, for future)
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (not committed)
```

### Frontend (HTML/CSS/JavaScript)
```
static/
├── css/
│   ├── style.css          # Main styling (calm colors: light blue, purple)
│   ├── home.css           # Home screen specific styles
│   ├── chat.css           # Chat interface styles
│   ├── exercises.css      # Exercise screen styles
│   └── journal.css        # Journal screen styles
├── js/
│   ├── main.js            # Core app logic
│   ├── chat.js            # Chat interaction
│   ├── exercises.js       # Exercise functionality
│   ├── journal.js         # Journal management
│   └── api.js             # API communication
└── images/
    └── (icons, mood emojis, etc.)

templates/
├── base.html              # Base template
├── home.html              # Home screen
├── chat.html              # Chat screen
├── exercises.html         # Exercises screen
└── journal.html           # Journal screen
```

### Database
- **SQLite** (for simplicity) or **PostgreSQL** (for scalability)
- Tables:
  - `users` (id, username, created_at, language_preference)
  - `mood_entries` (id, user_id, mood, date, timestamp)
  - `journal_entries` (id, user_id, content, date, mood_at_time, encrypted)
  - `chat_history` (id, user_id, message, response, timestamp)
  - `exercise_completions` (id, user_id, exercise_name, timestamp)

---

## 🔐 Key Features

### 1. **Mood Tracking**
- Daily mood check-in (5-point scale with emojis)
- Visual mood history (7-day and 30-day charts)
- Mood-based quick replies from chatbot
- Trends analysis (identifying patterns)

### 2. **AI Chatbot**
- Powered by Anthropic Claude API
- Context-aware responses about Pakistani youth issues
- Quick-reply suggestions for faster interaction
- Maintains conversation history within session
- Escalation guidelines for serious concerns

### 3. **Language Toggle**
- Default: English (emotionally accessible)
- Toggle: Hinglish/Urdu for those who prefer it
- Affects:
  - UI labels and buttons
  - Chat responses
  - Journal prompts
  - Exercise descriptions
- User preference saved

### 4. **Wellness Exercises**
- Guided breathing techniques
- Grounding exercises for anxiety
- Simple meditations
- Interactive progress tracking
- Educational explanations

### 5. **Private Journaling**
- Encrypted local storage or secure server-side storage
- No data analysis/tracking (user privacy prioritized)
- Conversational prompts
- Free-write option
- Export functionality

### 6. **Streak Counter**
- Daily engagement encouragement
- Motivational badges
- No shame for broken streaks (can restart anytime)

---

## 📊 Color Palette & Design

**Primary Colors:**
- Calm Light Blue: `#E8F4F8` (backgrounds, accents)
- Soft Purple: `#F0E8F8` (secondary accents, hover states)
- Deep Blue: `#4A7C8C` (text, buttons, primary actions)

**Neutral Colors:**
- Off-white: `#FAFAFA` (main background)
- Light Gray: `#E8E8E8` (borders, dividers)
- Dark Gray: `#333333` (primary text)

**Accent Colors:**
- Green: `#A8D5BA` (positive actions, completed)
- Orange: `#F4B860` (warnings, alerts)
- Soft Red: `#E8A9A9` (gentle alerts)

**Typography:**
- Font: Inter or Segoe UI (clean, modern, highly readable)
- Headings: Bold, 24-32px
- Body: Regular, 14-16px
- Line-height: 1.6 (breathing room)

---

## 🚀 Technology Stack

### Backend
- **Flask** - Lightweight Python web framework
- **Anthropic Python SDK** - For Claude API integration
- **SQLAlchemy** - ORM for database
- **Flask-CORS** - For cross-origin requests
- **python-dotenv** - Environment variable management
- **requests** - HTTP library for external APIs

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with flexbox/grid
- **Vanilla JavaScript** - No heavy frameworks (keep it simple)
- **Fetch API** - For async requests
- **Chart.js** - For mood trend visualization (optional)

### Infrastructure
- **Database:** SQLite (development) or PostgreSQL (production)
- **Hosting:** Can be deployed on Heroku, Railway, Render, or AWS
- **API:** Anthropic Claude API

---

## 📋 User Journey

### First Time User
1. Opens app
2. Creates optional account (or uses anonymously)
3. Sets language preference
4. Takes mood check-in
5. Sees home screen with quick-access cards
6. Can explore any of the 4 screens

### Daily User
1. Opens app
2. Takes mood check-in (builds streak)
3. Chats with Dil Se OR does an exercise OR journals
4. Sees progress/history
5. Gets subtle encouragement to return tomorrow

### Returning User with Concerns
1. Opens app
2. Navigates to chat
3. Describes concern in conversational English
4. Gets empathetic, culturally-aware response
5. Can continue conversation or try an exercise
6. Optionally journals about it after

---

## 🔄 Data Flow

```
User Input
    ↓
Frontend (HTML/JS)
    ↓
Flask API (/api/mood, /api/chat, /api/journal, etc.)
    ↓
Database (SQLite/PostgreSQL) + External APIs (Anthropic)
    ↓
Response sent back to Frontend
    ↓
User sees result in UI
```

---

## 🛡️ Privacy & Safety

- **All journal entries are private** (encrypted or client-side only)
- **No tracking of emotions** beyond user-initiated mood checks
- **No data sold or shared** with third parties
- **Optional account creation** (can use anonymously)
- **Safe escalation:** If user mentions serious harm, provide crisis resources:
  - **Pakistan Crisis Helpline:** 0345-5000-500
  - **Befrienders Pakistan:** 0300-5000-500
  - **AASRA (Emotional support):** 022-2754-6669

---

## 📈 Success Metrics

How we'll measure if Dil Se is working:
- Daily active users
- Average session duration
- Chat conversations per user
- Journal entries written
- Streak maintenance rate
- User satisfaction (in-app feedback)
- Mood trend improvements over time

---

## 🔮 Future Enhancements

- **User accounts** with cloud sync
- **Mood pattern analysis** (ML to identify triggers)
- **Community features** (anonymous peer support groups)
- **Professional resource integration** (therapist directory)
- **Offline mode** (works without internet)
- **Mobile app** (iOS/Android)
- **Parent/caregiver resources** (explaining how to support)
- **Multi-language support** (Urdu, Sindhi, etc.)
- **Integration with local Pakistani mental health organizations**

---

## 👨‍💻 Development Roadmap

### Phase 1: MVP (2-3 weeks)
- ✅ Home screen with mood check-in
- ✅ Basic chat interface
- ✅ Simple exercises screen
- ✅ Basic journaling
- ✅ Language toggle

### Phase 2: Polish & Personalization (1-2 weeks)
- Add mood history charts
- Improve chatbot responses
- Add more exercises
- Streak counter
- Better UI/UX

### Phase 3: Launch & Gather Feedback (1 week)
- Deploy to hosting platform
- Beta testing with target users
- Gather feedback

### Phase 4: Improvements (Ongoing)
- Add user accounts
- Implement suggested features
- Improve AI responses based on feedback

---

## 📝 Setup Instructions

See `README.md` for installation and running instructions.

---

## 👤 Author
**Rabeea Hussain** - AI Mental Wellness Project  
Created: May 2026

---

**Last Updated:** May 2, 2026
