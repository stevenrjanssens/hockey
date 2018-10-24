#!/usr/bin/env python

"""hockey.py -- tool to open extended highlights

Usage:
    hockey.py [options] [<team>]

Options:
    -h --help  Show this screen.
    -d DATE    YYYY-MM-DD

"""

from __future__ import print_function
import docopt
import sys
import requests
import subprocess
import json
import datetime

if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    team = arguments['<team>']
    if team:
        team = team.lower()
    date = arguments['-d']

    if date and date.lower() == 'today':
        date = datetime.date.today()
    elif date:
        yyyy, mm, dd = [int(i) for i in date.split('-')]
        date = datetime.date(yyyy, mm, dd)
    else:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(1)
        date = yesterday

    stats_api = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate={date}&endDate={date}&expand=schedule.game.content.media.epg'
    r = requests.get(stats_api.format(date=date.strftime('%Y-%m-%d')))
    data = json.loads(r.text)

    if data['totalGames'] == 0:
        print('No games')
        sys.exit()

    if not team:
        print('Games on {}\n'.format(date.strftime('%Y-%m-%d')))

    for game in data['dates'][0]['games']:
        blurb = game['content']['media']['epg'][2]['items'][0]['blurb']
        teams = ' '.join(blurb.split(':')[1].split('@')).lower()
        extended_highlights = game['content']['media']['epg'][2]['items'][0]['playbacks'][-1]['url']
        if not team:
            print(blurb)
            print(extended_highlights+'\n')
        elif team in teams:
            subprocess.call('open -a \'QuickTime Player\' {:s}'.format(extended_highlights), shell=True)
