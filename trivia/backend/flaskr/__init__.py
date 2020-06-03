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


def get_random_question(questions):
    return questions[random.randint(0, len(questions) - 1)]


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

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()

            return jsonify({
                'success': True,
                'question_deleted': question.id
            }), 200
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()

        question = data.get('question', '')
        answer = data.get('answer', '')
        difficulty = data.get('difficulty', '')
        category = data.get('category', '')

        # ensure data is not empty
        if (question == '' or answer == '' or
                difficulty == '' or category == ''):
            abort(422)

        try:
            question = Question(question=question, answer=answer,
                                difficulty=difficulty, category=category)
            question.insert()

            return jsonify({
                'success': True,
                'question_created': question.id
            }), 201
        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.get_json()
        search_term = data.get('searchTerm', '')

        if search_term == '':
            abort(422)

        try:
            questions = Question.query.filter(Question.question.
                                              ilike(f'%{search_term}%')).all()

            return jsonify({
                'success': True,
                'questions': get_paginated_questions(request, questions),
                'total_questions': len(questions),
                'current_category': [question.category for question in questions]
            }), 200
        except:
            abort(404)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):

        category = Category.query.filter_by(id=category_id).one_or_none()
        if category is None:
            abort(422)

        questions = Question.query.filter_by(category=category_id).all()

        return jsonify({
            'success': True,
            'questions': get_paginated_questions(request, questions),
            'total_questions': len(questions),
            'current_category': category.type
        }), 200

    @app.route('/quizzes', methods=['POST'])
    def play_quiz_question():
        data = request.get_json()
        previous_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')

        if (previous_questions is None) or (quiz_category is None):
            abort(400)

        if quiz_category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(
                category=quiz_category['id']).all()

        next_question = get_random_question(questions)
        while next_question.id in previous_questions:
            next_question = get_random_question(questions)

            if (len(previous_questions) == len(questions)):
                return jsonify({
                    'success': True
                })

        return jsonify({
            'success': True,
            'question': next_question.format()
        }), 200

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'An error occured. Please try again later'
        }), 500

    @app.errorhandler(422)
    def unprocesable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    return app
