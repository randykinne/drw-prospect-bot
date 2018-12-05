## 
## twitter-subreddit-bot v1 (12/5/2018)
## A twitter-subreddit bot based on DRWProspectsBot
## 
## by Randy Kinne
##
## TODO: format config default better
## TODO: add verbose setting in config, then read to determine verbosity
## TODO: add confirmation setting in config, then read to determine whether a confirmation for bot actions is necessary
## TODO: Reformat the printed messages to user

import praw
import time
import json
import os.path
import twitter
from datetime import datetime

##
## @brief      Reads a configuration.
##
## @return     { Returns the config file }
##
def readConfig():

	# if 'config.json' file exists in same path as this file, open it
	if (os.path.isfile('config.json')):

		# open config file, return the data loaded as json
		with open('config.json', 'r') as f:
			data = json.load(f)
			f.close()

			return data

	# if 'config.json' file does not exist
	else:

		# create basic outline for file 
		# need to format this better, it's a mess
		config = {
		"Reddit": [{"client_id": "X", 
		"client_secret": "X", 
		"username": "X", 
		"password": "X" }], 

		"Twitter": [{"access_key": "X", 
		"access_secret": "X", 
		"consumer_key": "X", 
		"consumer_secret": "X"}],

		"subreddit_name": "subreddit_name_to_post_to",
		"subreddit_sort_by": "0_for_hot_1_for_new_2_for_top",
		"author_name": "name",

		"twitter_name": "twitter_account_to_get_tweets_from",
		"twitter_count": "15",

		"message_prefix": "message_prefix_one_line",
		"message_suffix": [{"suffix_1", "suffix_2"}],
		"message_replace": [{"word", "replaceWith"}],

		"verbose": "True",
		"confirm_actions": "True"
		}

		# create the file, indent=4 and sort_keys=True to add readability to the json file
		with open('config.json', 'w') as secret_info:
			json.dump(config, secret_info, indent=4, sort_keys=True)

		# return the default config which will attempt to log in, it won't work and it'll let the user know 
		return config
	
##
## @brief      Log messages to console
##
## @param      message  str The message to be posted to console
## @param      verbose  bool Whether messages are to be broadcasted to console
## @return     { None }
##
def log(message, verbose):
	if (verbose):
		print(message)

##
## @brief      Confirmation dialoge to user
##
## @param      message  The message asked to the user
##
## @return     { Returns whether the user wants to complete the action or not }
##
def confirm(message):
	answer = input("Do you want to " + message + "? y/n")
	if (answer == "y" or answer == "yes"):
		return True
	elif (answer == "n" or answer == "no"):
		return False
	else:
		print("Invalid answer. Option(s): y/n")
		return confirm(message)
##
## @brief      Main function
## 
## @return 	   { None }
##
def main():

	# Attempt to get the config, see function readConfig() above
	config = readConfig()

	verbose = config['verbose']
	confirm = config['confirm']
	subreddit_name = config['subreddit_name']
	subreddit_sort = config['subreddit_sort_by']
	author_name = config['author_name']
	twitter_name = config['twitter_name']
	twitter_count = config['twitter_count']
	message_prefix = config['message_prefix']
	message_suffix = config['message_suffix']
	message_replace = config['message_replace']


	# verbose messages for user
	log("Loaded Json Config Data", verbose)

	# declare redditInfo to make it easier to get info from the config
	redditInfo = config['Reddit'][0]

	# set praw reddit user info with the info from the config
	reddit = praw.Reddit(user_agent=redditInfo['username'],
			client_id=redditInfo["client_id"],
			client_secret=redditInfo["client_secret"],
			username=redditInfo["username"],
			password=redditInfo["password"])

	# declare twitterInfo to make it easier to get info from the config
	twitterInfo = config['Twitter'][0]

	# set python-twitter user info with the info from the config
	twitterApi = twitter.Api(consumer_key=twitterInfo['consumer_key'],
		consumer_secret=twitterInfo['consumer_secret'],
		access_token_key=twitterInfo['access_key'],
		access_token_secret=twitterInfo['access_secret'],
		tweet_mode='extended')

	# set the subreddit name for praw
	subreddit = reddit.subreddit(subreddit_name)

	# finds the daily reddit post by OctoMod (bot). It's always the 2nd post sorted by hot
	for submission in subreddit.hot(limit=2):
		if (submission.author == author_name):
			# print name of the submission to ensure the name is correct

	 		log("Found submission titled: " + submission.title, verbose)

	# get the user timeline from twitter user 'DRWProspects', they wouldn't post more than 15 in a single day 
	updates = twitterApi.GetUserTimeline(screen_name=twitter_name, count=twitter_count)

	# preface message with yesterday's results so users know which day the scores happened on, then newline for formatting
	message = (message_prefix + "\n")

	# get every update from the twitter user
	for x in updates:
		# format the date into a format python can recognize
		d = datetime.strptime(x.created_at,'%a %b %d %H:%M:%S %z %Y');
		# check if the date was the same as today, necessary to ensure that you aren't getting tweets from the past
		if (d.date() == datetime.today().date()):
			# append the tweet to the message while replacing #RedWings with a space
			# the twitter user adds #RedWings to the end of every tweet, could get redundant or annoying
			# newlines for formatting
			message = message + (str(x.full_text) + "\n\n").replace(message_replace[0], message_replace[1])

	# after all tweets have been added to message, add this to bottom of message posted to reddit so users have more information about this project as well as the data source
	for i in message_suffix:
		message = message + message_suffix[i]

	# print the message to the screen so the user sees what will be posted on Reddit
	log(message, verbose)

	# finally post the message on Reddit
	#//submission.reply(message)

	# confirmation dialog
	#//log("Message posted on Reddit.")
	
# this is necessary, I once forgot this and nothing happened when I ran the program, spent several hours figuring out why
# pretty self explanatory though
main()


##
## eop
##
