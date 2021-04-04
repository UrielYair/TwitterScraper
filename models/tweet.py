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

    comments = db.relationship('Comment', backref='tweet', lazy='dynamic')

    def __repr__(self):
        return '<Tweet %r %r>' % (self.tweet_text, self.comments)


##### SCHEMAS #####

class TweetSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tweet
        fields = ('tweet_id', 'tweet_text',
                  'tweet_username', 'links')  # 'comments',
        include_fk = True

    # comments = ma.List(ma.HyperlinkRelated("tweet_detail"))

    # links = ma.Hyperlinks(
    #     {
    #         "self": ma.URLFor("tweet_blueprint.tweet_detail", values=dict(id="<tweet_id>")),
    #         "collection": ma.URLFor("tweet_blueprint.tweets"),
    #     }
    # )


# Init tweet schemas
tweet_schema = TweetSchema()
tweets_schema = TweetSchema(many=True)
