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

'''
@DONE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES


'''
@DONE implement endpoint
    GET /drinks
'''


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    short_drinks = []
    if len(drinks) > 0:
        short_drinks = [drink.short() for drink in drinks]

    return jsonify({
        "success": True,
        "drinks": short_drinks
    })


'''
@DONE implement endpoint
    GET /drinks-detail
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    drinks = Drink.query.all()
    long_drinks = []

    if len(drinks) > 0:
        long_drinks = [drink.long() for drink in drinks]

    return jsonify({
        "success": True,
        "drinks": long_drinks
    })


'''
@DONE implement endpoint
    POST /drinks
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    body = request.get_json()
    title = body.get("title", None)
    recipe = body.get("recipe", None)
    recipe_string = json.dumps(recipe)

    if title is None or recipe is None:
        abort(400)

    try:
        drink = Drink(title=title, recipe=recipe_string)
        drink.insert()

        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })
    except():
        abort(400)


'''
@DONE implement endpoint
    PATCH /drinks/<id>
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(jwt, drink_id):
    body = request.get_json()
    title = body.get("title")
    recipe = body.get("recipe")
    recipe_string = json.dumps(recipe)

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            abort(404)

        drink.title = title
        drink.recipe = recipe_string
        drink.update()

        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })
    except():
        abort(422)


'''
@DONE implement endpoint
    DELETE /drinks/<id>
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            "success": True,
            "delete": drink.id
        })
    except():
        abort(422)


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@DONE implement error handlers using the @app.errorhandler(error) decorator

'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400


'''
@DONE implement error handler for 404
    error handler should conform to general task above 
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
    }), 404


'''
@DONE implement error handler for AuthError
    error handler should conform to general task above 
'''


@app.errorhandler(AuthError)
def auth_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code


