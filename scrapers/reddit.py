from pathlib import Path
import argparse
import requests

# cant use praw
# use pushshift
#

def main(args):
  r = requests.get('https://api.pushshift.io/reddit/submission/search/?after={}&before={}&sort_type=created_utc&sort=desc&subreddit={}'.format(args.start, args.end, args.subreddit))
  data = r.json()
  print(data['data'])

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Download post titles for a subreddit')
  parser.add_argument('subreddit', type=str,
                      help='Subreddit to crawl')
  parser.add_argument('start', type=str,
                      help='Start time for submissions (unix timestamp)')
  parser.add_argument('end', type=str,
                      help='End time for submissions (unix timestamp)')
  args = parser.parse_args()
  main(args)
