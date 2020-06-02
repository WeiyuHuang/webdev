import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def get_paginated_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in questions]
    return formatted_questions[start:end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for all origins.
    CORS(app, resources={'/': {'origins': '*'}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        """ Set Access Control """

        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS'
        )

        return response

    @app.route('/categories')
    def get_all_categories():
        """
        Get categories endpoint

        Return all categories or status 500 if there is an error
        """

        try:
            categories = Category.query.all()
            categories_dict = {}

            for category in categories:
                categories_dict[category.id] = category.type

            return jsonify({
                'success': True,
                'categories': categories_dict
            }), 200
        except:
            abort(500)


    @app.route('/questions')
    def get_questions():
        """
        Get paginated questions

        Return all questions, listed as paginated, or status 404
        """
        try:
            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()
            current_questions = get_paginated_questions(request, questions)

            if len(current_questions) == 0:
                abort(404)

            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type

            return jsonify({
                'success': True,
                'total_questions': len(questions),
                'categories': categories_dict,
                'questions': current_questions
            }), 200
        except:
            abort(422)


    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''


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

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    return app
