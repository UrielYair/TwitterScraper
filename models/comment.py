from models.database import db, ma
from models.tweet import TweetSchema
from constants.constants_variables import TWEET_REPLY_TEXT_LENGTH
##### MODELS #####


class Comment(db.Model):
    # __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(
        db.String(TWEET_REPLY_TEXT_LENGTH), nullable=False)
    tweet_id = db.Column(db.Integer, db.ForeignKey(
        "tweet.tweet_id"), nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.comment_text


##### SCHEMAS #####

class CommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Comment
        fields = ('comment_id', 'comment_text', 'tweet_id', 'comments')
        include_fk = True

    comments = ma.Nested(TweetSchema, many=True)


# Init comment schemas
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
