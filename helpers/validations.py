import re


def validate_tweeter_username(username):

    # username length must be between 5 and 15 characters.
    if len(username) <= 4 or len(username) >= 15:
        return False

    # username can contain only letters, numbers, and underscores—no spaces are allowed.
    pattern = "^[a-zA-Z0-9_]*$"

    return bool(re.match(pattern, username))


def validate_tweeter_tweet_id(tweet_id):
    # tweet id is numeric only
    return tweet_id.isnumeric()
