# Full Stack Trivia API Backend

## Introduction
This project is part of the Full-Stack Nanodegree which is presented by Udacity.
The main idea behind this project is to provide a Trivia API, which allows the user to play a quiz that consists of a question from many categories.
It also allows the users to create, and delete questions.

## Getting Started
- Base URL:  `http://127.0.0.1:5000/`.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
  "error": 404,
  "message": "Not found",
  "success": false
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Not Found
- 422: Unprocessable Entity
- 500: Internal Server Error

## Endpoints

- ### GET /categories
    - General:
        - Returns an object that contains available categories.
    - Sample: `curl GET http://127.0.0.1:5000/categories`
    ```

    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        }
    }

    ```
- ### GET /questions
    - General:
        - Returns an object that contains available categories, current category, list of questions, and total number of available questions
        - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
    - Sample: `curl GET http://127.0.0.1:5000/questions`

    ```

    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "current_category": {
            "1": "Science"
        },
        "questions": [
            {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
            },
            {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            },
            {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            },
            {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
            },
            {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
            },
            {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
            },
            {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
            },
            {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
            },
            {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
            }
        ],
        "total_questions": 18
    }

    ```
- ### DELETE /questions/<question_id>
    - General:
        - Deletes a Question using the Question ID provided in the URL.
    - Sample: `curl DELETE http://127.0.0.1:5000/questions/1`

    ```

    {
        "message": "Question Deleted"
    }

    ```
- ### POST /questions
    - General:
        - Creates a Question, the user needs to provide an object that contains the question, the answer, category, and difficulty.
    - Sample: `curl -d '{"question": "TEST Question","answer": "TEST Answer","difficulty": 3,"category": 4}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/questions`


    ```

    {
        "message": "Question Created"
    }

    ```

- ### POST /questions/search
    - General:
        - Returns a list of questions that contains the search term provided in the request, total number of questions found in the result, and the current category.
    - Sample: `curl -d '{"searchTerm": "title"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/questions/search`


    ```

    {
        "currentCategory": {
            "3": "Geography"
        },
        "questions": [
            {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            }
        ],
        "totalQuestions": 2
    }

    ```

- ### GET /categories/<category_id>/questions
    - General:
        - Returns a list of questions that are in the same category provided in the request, total number of questions found in the result, and the current category.
    - Sample: `curl GET 'http://127.0.0.1:5000/categories/4/questions'`

    ```

    {
        "currentCategory": "History",
        "questions": [
            {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
            },
            {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
            },
            {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
            },
            {
            "answer": "TEST Answer",
            "category": 4,
            "difficulty": 3,
            "id": 35,
            "question": "TEST Question"
            }
        ],
        "totalQuestions": 5
    }
    ```

- ### POST /quizzes
    - General:
        - takes a list of previous questions, and a category as a request, and returns a random question that hasn't been in the previous questions list and of the same category provided in the request.
    - Sample: `curl -d '{"previous_questions": [],"quiz_category": {"type": "History","id": 4}}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/quizzes`

    ```
    {
        "question": {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        }
    }
    ```