# twitter-subreddit-bot

[![Maintainability](https://api.codeclimate.com/v1/badges/7805c1472547daf0f0e1/maintainability)](https://codeclimate.com/github/randykinne/twitter-subreddit-bot/maintainability)
This is a twitter subreddit bot written in [Python](https://www.python.org/). It currently adds all daily posts from a twitter account into a single post to a subreddit thread

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for different purposes. See *Use* section for notes on how to use the bot.

### Prerequisites
You will need to have [Python 3.6+](https://www.python.org/downloads/), [PRAW](https://praw.readthedocs.io/en/latest/getting_started/installation.html), and [python-twitter](https://python-twitter.readthedocs.io/en/latest/installation.html)

***If you've just installed Python3, pip3 will be included but might not be up-to-date. Update it by running the command:

```
python3 -m pip install --upgrade pip
```

pip3 will now be updated to version 18.1.

For more information or more help on using pip3, reference [Using pip3 to install Python modules].(https://help.dreamhost.com/hc/en-us/articles/115000699011-Using-pip3-to-install-Python3-modules)

Now install the necessary modules individually (manually) or all at once with the following commands:

*Easy Method*
```
pip3 install -r requirements.txt
```
*Manual/Individual Method*
```
pip3 install praw
```
```
pip3 install python-twitter
```

### Installing
Clone or download the respository.

## Config
Change the config to fit your needs.

| Parameter            | Type|                Description                           |        Default value             |
|:--------------------:|:---:|:----------------------------------------------------:|:--------------------------------:|
| client_id            | str | Your reddit client id                                | X    |
| client_secret        | str | Your reddit client secret                            | X    |
| password             | str | Your reddit account password                         | X    |
| username             | str | Your reddit account username                         | X    |
| access_key           | str | Your twitter access key                              | X    |
| access_secret        | str | Your twitter access secret                           | X    |
| consumer_key         | str | Your twitter consumer key                            | X    |
| consumer_secret      | str | Your twitter consumer secret                         | X    |
| author_name          | str | Author of the reddit thread to comment on            | name |
| confirm_actions      | boo | Boolean value of whether to confirm the bot's actions before they happen | True |
| message_prefix       | str | Prefix to attach to the twitter updates the bot posts| message_prefix |
| message_replace      | [str] | Replace text in the tweets. Useful for repetitive hashtags. Can only replace one word with another single word.| ["word", "replaceWith"] |
| message_suffix       | [str] | Suffix to attach to the twitter updates the bot posts on Reddit.| ["suffix_1", "suffix_2"] |
| subreddit_name       | str | Name of subreddit to search for posts                | subreddit |
| subreddit_sort_by    | int | 0 for hot, 1 for new, 2 for top                      | 0  |
| testing              | boo | When enabled, testing prevents the bot from actually posting to Reddit| True | 
| twitter_count        | int | Number of tweets to get from Twitter. Max limit of time is 30 regardless of the number of tweets getting | 15   |
| twitter_name         | str | Username of twitter account to pull tweets from      | twitter_name |
| verbose              | boo | Boolean value of whether to print updates to console. Recommended: True| True |

## Use
In Terminal or Command Prompt, run the following command in the directory of the repo:

```
python3 bot.py
```

If the config.json file doesn't exist yet, it will be generated. 

Replace each 'x' with the correct values to log into Reddit and Twitter. Adjust the rest of the config to suit needs. For reference, see 'Config' section above. Once done, run the *python3 bot.py* command again. If everything was installed correctly, the program should state the found Reddit thread, as well as list all of the tweets found, and then post the tweets found to the reddit thread.

This command/program will need to be ran again each time it is used.

## Contributing
Feel free to contribute. When submitting pull requests, document changes made and why. If the changes heavily alter the program itself, fork if you wish to publish your changes publicly.

## Examples
[u/DRWProspectBot](https://reddit.com/u/DRWProspectBot)

## Authors
* **Randy Kinne** - *Creator* - [GitHub](https://github.com/randykinne)
* **Evan Lock** - *Contributor* - [GitHub](https://github.com/elock37)

## License
Licensed under the [GNU General Public License v3.0](LICENSE).
