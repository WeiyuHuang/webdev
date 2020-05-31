import os
import random
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from models import setup_db, Book

BOOKS_PER_SHELF = 8

def paginate_books(request, selection):
	page = request.args.get('page', 1, type=int)
	start = (page - 1) * BOOKS_PER_SHELF
	end = start + BOOKS_PER_SHELF

	formatted_books = [book.format() for book in selection]
	return formatted_books[start:end]

def create_app(test_config=None):
	app = Flask(__name__)
	setup_db(app)
	CORS(app)

	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
		response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
		return response

	@app.route('/books')
	def get_books():
		books = Book.query.order_by(Book.id).all()

		return jsonify({
			'success': True,
			'books': paginate_books(request, books),
			'total_books': len(books)
		})

	@app.route('/books/<int:book_id>')
	def get_book(book_id):
		book = Book.query.filter(Book.id == book_id).one_or_none()

		if book is None:
			abort(404)

		return jsonify({
			'success': True,
			'book': book.format()
		})

	@app.route('/books/<int:book_id>', methods=['PATCH'])
	def update_book(book_id):
		body = request.get_json()

		try:
			book = Book.query.filter(Book.id == book_id).one_or_none()
			if book is None:
				abort(404)

			if 'rating' in body:
				book.rating = int(body['rating'])
				book.update()
				return jsonify({
					'success': True,
					'id': book.id
				})
		except:
			abort(400)

	@app.route('/books/<int:book_id>', methods=['DELETE'])
	def delete_book(book_id):
		try:
			book = Book.query.filter(Book.id == book_id).one_or_none()

			if book is None:
				abort(404)

			book.delete()
			books = Book.query.order_by(Book.id).all()

			return jsonify({
				'success': True,
				'books': paginate_books(request, books),
				'deleted': book.id,
				'total_books': len(books)
			})

		except:
			abort(422)

	@app.route('/books', methods=['POST'])
	def create_book():
		body = request.get_json()
		title = body.get('title', None)
		author = body.get('author', None)
		rating = body.get('rating', None)

		try:
			book = Book(title=title, author=author, rating=rating)
			book.insert()

			books = Book.query.order_by(Book.id).all()

			return jsonify({
				'success': True,
				'books': paginate_books(request, books),
				'created': book.id,
				'total_books': len(books)
			})
		except:
			abort(422)

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
			"success": False,
			"error": 404,
			"message": "resource not found"
		}), 404

	@app.errorhandler(422)
	def cannot_update(error):
		return jsonify({
			"success": False,
			"error": 422,
			"message": "unprocessable"
		}), 422

	@app.errorhandler(400)
	def not_exist(error):
		return jsonify({
			"success": False,
			"error": 400,
			"message": "bad request"
		}), 400

	@app.errorhandler(405)
	def not_exist(error):
		return jsonify({
			"success": False,
			"error": 405,
			"message": "method not allowed"
		}), 405

	return app