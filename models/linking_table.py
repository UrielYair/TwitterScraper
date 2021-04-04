from models.database import db

tweet_comments = db.Table(
    'tweet_comments',
    db.Column('tweet_id', db.Integer,
              db.ForeignKey('tweet.tweet_id')),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.comment_id'))
)
