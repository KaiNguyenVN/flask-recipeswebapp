# Recipe Portal


## Description

Recipe Web App
A Flask-based web application that allows users to browse, view, and review recipes.
It features user authentication, recipe details, and review management, with a modular structure using Blueprints and an SQLAlchemy database backend.

### Key Features

1. Built with Flask and Jinja2 templating

2. User authentication (login, registration, and session management)

3. Recipe browsing and detail pages with user reviews

4. WTForms for secure form handling (with CSRF protection)

5. Uses SQLAlchemy ORM for database integration

6. Simple, responsive HTML/CSS interface

## Installation

**Installation via requirements.txt**

**Windows**
```shell
$ cd <project directory>
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

**MacOS**
```shell
$ cd <project directory>
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File or PyCharm'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add Interpreter'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *project directory*, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Testing

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right-clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call 'python -m pytest tests' to run all the tests. PyCharm also provides a built-in terminal, which uses the configured virtual environment. 

## Configuration

The *project directory/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

## what we have done
* Create domainmodels.
* Create a csv file reader.
* Did unit test for domainmodels.
* Create a memory_repository to store the recipe data.
* Create a Home page for our Web app.
* Create a Browse page to display all the recipes.
* Create a Detail page to display recipe detail.
* Did unit test for the service layer and memory_repository.
 
## Data sources

The data files are modified excerpts downloaded from:

https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews/

## About health star rating calculation
First: Baseline points (negative).

    These penalized high amounts of saturated fat, sugar, and sodium.
    Higher value of these "bad" nutrients increase baseline, which reduces the health score. 

    Saturated fat (per 100g/ml):
    ≤1 → 0 points
    ≤3 → 1 point
    ≤5 → 2 points
    5 → 3 points

    Sugar (per 100g/ml):
    ≤5 → 0 points
    ≤10 → 1 point
    ≤15 → 2 points
    15 → 3 points

    Sodium (per 100g/ml):
    ≤120 → 0 points
    ≤200 → 1 point
    ≤400 → 2 points
    400 → 3 points

Second: Modifying points (positive).

    These give credit for “good” nutrients fiber and protein.
    Higher values of these "good" nutrients incresed modifying points, 
    which increases the health score

    Fiber:
    ≥4 → +1
    ≥8 → +1 extra

    Protein:
    ≥5 → +1
    ≥10 → +1 extra

Third: Calculate final score

    score = 5 - baseline + modifying

    Then clamp the score between 0.5 and 5, and round to the nearest 0.5 stars

We're trying to follow the Australia/New Zealand HSR but we simplify it 
because the real system is more complex and need to consider a lot of things.
So here, we only take into account the amount of saturated fat, sugar, sodium, fiber and protein.



