[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

# drw-prospect-bot

This is a bot written in [Python](https://www.python.org/). It currently adds all daily posts from a twitter account into a single post to a subreddit thread - specifically, a post about the prospects of the Detroit Red Wings.

## Deployment

The bot is currently deployed as a [Cloud Function](https://developers.google.com/learn/topics/functions) which is subscribed to the `updates` [Cloud Pub/Sub](https://cloud.google.com/pubsub) topic.

The `updates` topic recieves scheduled messages from [Cloud Scheduler](https://cloud.google.com/scheduler). Fancy.

## Config

|     Parameter     | Type  |                                                   Description                                                   |      Default value       |
| :---------------: | :---: | :-------------------------------------------------------------------------------------------------------------: | :----------------------: |
|     client_id     |  str  |                                              Your reddit client id                                              |            X             |
|   client_secret   |  str  |                                            Your reddit client secret                                            |            X             |
|     password      |  str  |                                          Your reddit account password                                           |            X             |
|     username      |  str  |                                          Your reddit account username                                           |            X             |
|    access_key     |  str  |                                             Your twitter access key                                             |            X             |
|   access_secret   |  str  |                                           Your twitter access secret                                            |            X             |
|   consumer_key    |  str  |                                            Your twitter consumer key                                            |            X             |
|  consumer_secret  |  str  |                                          Your twitter consumer secret                                           |            X             |
|    author_name    |  str  |                                    Author of the reddit thread to comment on                                    |           name           |
|  confirm_actions  |  boo  |                    Boolean value of whether to confirm the bot's actions before they happen                     |           True           |
|  message_prefix   |  str  |                              Prefix to attach to the twitter updates the bot posts                              |      message_prefix      |
|  message_replace  | [str] | Replace text in the tweets. Useful for repetitive hashtags. Can only replace one word with another single word. | ["word", "replaceWith"]  |
|  message_suffix   | [str] |                        Suffix to attach to the twitter updates the bot posts on Reddit.                         | ["suffix_1", "suffix_2"] |
|  subreddit_name   |  str  |                                      Name of subreddit to search for posts                                      |        subreddit         |
| subreddit_sort_by |  int  |                                         0 for hot, 1 for new, 2 for top                                         |            0             |
|      testing      |  boo  |                     When enabled, testing prevents the bot from actually posting to Reddit                      |           True           |
|   twitter_count   |  int  |    Number of tweets to get from Twitter. Max limit of time is 30 regardless of the number of tweets getting     |            15            |
|   twitter_name    |  str  |                                 Username of twitter account to pull tweets from                                 |       twitter_name       |
|      verbose      |  boo  |                     Boolean value of whether to print updates to console. Recommended: True                     |           True           |

## Contributors

- **Randy Kinne** - _Creator_ - [GitHub](https://github.com/randykinne)
- **Evan Lock** - _Contributor_ - [GitHub](https://github.com/elock37)

## License

Licensed under the [GNU General Public License v3.0](LICENSE).
