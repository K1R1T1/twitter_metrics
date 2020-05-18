"""
Import the necessary libraries
"""
import requests
import re
import sys
from bs4 import BeautifulSoup
import logging
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def parse_metrics(url):
    """
    :param url: Twitter URL example : https://twitter.com/BarackObama/status/952914779458424832
    :return: JSON with Metrics.
    """
    logging.info('Input URL = {}'.format(url))

    if url.startswith("https://twitter.com/"):
        logging.info('URL is a valid twitter URL')

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        tweet_id = str([int(s) for s in url.split('/') if s.isdigit()][0])

        re_tweets_id = 'profile-tweet-action-retweet-count-aria-' + tweet_id
        replies_id = 'profile-tweet-action-reply-count-aria-' + tweet_id
        favourites_id = 'profile-tweet-action-favorite-count-aria-' + tweet_id

        rt = str(soup.find_all(id=re_tweets_id))
        rp = str(soup.find_all(id=replies_id))
        fv = str(soup.find_all(id=favourites_id))
        time = str(soup.find_all(class_="tweet-timestamp js-permalink js-nav js-tooltip"))

        try:
            rts = int(re.sub('[^0-9]', '', re.findall(re.compile(r"(?<=>)(.*)(?=</span>)"), rt)[0]))
            rps = int(re.sub('[^0-9]', '', re.findall(re.compile(r"(?<=>)(.*)(?=</span>)"), rp)[0]))
            fav = int(re.sub('[^0-9]', '', re.findall(re.compile(r"(?<=>)(.*)(?=</span>)"), fv)[0]))
            tsp = int(re.sub('[^0-9]', '', re.findall(re.compile(r"(?<=data-time-ms=\")\d{13}(?=\">)"), time)[-1]))
            logging.info('Parsing Successful')
            return {'url': url, 'retweets': rts, 'replies': rps, 'favourites': fav, 'timestamp': tsp}
        except Exception as e:
            logging.info('Encountered error {} during parsing'.format(e))
            return {'url': url, 'retweets': 0, 'replies': 0, 'favourites': 0, 'timestamp': 0}
    else:
        logging.info('URL is not a valid twitter URL')
        return {'url': url, 'retweets': 0, 'replies': 0, 'favourites': 0, 'timestamp': 0}


def main():
    metrics = parse_metrics(str(sys.argv[1]))
    return metrics


if __name__ == '__main__':
    main()
