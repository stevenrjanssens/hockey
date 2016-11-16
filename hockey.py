#!/usr/bin/env python

"""hockey.py -- tool to open extended highlights

Usage:
    hockey.py

Options:
    -h --help  Show this screen.

"""

from __future__ import print_function
import sys
import docopt
import urllib
import subprocess
import json
import datetime

if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)

    stats_api = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate={date}&endDate={date}&expand=schedule.game.content.media.epg'
    games_data = urllib.urlopen(stats_api.format(date=yesterday.strftime("%Y-%m-%d"))).read()
    games = json.loads(games_data)

    for game in games['dates'][0]['games']:
        blurb = game['content']['media']['epg'][2]['items'][0]['blurb']
        extended_highlights = game['content']['media']['epg'][2]['items'][0]['playbacks'][-1]['url']
        print(blurb)
        print(extended_highlights+'\n')
