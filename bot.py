#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# twitter-subreddit-bot v1.1 (12/10/2018) 7:29 PM EST
# A twitter-subreddit bot based on DRWProspectsBot.
#
# by Randy Kinne
# https://github.com/randykinne/

from datetime import datetime
import json
import os.path
import time

import praw
import twitter


def read_config():
	"""Reads a configuration.

	@return     {<Dict>}  ( Returns the configuration as dict )
	"""
	if (os.path.isfile("config.json")):
		# open config file, return the data loaded as json
		with open("config.json", "r") as f:
			data = json.load(f)
			f.close()
			return data
	else:
		# create basic outline for file
		config = {
			"Reddit": {
				"subreddit": "subreddit",
				"sort_by": 0,
				"author": "name",
				"auth": {
					"client_id": "X",
					"client_secret": "X",
					"username": "X",
					"password": "X"
				}
			},
			"Twitter": {
				"name": "twitter_name",
				"tweet_count": "15",
				"auth": {
					"access_key": "X",
					"access_secret": "X",
					"consumer_key": "X",
					"consumer_secret": "X"
				}
			},
			"message_prefix": "message_prefix",
			"message_suffix": ("suffix_1", "suffix_2"),
			"message_replace": ("word", "replaceWith"),
			"verbose": "True",
			"confirm_actions": "True",
			"testing": "True"
		}

		# Create the file, indent=4 and sort_keys=True to add readability.
		with open('config.json', 'w') as secret_info:
			json.dump(config, secret_info, indent=4, sort_keys=True)

		# Tell the user that the config was not found.
		# Exit program.
		log("No configuration found. Please edit config.json and try again.", True)
		exit()


def log(message, verbose):
	"""Log messages to console.

	@param      {<String>}  message  The message to console.
	@param      {<Boolean>}  verbose  Print message to console or not.
	@return     {<None>}  ( None )
	"""
	if (verbose):
		print(message)


def confirm(message):
	"""Confirmation dialogue to console.

	@param      {<String>}  message  The message asked to console
	@return     {<Boolean>}  ( Returns whether the user wants to complete the action )
	"""
	answer = input("Do you want to " + message + "? y/n: ")
	if (answer == "y" or answer == "yes"):
		return True
	elif (answer == "n" or answer == "no"):
		return False
	else:
		log("Invalid answer. Option(s): y/n", True)
		return confirm(message)

#
# @brief      Main function
#
# @return 	   { None }
#


def main():
	"""Main function of the program.

	@return     {<None>}  ( None )
	"""
	# Attempt to get the config, see function readConfig() above.
	try:
		config = read_config()
	except:
		log(
			"An error occured while attempting to read the config. "
			"Please check config values and try again.",
			True
			)

	verbose = config['verbose']
	confirm_actions = config['confirm_actions']
	subreddit_name = config['Reddit']['subreddit']
	sort_by = config['Reddit']['sort_by']
	author_name = config['Reddit']['author']
	twitter_name = config['Twitter']['name']
	twitter_count = config['Twitter']['tweet_count']
	message_prefix = config['message_prefix']
	message_suffix = config['message_suffix']
	message_replace = config['message_replace']

	# Let console know the config data was loaded correctly.
	log("Loaded Json Config Data", verbose)

	# Set praw reddit user info with the info from the config.
	reddit = praw.Reddit(
		user_agent=config['Reddit']['auth']['username'],
		client_id=config['Reddit']['auth']["client_id"],
		client_secret=config['Reddit']['auth']["client_secret"],
		username=config['Reddit']['auth']["username"],
		password=config['Reddit']['auth']["password"]
		)

	# Set python-twitter user info with the info from the config.
	twitterApi = twitter.Api(
		consumer_key=config['Twitter']['auth']['consumer_key'],
		consumer_secret=config['Twitter']['auth']['consumer_secret'],
		access_token_key=config['Twitter']['auth']['access_key'],
		access_token_secret=config['Twitter']['auth']['access_secret'],
		tweet_mode='extended'
		)

	# Set the subreddit name for praw.
	if (confirm_actions):
		if (confirm("set subreddit name to \'" + subreddit_name + "\'")):
			subreddit = reddit.subreddit(subreddit_name)
		else:
			subreddit_name = input("Enter the name of the subreddit: ")
			subreddit = reddit.subreddit(subreddit_name)
	else:
		subreddit = reddit.subreddit(subreddit_name)

	posts = subreddit.hot(limit=1)
	if (sort_by == 0):
		posts = subreddit.hot(limit=5)
	elif (sort_by == 1):
		posts = subreddit.new(limit=5)
	elif (sort_by == 2):
		posts = subreddit.top(limit=5)
	else:
		log("Invalid config! Please change subreddit_sort_by to 0, 1, or 2", True)

	submission_ = ""
	for submission in posts:
		if (submission.author == author_name):
			# Print name of the submission to ensure the name is correct.
			if (confirm_actions):
				if (confirm("set submission title to \'" + submission.title + "\'")):
					submission_ = submission
					log("Found submission titled: " + submission.title, verbose)
				else:
					log("Submission not found", True)
			else:
				submission_ = submission
				log("Found submission titled: " + submission.title, verbose)

	if (submission_.author != author_name):
		log("Submission author not found. Edit the config and try again.", True)
		exit()

	# Get the user timeline from twitter user.
	updates = twitterApi.GetUserTimeline(
		screen_name=twitter_name,
		count=twitter_count
		)

	log("=================== MESSAGE ===================", verbose)

	# Add prefix to message and newline for message readability.
	message = (message_prefix + "\n")

	# Get every update from the twitter user.
	for tweet in updates:
		# Format the date into a format python can recognize.
		tweet_date = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S %z %Y')
		# Check if the date was the same as today.
		# Necessary to ensure that you aren't getting tweets from the past.
		if (tweet_date.date() == datetime.today().date()):
			# Append the tweet to the message while replacing text.
			# Newlines for formatting.
			message = message + (str(tweet.full_text) + "\n\n").replace(
				str(message_replace[0]),
				str(message_replace[1])
				)

	# Add suffix to message.
	for i in range(len(message_suffix)):
		message = message + str(message_suffix[i]) + "\n\n"

	# Print the message to the screen so the user sees the post to Reddit.
	log(message, verbose)
	log("================ END OF MESSAGE =================", verbose)

	# Finally post the message on Reddit if not testing.
	if (config['testing']):
		log("Since this is just a test, we won't actually post it on Reddit.", True)
	else:
		try:
			if (confirm_actions):
				if (confirm("post message on Reddit")):
					submission_.reply(message)
				else:
					log("Message not posted on Reddit.", True)
			else:
				submission_.reply(message)
			log("Message posted on Reddit.", verbose)
		except Exception as exception:
			log(
				"An error occured. There was a problem submitting the message to Reddit."
				"Exception: " + repr(exception),
				True
				)


main()


# End of program.
