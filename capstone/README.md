# Udacity Full Stack Developer Nanodegree Capstone Project

## Motivation

Create a back-end web application which demonstrates the functinality of endpoints with Role Based Access tests.

- Coding standards: PEP8 compliant code
- Authorization: RBAC roles and JWT is implemented via the 3rd party Auth0.
- Testing: Comprehensive RBAC and error handling.
- Documentation: Setup instructions and endpoints has been documented.
- Deployment: The final code is deployed on Heroku and tests can be run agains its database.

This project is for a movie agency which has movies and actors listed in its database. There are two roles, Casting Assistant and Casting Director. For viewing the list of movies and actors in the database the user shoul be logged with the Casting Assistant role. To add, delete and modify movies the role of the user has to be Casting Director.

## Setup and dependencies

This project is based on Python3, pip and psql.

To start the project create a virtual environment in the downloaded project folder with the following bash commands:

```bash
python3 -m venv env-web
source env-web/bin/activate
```

After this, install the required packages through pip.

```bash
pip install -r requirements.txt
```

There are environment variables such as JWT codes and the database URL are stored in the setup.sh file. Please run this to execute.

```bash
source setup.sh
```

Following this the application endpoints are ready to be tested with the deployed server by running:

```bash
python3 test_app.py
```

##### Note: If the existing JWT's are expired new ones can be obtained by following the link on the application homepage.

1) For the Casting Director JWT, please log in with the following credentials:

- email: director@bear.com
- password: Udacity123!


2) For the Casting Assistant JWT, please login with the following credentials:

- email: assistant@bear.com
- password: Udacity123!

You'll be redirected to the main page where the JWT can be copied from the URL after the # part. Paste the JWT into the setup.sh into the CA_TOKEN and CD_TOKEN variables accordingly.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle backend requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight sqlite database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Avaible Endpoints

The available operations are:

- [/](#homePage)
- [GET movies](#getMovie)
- [GET actors](#getActor)
- [DELETE movies](#deleteMovie)
- [POST movies](#postMovie)
- [PATCH movies](#patchMovie)

<h4 id="homePage"></h4>

> '/'

This is the main page of the application, it displays a link to log in and generate new JWT tokens.

<h4 id="getMovie"></h4>

> **GET '/movies'**

This endpoint fetches all movies.

**Request Arguments:**

- _None_

**Returns:** The return should include an success: True message along with a list of movies in JSON format.

```javascript
{
	'success': True,
	'movies': {
		'id': 'movie id', 
		'title': 'movie title',
  		'realease_date': '2020-01-01'
  	}
}
```

<h4 id="getActor"></h4>

> **GET '/actors'**

This endpoint fetches all actors.

**Request Arguments:**

- _None_

**Returns:** The return should include an success: True message along with a list of movies in JSON format.

```javascript
{
	'success': True,
	'movies': {
		'id': 'actor id', 
		'name': 'name of actor',
		'age': age of actor
  		'gender': 'gender of actor'
  	}
}
```

<h4 id="postMovie"></h4>

> **POST '/movies'**

This endpoint allows you to POST a new movie.

**Request Arguments:**

A JSON object containing the title and the release date:

```javascript
{
	'title': 'movie title',
	'realease_date': '2020-01-01'
}
```

**Returns:** An object with a success message, and the newly posted movie in JSON format.

```javascript
{
	'success': True,
	'movies': {
		'id': 'movie id', 
		'title': 'movie title',
  		'realease_date': '2020-01-01'
  	}
}
```

<h4 id="patchMovie"></h4>

> **PATCH '/movies/"id"'**

This endpoint allows you to PATCH an existing movie with the `id`.

**Request Arguments:**

- _id_ (integer) of the movie to delete.
- A JSON object containing the title and the release date:

```javascript
{
	'title': 'movie title',
	'realease_date': '2020-01-01'
}
```

**Returns:** An object with a success message, and the patched movie in JSON format.

```javascript
{
	'success': True,
	'movies': {
		'id': 'movie id', 
		'title': 'movie title',
  		'realease_date': '2020-01-01'
  	}
}
```

<h4 id="deleteMovie"></h4>

> **DELETE '/movies/"id"'**

This endpoint allows you to delete a movie, based on its id.

**Request Arguments:**

- _id_ (integer) of the movie to delete.

**Returns:** An object with a success message, the `id` of the movie deleted.

```javascript
{
  'success': True,
  'delete': str(delete_id)
}
```

## Testing

To run the tests, run

```
python test_app.py
```

# Available Roles

There are 2 roles and 6 different permissions defined in the Authorization backend for this application

## Permissions:

    ```
    'get:movies': Get the list of all movies
    'get:actors': Get the list of all actors
    'post:movies': Post a new movie
    'post:actors': Post a new actor
    'delete:movies': Delete a movie
    'patch:movies': Edit an existing movie
    ```

## Roles

### Casting Assistant

Can get actors and get movies.

### Casting Director

Can do all operations: get movies, get actors, post movies, modify movies and delete movies.
