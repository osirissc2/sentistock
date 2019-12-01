from dotenv import load_dotenv
from pathlib import Path
import tweepy
import argparse
import os
import csv

def main(args):
  load_dotenv()
  auth = tweepy.OAuthHandler(os.getenv("TWITTER_CONSUMER_KEY"), os.getenv("TWITTER_CONSUMER_SECRET"))
  auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))

  api = tweepy.API(auth)
  user = api.get_user(args.username)
  print('=> Total tweets for @{}: {}'.format(args.username, user.statuses_count))

  tweets = []
  recent_tweets = api.user_timeline(screen_name=args.username, count=200)
  tweets.extend(recent_tweets)

  oldest = tweets[-1].id - 1
  while len(recent_tweets) > 0:
    print('=> Downloading tweets before ID {}...'.format(oldest))
    recent_tweets = api.user_timeline(screen_name=args.username, count=200, max_id=oldest)
    tweets.extend(recent_tweets)
    oldest = tweets[-1].id - 1
    print('=> {} tweets downloaded so far'.format(len(tweets)))

  csv_content = [[tweet.id_str, tweet.created_at, tweet.text.encode()] for tweet in tweets]
  csv_path = Path(Path.cwd(), 'data/tweets/{}.csv'.format(args.username))
  with open(csv_path, 'w', newline='\n', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["id","created_at","text"])
    writer.writerows(csv_content)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Download tweets for a user')
  parser.add_argument('username', type=str,
                      help='Username to crawl')
  parser.add_argument('--start', type=str,
                    help='Start time for interval')
  parser.add_argument('--end', type=str,
                    help='End time for interval')
  args = parser.parse_args()
  main(args)
