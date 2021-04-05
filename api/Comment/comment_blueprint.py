from flask import Blueprint, jsonify, request

from models.tweet import Tweet, TweetSchema, tweet_schema, tweets_schema
from models.comment import Comment, CommentSchema, comment_schema, comments_schema

from models.database import db, ma

from flasgger import swag_from

comment_blueprint = Blueprint('comment_blueprint', __name__)


##### comments #####

@ comment_blueprint.route("/comments/")
# @ swag_from('candidates.yaml')
def comments():
    all_comments = Comment.query.all()
    return jsonify(comments_schema.dump(all_comments))


@ comment_blueprint.route("/comments/<int:comment_id>")
# @ swag_from('comment_detail.yaml')
def comment_detail(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return comment_schema.dump(comment)
