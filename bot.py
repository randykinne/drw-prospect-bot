## 
## twitter-subreddit-bot v1.0 (12/7/2018) 4:07 PM EST
## A twitter-subreddit bot based on DRWProspectsBot
## 
## by Randy Kinne
##
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
			"Reddit": {
				"subreddit": "subreddit",
				"sort_by": "0",
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
	answer = input("Do you want to " + message + "? y/n: ")
	if (answer == "y" or answer == "yes"):
		return True
	elif (answer == "n" or answer == "no"):
		return False
	else:
		log("Invalid answer. Option(s): y/n", True)
		return confirm(message)
##
## @brief      Main function
## 
## @return 	   { None }
##
def main():
	# Attempt to get the config, see function readConfig() above
	try:
		config = readConfig()
	except:
		log("An error occured while attempting to read the config. Please check config values and try again.")

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
	testing = config['testing']

	# verbose messages for user
	log("Loaded Json Config Data", verbose)

	# set praw reddit user info with the info from the config
	reddit = praw.Reddit(user_agent=config['Reddit']['auth']['username'],
			client_id=config['Reddit']['auth']["client_id"],
			client_secret=config['Reddit']['auth']["client_secret"],
			username=config['Reddit']['auth']["username"],
			password=config['Reddit']['auth']["password"])

	# set python-twitter user info with the info from the config
	twitterApi = twitter.Api(consumer_key=config['Twitter']['auth']['consumer_key'],
		consumer_secret=config['Twitter']['auth']['consumer_secret'],
		access_token_key=config['Twitter']['auth']['access_key'],
		access_token_secret=config['Twitter']['auth']['access_secret'],
		tweet_mode='extended')

	# set the subreddit name for praw
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

	subm = ""
	for submission in posts:
		if (submission.author == author_name):
			# print name of the submission to ensure the name is correct
			if (confirm_actions):
				if (confirm("set submission title to \'" + submission.title + "\'")):
					subm = submission
					log("Found submission titled: " + submission.title, verbose)
				else: log("Submission not found", True)
			else:
				subm = submission
				log("Found submission titled: " + submission.title, verbose)


	if (subm.author != author_name):
		log("Submission author not found. Edit the config and try again.", True)
		exit()

	# get the user timeline from twitter user
	updates = twitterApi.GetUserTimeline(screen_name=twitter_name, count=twitter_count)

	log("=================== MESSAGE ===================", verbose)

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
			message = message + (str(x.full_text) + "\n\n").replace(str(message_replace[0]), str(message_replace[1]))

	# after all tweets have been added to message, add this to bottom of message posted to reddit so users have more information about this project as well as the data source
	for i in range(len(message_suffix)):
		message = message + str(message_suffix[i]) + "\n\n"

	# print the message to the screen so the user sees what will be posted on Reddit
	log(message, verbose)
	log("================ END OF MESSAGE =================", verbose)

	# finally post the message on Reddit if not testing
	if (config['testing']):
		log("Since this is just a test, we won't actually post it on Reddit.", True)
	else:
		try:
			if (confirm_actions): 
				if (confirm("post message on Reddit")):
					subm.reply(message)
				else: log("Message not posted on Reddit.", True)
			else:
				subm.reply(message)
			
			log("Message posted on Reddit.", verbose)
		except:
			log("An error occured. There was a problem submitting the message to Reddit.", True)
	
# this is necessary, I once forgot this and nothing happened when I ran the program, spent several hours figuring out why
# pretty self explanatory though
main()

##
## eop
##
