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
# @ swag_from('candidates.yaml')
def tweets():
    all_tweets = Tweet.query.all()
    return jsonify(tweets_schema.dump(all_tweets))


@ tweet_blueprint.route("/tweets/<int:id>")
# @ swag_from('candidate_detail.yaml')
def tweet_detail(id):
    tweet = Tweet.query.get_or_404(id)
    return tweet_schema.dump(tweet)


@ tweet_blueprint.route("/tweets/store/<string:username>/<string:tweet_id>")
# @ swag_from('tweet_detail.yaml')
def store_tweet_with_replies(username, tweet_id):

    if not validate_tweeter_username(username) or not validate_tweeter_tweet_id(tweet_id):
        return {'error': "username or tweet id is not in the corrrect format."}

    url = f'{TWITTER_BASE_URL}{username}/status/{tweet_id}'
    # tweet_text = fetch_post_text(url)
    # tweet_replies = fetch_post_replies(url)

    tweet_text = {'post_found': True, 'tweet_text': 'כל פעם שגורם ממסדי כלשהו אומר משהו שלא מתאים לליכודניקים הם מתחילים להשתולל ולאיים בחורבן.\nפעם זה בג"צ ופעם זה הנשיא.\n\nלא מתאים לכם מדינת חוק דמוקרטית עם איזונים ובלמים תתכבדו ותקימו לכם את מונרכיית יהודה ותעזבו אותנו בשקט.'}
    tweet_replies = {'post_found': True, 'tweet_replies': {'ומי יממן אותם?',
                                                           'יותר מונרכית ביביסטן.\nיהודה זה שלנו.', 'מדוייק\nביביסטים נמאסתם\n@Likud_Party'}}

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
