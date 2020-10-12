#! /usr/bin/env python

from datetime import datetime
import json
import time
import base64

import praw
import twitter


def post(event, context) -> None:
        # event is populated by data from cloud pub/sub message
        # in this case, the data is the config ()
    try:
        config = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    except Exception as ex:
        print(
            "An error occured while attempting to read the config. Exception: " +
            repr(ex)
        )

    subreddit_name = config["Reddit"]["subreddit"]
    sort_by = config["Reddit"]["sort_by"]
    author_name = config["Reddit"]["author"]
    twitter_name = config["Twitter"]["name"]
    twitter_count = config["Twitter"]["tweet_count"]
    message_prefix = config["message_prefix"]
    message_suffix = config["message_suffix"]
    message_replace = config["message_replace"]
    testing = config["testing"]

    reddit = praw.Reddit(
        user_agent=config["Reddit"]["auth"]["username"],
        client_id=config["Reddit"]["auth"]["client_id"],
        client_secret=config["Reddit"]["auth"]["client_secret"],
        username=config["Reddit"]["auth"]["username"],
        password=config["Reddit"]["auth"]["password"],
    )

    twitterApi = twitter.Api(
        consumer_key=config["Twitter"]["auth"]["consumer_key"],
        consumer_secret=config["Twitter"]["auth"]["consumer_secret"],
        access_token_key=config["Twitter"]["auth"]["access_key"],
        access_token_secret=config["Twitter"]["auth"]["access_secret"],
        tweet_mode="extended",
    )

    subreddit = reddit.subreddit(subreddit_name)
    # Refactor number to something more descriptive
    posts = subreddit.hot(limit=1)
    if sort_by == 0:
        posts = subreddit.hot(limit=5)
    elif sort_by == 1:
        posts = subreddit.new(limit=5)
    elif sort_by == 2:
        posts = subreddit.top(limit=5)
    else:
        print("Invalid config! Please change subreddit_sort_by to 0, 1, or 2")

    # Of all the posts on the subreddit, we need to find the daily thread
    submission = ""
    for post in posts:
        if post.author == author_name:
            submission = post
            print("Found post titled: " + post.title)

    if submission.author != author_name:
        print("Submission author not found. Edit the config and try again.")
        exit()

    updates = twitterApi.GetUserTimeline(
        screen_name=twitter_name, count=twitter_count)

    message = message_prefix + "\n\n"

    print(len(updates) + " tweets found from " + twitter_name)

    # We should probably filter map reduce lambda instead for extra coolness
    # think of all the buzzwords!
    for tweet in updates:
        tweet_date = datetime.strptime(
            tweet.created_at, "%a %b %d %H:%M:%S %z %Y")
        if tweet_date.date() == datetime.today().date():
            message = message + (str(tweet.full_text) + "\n\n").replace(
                str(message_replace[0]), str(message_replace[1])
            )

    for i in range(len(message_suffix)):
        message = message + str(message_suffix[i]) + "\n\n"

    if testing:
        print("Since this is just a test, we won't actually post it on Reddit.")
        print(message)
    else:
        try:
            submission_.reply(message)
            print("Message posted on Reddit.")
        except Exception as exception:
            print(
                "There was a problem submitting the message to Reddit."
                "Exception: " + repr(exception)
            )
