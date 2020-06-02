import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

def create_dummy_question():
    question = Question(
        question='This is a test question',
        answer='this is a test answer',
        difficulty=1,
        category='1'
    )
    question.insert()

    return question.id

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['total_questions'])

    def test_get_paginated_questions_error_out_of_bound(self):
        response = self.client().get('/questions?page=10000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_question(self):
        dummy_question_id = create_dummy_question()

        response = self.client().delete('/questions/{}'.format(dummy_question_id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question_deleted'], dummy_question_id)

    def test_delete_question_error_not_exist(self):
        response = self.client().delete('/questions/10000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_create_question(self):
        dummy_question_data = {
            "question": "This is a dummy question",
            "answer": "This is a dummy answer",
            "difficulty": 1,
            "category": 1
        }

        response = self.client().post('/questions', json=dummy_question_data)
        data = json.loads(response.data)
        self.client().delete('/questions/{}'.format(data['question_created']))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_create_question_error_empty_inputs(self):

        dummy_question_data = {
            "question": "",
            "answer": "",
            "difficulty": 1,
            "category": 1
        }

        response = self.client().post('/questions', json=dummy_question_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()