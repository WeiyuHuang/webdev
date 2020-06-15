import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# Route


@app.route('/drinks')
def get_drinks():
    """
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
            where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    """
    drinks = Drink.query.all()
    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    }), 200


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(token):
    """
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
            where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    """
    drinks = Drink.query.all()
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drinks(token):
    """
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
            where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
    """
    req = request.get_json()

    try:
        req_recipe = req['recipe']
        if isinstance(req_recipe, dict):
            req_recipe = [req_recipe]

        drink = Drink()
        drink.title = req['title']
        drink.recipe = json.dumps(req_recipe)  # convert object to a string
        drink.insert()

    except BaseException:
        abort(400)

    drinks = Drink.query.all()
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(token, drink_id):
    """
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
            where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
    """
    new_drink_data = json.loads(request.data.decode('utf-8'))
    drink_data = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not drink_data:
        abort(404)

    try:
        if 'title' in new_drink_data:
            setattr(drink_data, 'title', new_drink_data['title'])
        if 'recipe' in new_drink_data:
            setattr(drink_data, 'recipe', json.dumps(new_drink_data['recipe']))
        Drink.update(drink_data)
    except BaseException:
        abort(400)

    drinks = Drink.query.all()
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200


@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(token, drink_id):
    """
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id}
            where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    """
    drink_data = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not drink_data:
        abort(404)

    try:
        Drink.delete(drink_data)
    except BaseException:
        abort(400)

    return jsonify({
        'success': True,
        'delete': drink_id
    }), 200


# Error handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    error_data = {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }
    return jsonify(error_data), 404


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405
