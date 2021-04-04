from models.database import db, ma
from constants.constants_variables import TWEET_TEXT_LENGTH, TWITTER_USERNAME_LENGTH
##### MODELS #####


class Tweet(db.Model):
    # __tablename__ = 'tweets'
    tweet_id = db.Column(db.Integer, primary_key=True)
    tweet_text = db.Column(db.String(TWEET_TEXT_LENGTH),
                           unique=True, nullable=False)
    tweet_username = db.Column(
        db.String(TWITTER_USERNAME_LENGTH), nullable=False)

    def __repr__(self):
        return '<Tweet %r %r>' % (self.tweet_text, self.comments)


##### SCHEMAS #####

class TweetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tweet
        include_fk = True
        # fields = ('tweet_id', 'tweet_text', 'tweet_username', 'comments')
    # working: # comments = ma.List(ma.HyperlinkRelated("tweet_blueprint.tweet_detail"))


# Init tweet schemas
tweet_schema = TweetSchema()
tweets_schema = TweetSchema(many=True)


def tweet_as_dict(sqlalchemy_tweet):
    pass
