import datetime

from TwitterAPI import TwitterAPI

import Settings


# Messages container for stroring global tweet-data
class Messages:
    # Sets the attributes.
    def __init__(self):
        self.normaltweets = [0]
        self.storingtweets = [0]
        self.storingen = 0
        self.toeslagentweets = [0]
        self.toeslagen = 0
        self.total = 0
        self.lid = ''


# Convert tweet to a message object.
class Message:
    # Convert JSON to a message object
    def __init__(self, item):
        self.text = item['text']
        self.storing = storing(self.text)
        self.toeslagen = toeslagen(self.text)
        self.idn = item["id"]


# Test tweet for any occurrence of a certain (sub)string
def storing(item):
    if "storing" in item.lower():
        return True
    else:
        return False

# Test tweet for any occurrence of a certain (sub)string
def toeslagen(item):
    if "toeslagen" in item.lower():
        return True
    else:
        return False


# Retrieve tweets with the TwitterAPI
def get_tweets():
    # Create an empty message container.
    tweet_container = Messages()

    # Today (Set date and time for twitter).
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # Create a TwitterAPI object, Auth1 is preferred.
    api = TwitterAPI(Settings.consumer_key, Settings.consumer_secret, Settings.access_token_key,
                     Settings.access_token_secret, auth_type='oAuth1', )

    # Retrieve the last 100 tweets
    tweets = api.request('search/tweets', {'q': 'to:abnamro', 'count': '100', 'since': today})

    # Fill the message container with the TwitterAPI response.
    tweet_container = tweet_creator(tweets, tweet_container)

    # If total tweets exceeds 100 make a new call to the TwitterAPI with a max_id.
    ext_tweets = tweet_container.total
    i = 0

    while ext_tweets == 100:
        # Get the maximum id from the container (last processed id).
        max_id = tweet_container.lid

        # New call to the TwitterAPI.
        tweets = api.request('search/tweets', {'q': 'to:abnamro', 'count': '100', 'since': today, 'max_id': max_id})

        # Append new data to tweet_container
        tweet_container = tweet_creator(tweets, tweet_container)

        # Extract the iterations for the loop
        i += 1
        ext_tweets = (tweet_container.total - (100 * i))

    # Return the message container
    return tweet_container

# Removes the @ABNAMRO sign from the tweet text
def remove_aab(tweet):

    return tweet.replace('@ABNAMRO', '')


# Fill the tweet_container with content
def tweet_creator(tweets, tweet_container):
    # Create a message object of every tweet
    for tweet in tweets:

        # Validate returned JSON object
        if 'text' in tweet:

            # Get a tweet (message class)
            tweet_message = Message(tweet)

            # Append the tweet to the container.

            # For tweets containing storing.
            if tweet_message.storing:

                # Remove @ABNAMRO and append to the container.
                tweet_container.storingtweets.append(remove_aab(tweet_message.text))

                # Update both total and storing count at container level.
                tweet_container.storingen += 1
                tweet_container.total += 1

            # For tweets containing toeslagen.
            elif tweet_message.toeslagen:

                # Remove @ABNAMRO and append to the container.
                tweet_container.toeslagentweets.append(remove_aab(tweet_message.text))

                # Update both total and toeslagen count at container level.
                tweet_container.toeslagen += 1
                tweet_container.total += 1

            # For every other tweet (normal tweet).
            else:

                # Remove @ABNAMRO and append to the container.
                tweet_container.normaltweets.append(remove_aab(tweet_message.text))

                # Update the total at container level.
                tweet_container.total += 1

            # Set the lid (last id) to the message_id of the oldest tweet.
            tweet_container.lid = tweet_message.idn

        # Not valid, skip the tweet.
        else:
            tweet

    # Return the updated container to the caller.
    return tweet_container
