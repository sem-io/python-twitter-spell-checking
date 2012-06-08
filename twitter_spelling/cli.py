# -*- coding: utf-8 -*-

from datetime import datetime
import sys
import argparse
import os
import json
import ConfigParser

import twitter
from utils import clean, is_valid
from collections import defaultdict

# Lambda function which tranforms a ConfigParser items
# list of tuples object into a dictionnary
items_to_dict = lambda items : {k:v for k,v in items}


def fetch(args):
    print 'Welcome to Twitter Spell Checking : Fetching !'
    CONFIG = ConfigParser.ConfigParser()
    CONFIG.read(args.config)

    settings = items_to_dict(CONFIG.items('twitter'))
    config = items_to_dict(CONFIG.items('namespace:%s' % args.namespace))
    api = twitter.Api(consumer_key=settings['consumer_key'], consumer_secret=settings['consumer_secret'], access_token_key=settings['access_token'], access_token_secret=settings['access_token_secret'])

    accounts = [account.replace(' ', '') for account in config['accounts'].split(',')]
    max_tweets_file = os.path.join(os.path.dirname(config['files']), 'max_tweets_%s.txt' % args.namespace)

    def save_max_tweets():
        open(max_tweets_file, 'w').write(json.dumps(max_tweets))

    if os.path.exists(max_tweets_file):
        max_tweets = json.loads(open(max_tweets_file).read())
    else:
        max_tweets = dict()

    print max_tweets_file
    f = open(os.path.join(config['files'], 'tweets_%s.txt' % args.namespace), 'a')
    for account in accounts:
        if account in max_tweets and max_tweets[account] > 0:
            retrieving = "new"
        else:
            retrieving = "old"
            page = 0
        while True:
            if retrieving == "new":
                print 'process %s since id %s' % (account, max_tweets[account])
                try:
                    tweets = api.GetUserTimeline(account, count=200, include_rts=False, since_id=max_tweets[account])
                except twitter.TwitterError, e:
                    print 'error : %s' % str(e)
                    tweets = []
            else:
                print 'process %s from zero, page %s' % (account, page)
                try:
                    tweets = api.GetUserTimeline(account, count=200, include_rts=False, page=page)
                except twitter.TwitterError, e:
                    print 'error : %s' % str(e)
                    tweets = []
            if tweets:
                for s in tweets:
                    if is_valid(s, account):
                        f.write(clean(s.text).lower().encode('UTF-8') + '\n')
                        if  account not in max_tweets or s.id > max_tweets[account]:
                            max_tweets[account] = s.id
                if retrieving == "old":
                    page += 1
                save_max_tweets()
            else:
                print 'no more tweets for %s' % account
                break
    f.close()


def main():
    parser = argparse.ArgumentParser(
                description='Import tweets from a lang')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_fetch = subparsers.add_parser('fetch', help='Fetch tweets')
    parser_fetch.add_argument('-n', '--namespace', dest='namespace', type=str, required=True, help='Namespace')
    parser_fetch.add_argument('-c', '--config', dest='config', type=str, required=True, help='Config File', default='twitter_spelling.conf')
    parser_fetch.set_defaults(func=fetch)

    args = parser.parse_args(sys.argv[1:])
    args.func(args)

if __name__ == '__main__':
    main()
