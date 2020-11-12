import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# a helper method that formats the categories,
# returns a dictionary that holds all the categories,
# so that it can be handled in client-side


def get_result_categories(categories):
    result_categories = {}
    formatted_categories = [category.format() for category in categories]

    for category in formatted_categories:
        result_categories[category["id"]] = category["type"]

    return result_categories


def get_current_category(categories):
    result_current_category = {}
    current_category = categories[random.randrange(0, 6)].format()
    result_current_category[current_category["id"]] = current_category["type"]

    return result_current_category


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins.
  Delete the sample route after completing the TODOs
  '''
    CORS(app)
    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        response_data = get_result_categories(categories)

        return jsonify({'categories': response_data})

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination
  at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        categories = Category.query.all()
        formatted_questions = [question.format() for question in questions]

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        result_questions = formatted_questions[start:end]
        if len(result_questions) == 0:
            abort(404)

        result_categories = get_result_categories(categories)
        result_current_category = get_current_category(categories)

        return jsonify({
            'questions': result_questions,
            'total_questions': len(formatted_questions),
            'categories': result_categories,
            'current_category': result_current_category
        })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question,
  the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query \
                .filter(Question.id == question_id) \
                .one_or_none()

            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                'message': 'Question with ID: ' + question_id + ' is Deleted'
            })
        except():
            abort(422)

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        question = body.get("question", None)
        answer = body.get("answer", None)
        category = body.get("category", None)
        difficulty = body.get("difficulty", None)

        if question is None or \
                answer is None \
                or category is None \
                or difficulty is None:
            abort(400)

        try:
            question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
            question.insert()
            return jsonify({'message': 'Question Created'}), 201
        except():
            abort(400)

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_term = request.json["searchTerm"]
        # add %% before and after search term,
        # to get all the results that has the search term in their names
        search = "%{}%".format(search_term)
        questions = Question.query \
            .filter(Question.question.ilike(search)).all()
        result_questions = [question.format() for question in questions]

        if len(result_questions) == 0:
            abort(404)

        categories = Category.query.all()
        result_current_category = get_current_category(categories)

        return jsonify({
            "questions": result_questions,
            "totalQuestions": len(result_questions),
            "currentCategory": result_current_category
        })

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

    @app.route('/categories/<category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query\
          .filter(Category.id == category_id).one_or_none()

        if category is None:
            abort(404)

        formatted_category = category.format()
        questions = Question.query.filter_by(category=formatted_category["id"])
        formatted_questions = [question.format() for question in questions]
        return jsonify({
            "questions": formatted_questions,
            "totalQuestions": len(formatted_questions),
            "currentCategory": formatted_category["type"]
        })

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        previous_questions = request.json["previous_questions"]
        quiz_category = request.json["quiz_category"]
        questions = []

        if quiz_category["id"] == 0:
            questions = Question.query.all()
        else:
            category = Category.query.get(quiz_category["id"]).format()
            questions = Question.query.filter_by(category=category["id"])

        formatted_questions = [question.format() for question in questions]
        random_question = {}

        for question in formatted_questions:
            if question["id"] not in previous_questions:
                random_question = question

        if random_question == {}:
            return jsonify({
                "message": "Game Over"
            })
        else:
            return jsonify({
                "question": random_question
            })

    '''
  @TODO:
  Create error handlers for all expected errors
  including 400, 404, 422 and 500.
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app
