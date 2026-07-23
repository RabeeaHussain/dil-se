from models import MoodEntry
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np


def predict_mood(user_id):
    """
    Predict tomorrow's mood using Linear Regression.
    Works with as little as 3 mood entries.
    """

    today = datetime.now().date()

    # Fetch last 14 days of moods
    entries = MoodEntry.query.filter(
        MoodEntry.user_id == user_id,
        MoodEntry.date >= today - timedelta(days=14)
    ).order_by(MoodEntry.date.asc()).all()

    # Need at least 3 points to fit a regression line
    if len(entries) < 3:
        return {
            "predicted_mood": None,
            "message": "Add at least 3 mood entries to unlock AI predictions.",
            "confidence": "low"
        }

    # X = day numbers
    X = np.array(range(len(entries))).reshape(-1, 1)

    # y = mood values
    y = np.array([entry.mood for entry in entries])

    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict tomorrow
    tomorrow = np.array([[len(entries)]])
    prediction = model.predict(tomorrow)[0]

    # Keep prediction within valid mood range
    prediction = max(1, min(5, round(prediction, 1)))

    mood_labels = {
        1: "Terrible",
        2: "Bad",
        3: "Okay",
        4: "Good",
        5: "Great"
    }

    rounded = round(prediction)

    # Determine trend from regression slope
    slope = model.coef_[0]

    if slope > 0.2:
        trend = "improving 📈"
    elif slope < -0.2:
        trend = "declining 📉"
    else:
        trend = "stable ➡️"

    return {
        "predicted_mood": prediction,
        "predicted_label": mood_labels[rounded],
        "trend": trend,
        "message": f"Our AI predicts your mood tomorrow may be {mood_labels[rounded]}. Your overall mood trend appears to be {trend}.",
        "confidence": "medium" if len(entries) >= 5 else "low"
    }