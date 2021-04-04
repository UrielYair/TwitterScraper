from flask import Flask
from flasgger import Swagger

from api.Comment.comment_blueprint import *
from api.Tweet.tweet_blueprint import *


def create_app():
    app = Flask(__name__)

    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitter_alternative.sqlite.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # SQLAlchemy and Marshmallow
    from models.database import db, ma

    # SQLAlchemy and Marshmallow initiation:
    db.init_app(app)
    ma.init_app(app)

    ##### API #####
    # Blueprints registration
    app.register_blueprint(comment_blueprint, url_prefix="/api")
    app.register_blueprint(tweet_blueprint, url_prefix="/api")

    #######################################
    from flasgger import APISpec, Schema, Swagger, fields
    from apispec.ext.marshmallow import MarshmallowPlugin
    from apispec_webframeworks.flask import FlaskPlugin

    # Create an APISpec
    spec = APISpec(
        title='Twitter Alternative',
        version='1.0',
        openapi_version='2.0',
        plugins=[FlaskPlugin(), MarshmallowPlugin()]
    )

    from models.tweet import TweetSchema
    from models.comment import CommentSchema

    template = spec.to_flasgger(
        app,
        definitions=[TweetSchema, CommentSchema],
    )

    # set the UIVERSION to 3
    app.config['SWAGGER'] = {'uiversion': 3}

    # start Flasgger using a template from apispec
    swag = Swagger(app, template=template)
    #######################################

    return app


##### Main #####
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
