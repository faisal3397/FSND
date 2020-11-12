import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "TEST Question",
            "answer": "TEST Answer",
            "difficulty": 3,
            "category": 6
        }

        self.bad_request_question = {
            "question": "TEST Question",
            "answer": "TEST Answer"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])

    def test_get_all_categories_not_found(self):
        res = self.client().get('/category')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Not found")
        self.assertEqual(data["success"], False)

    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
    
    def test_get_questions_exceeding_valid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Not found")
        self.assertEqual(data["success"], False)

    def test_if_question_not_found(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Not found")
        self.assertEqual(data["success"], False)
    
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["message"], "Question Created")
    
    def test_400_create_question_bad_request(self):
        res = self.client().post('/questions', json=self.bad_request_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["error"], 400)
        self.assertEqual(data["message"], "Bad Request")
        self.assertEqual(data["success"], False)

    def test_delete_question(self):
        # Use the id of the question created in the create question test case
        res = self.client().delete('/questions/23')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 23).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["message"], "Question with ID: 23 is Deleted")
        self.assertEqual(question, None)
    
    def test_search_question(self):
        res = self.client().post('/questions/search', json={"searchTerm": "title"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["currentCategory"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
    
    def test_search_result_not_found(self):
        res = self.client().post('/questions/search', json={"searchTerm": "dsgsfgerer"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Not found")
        self.assertEqual(data["success"], False)
    
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["currentCategory"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])

    def test_404_get_questions_by_invalid_category(self):
        res = self.client().get('/categories/400/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Not found")
        self.assertEqual(data["success"], False)
    
    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={
            "previous_questions": [],
            "quiz_category": {
                "type": "History",
                "id": 4
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])

    def test_play_quiz_bad_request(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["error"], 400)
        self.assertEqual(data["message"], "Bad Request")
        self.assertEqual(data["success"], False)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()