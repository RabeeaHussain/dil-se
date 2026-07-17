from models import MoodEntry
from datetime import datetime, timedelta

def predict_mood(user_id):
    """
    Simple weighted average prediction based on recent mood history.
    Returns a dict with predicted mood and confidence message.
    """
    today = datetime.now().date()
    
    # Fetch last 14 days of mood entries
    entries = MoodEntry.query.filter(
        MoodEntry.user_id == user_id,
        MoodEntry.date >= today - timedelta(days=14)
    ).order_by(MoodEntry.date.desc()).all()

    if len(entries) < 3:
        return {
            "predicted_mood": None,
            "message": "Check in a few more days to unlock mood predictions.",
            "confidence": "low"
        }

    # Weighted average — recent days count more
    weights = [2 if i < 3 else 1 for i in range(len(entries))]
    weighted_sum = sum(e.mood * w for e, w in zip(entries, weights))
    total_weight = sum(weights)
    predicted = round(weighted_sum / total_weight, 1)

    # Trend: compare last 3 days vs previous 4
    recent = [e.mood for e in entries[:3]]
    older  = [e.mood for e in entries[3:7]] if len(entries) >= 7 else recent
    trend = sum(recent) / len(recent) - sum(older) / len(older)

    if trend > 0.5:
        trend_label = "improving 📈"
    elif trend < -0.5:
        trend_label = "dipping 📉"
    else:
        trend_label = "steady ➡️"

    mood_labels = {1: "Terrible", 2: "Bad", 3: "Okay", 4: "Good", 5: "Great"}
    mood_rounded = max(1, min(5, round(predicted)))

    return {
        "predicted_mood": predicted,
        "predicted_label": mood_labels[mood_rounded],
        "trend": trend_label,
        "message": f"Based on your recent check-ins, you might feel {mood_labels[mood_rounded]} today. Your mood has been {trend_label}.",
        "confidence": "medium" if len(entries) >= 7 else "low"
    }