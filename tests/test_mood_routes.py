import unittest
from datetime import date

from app import app, db
from models import User


class MoodRouteFallbackTests(unittest.TestCase):
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

    def test_mood_route_falls_back_to_session_user(self):
        user = User(username='session-user', language_preference='english')
        db.session.add(user)
        db.session.commit()

        client = self.app.test_client()
        with client.session_transaction() as session:
            session['user_id'] = user.id

        response = client.post('/api/user/999999/mood', json={'mood': 4, 'note': 'testing'})

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['mood'], 4)


if __name__ == '__main__':
    unittest.main()
