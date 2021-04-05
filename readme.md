# Twitter Scraper using Selenium

instructions:
open up the terminal.

    git clone https://github.com/UrielYair/TwitterScraper.git
    cd TwitterScraper
    pip install -r requirement.txt

database creation/deletion - database already created - but if needed:
in terminal:

    python3
    from app import create_app
    from models.database import db
    db.create_all(app=create_app()) # in order to set up new database
    db.drop_all(app=create_app()) # in order to delete existing database
    exit()

## start server:

#### Option A:

in terminal:

    FLASK_APP=app.py
    flask run

#### Option B:

in terminal:

    python app.py

After running the server, open your browser and navigate to:
[Swagger Documentation](http://127.0.0.1:5000/apidocs/)

TECH Stack:

Python, flask, SQLAlchemy, SQLite, Marshmellow, flassger(swagger), Selenium WebDriver

Full list of endpoints are written in swagger documentation:
http://127.0.0.1:5000/apidocs/

feel free to use your favorite way of submitting http request:

-   cURL
-   postman
-   swagger UI

![alt text](https://github.com/UrielYair/HR-REST-API/blob/master/swagger_apidocs.png?raw=true)
