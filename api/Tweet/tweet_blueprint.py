from flask import Blueprint, jsonify, request

from models.tweet import Tweet, TweetSchema, tweet_schema, tweets_schema
from models.comment import Comment, CommentSchema, comment_schema, comments_schema

from models.database import db, ma
from flasgger import swag_from
from helpers.scraper.scrape import fetch_post_replies, fetch_post_text
from constants.constants_variables import TWITTER_BASE_URL
from helpers.validations import validate_tweeter_tweet_id, validate_tweeter_username

from pprint import pprint

tweet_blueprint = Blueprint('tweet_blueprint', __name__)

##### tweets #####


@ tweet_blueprint.route("/tweets/")
@ swag_from('tweets.yaml')
def tweets():
    all_tweets = Tweet.query.all()
    return jsonify(tweets_schema.dump(all_tweets))


@ tweet_blueprint.route("/tweets/<int:id>")
@ swag_from('tweet_detail.yaml')
def tweet_detail(id):
    tweet = Tweet.query.get_or_404(id)
    return tweet_schema.dump(tweet)


@ tweet_blueprint.route("/tweets/<int:tweet_id>/comments/")
@ swag_from('tweet_comments.yaml')
def get_comments_by_tweet_id_from_db(tweet_id):
    tweet = Tweet.query.get_or_404(tweet_id)
    return jsonify(comments_schema.dump(tweet.comments))


@ tweet_blueprint.route("/tweets/store/<string:username>/<string:tweet_id>")
@ swag_from('tweet_scrape.yaml')
def store_tweet_with_replies(username, tweet_id):

    # Find tweet in DB:
    tweet = Tweet.query.filter_by(tweet_id=tweet_id).first()

    # check if tweet already in DB:
    exists = tweet is not None
    if exists:
        return tweet_schema.dump(tweet)

    if not validate_tweeter_username(username) or not validate_tweeter_tweet_id(tweet_id):
        return {'error': "username or tweet id is not in the corrrect format."}

    url = f'{TWITTER_BASE_URL}{username}/status/{tweet_id}'
    tweet_text = fetch_post_text(url)
    tweet_replies = fetch_post_replies(url)

    if not tweet_text['post_found']:
        return tweet_text

    if not tweet_replies['post_found']:
        return tweet_replies

    # print(tweet_text)
    # pprint(tweet_replies['tweet_replies'])

    new_tweet = Tweet(
        tweet_id=tweet_id, tweet_text=tweet_text['tweet_text'], tweet_username=username)

    for comment in tweet_replies['tweet_replies']:

        # Create new comment row in DB
        new_comment = Comment(comment_text=comment, tweet_id=tweet_id)
        db.session.add(new_comment)

        # add comment to new_tweet
        new_tweet.comments.append(new_comment)

    db.session.add(new_tweet)
    db.session.commit()

    return tweet_schema.dump(new_tweet)
