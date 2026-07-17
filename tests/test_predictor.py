import unittest
from datetime import date, timedelta

from app import app, db
from models import MoodEntry, User
from predictor import predict_mood


class MoodPredictionTests(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_predict_mood_returns_prediction_for_enough_history(self):
        user = User(username='predictor-test', language_preference='english')
        db.session.add(user)
        db.session.commit()

        today = date.today()
        moods = [4, 3, 4, 2, 3, 5]
        for offset, mood in enumerate(moods):
            db.session.add(
                MoodEntry(
                    user_id=user.id,
                    mood=mood,
                    date=today - timedelta(days=offset),
                    note='test entry',
                )
            )
        db.session.commit()

        prediction = predict_mood(user.id)

        self.assertIsNotNone(prediction['predicted_mood'])
        self.assertIn(prediction['confidence'], {'low', 'medium'})
        self.assertIn('predicted_label', prediction)
        self.assertIn('message', prediction)

    def test_predict_mood_returns_low_confidence_when_history_is_short(self):
        user = User(username='predictor-short', language_preference='english')
        db.session.add(user)
        db.session.commit()

        today = date.today()
        for offset, mood in enumerate([4, 3]):
            db.session.add(
                MoodEntry(
                    user_id=user.id,
                    mood=mood,
                    date=today - timedelta(days=offset),
                    note='test entry',
                )
            )
        db.session.commit()

        prediction = predict_mood(user.id)

        self.assertIsNone(prediction['predicted_mood'])
        self.assertEqual(prediction['confidence'], 'low')


if __name__ == '__main__':
    unittest.main()
