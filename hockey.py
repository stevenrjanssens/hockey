#!/usr/bin/env python

"""hockey.py -- tool to open hockey streams from the command line

Usage:
    hockey.py
    hockey.py [<team>...] [-q QUALITY | --quality=QUALITY] [-a APPLICATION] [-v | --verbose]
    hockey.py [-l | --list] [-s | --streams]
    hockey.py (-h | --help)

Options:
    -h --help                     Show this screen.
    -l --list                     List available games today.       
    -s --streams                  Include stream links in list.
    -q QUALITY --quality=QUALITY  Set stream quality [default: 3000].
    -a APPLICATION                Application to open stream with.
    -v --verbose                  Turn on verbose messages.

"""

import sys
import docopt
import urllib
import subprocess
import json
import datetime

arguments = docopt.docopt(__doc__)

list_games = arguments['--list']
list_streams = arguments['--streams']
quality = arguments['--quality'] 
desired_feeds = arguments['<team>']
verbose = arguments['--verbose']
if desired_feeds:
    desired_feeds = [feed.lower() for feed in desired_feeds]
application = arguments['-a']
if not application:
    application = "QuickTime Player.app"
if verbose:
    print arguments
if quality not in ["800", "1600", "3000", "4500"]:
    print "Error: invalid quality"
    sys.exit()

games_url = "http://live.nhl.com/GameData/SeasonSchedule-20132014.json"
games_data = urllib.urlopen(games_url).read()
games = json.loads(games_data)

today = datetime.date.today().strftime("%Y%m%d")

feeds = {}
output = []
for game in games:
    date, time = game['est'].split()
    if date != today:
        continue
    game_id = str(game['id'])
    game_id = game_id[4:6]+"_"+game_id[6:]
    stream_url = "http://smb.cdnak.neulion.com/fs/nhl/mobile/feed_new/data/streams/2013/ipad/{0:s}.json".format(game_id)
    stream_data = urllib.urlopen(stream_url).read()
    streams = json.loads(stream_data)
    output.append("{0:s} @ {1:s} {2:s}".format(game['a'], game['h'], game['est']))
    try:
        ipad_home = streams['gameStreams']['ipad']['home']['live']['bitrate0']
        ipad_away = streams['gameStreams']['ipad']['away']['live']['bitrate0']
        home_stream = ipad_home.replace("ipad", quality)
        away_stream = ipad_away.replace("ipad", quality)
        feeds[game['h'].lower()] = home_stream
        feeds[game['a'].lower()] = away_stream
        if list_streams:
            output.append("{0:s}: {1:s}".format(game['a'], away_stream))
            output.append("{0:s}: {1:s}\n".format(game['h'], home_stream))
    except KeyError:
        if list_streams:
            output.append("No streams yet\n")

if not desired_feeds:
    output = "\n".join(output)+"\n"
    sys.stdout.write(output)
else:
    for desired_feed in desired_feeds:
        command = "open -a \"{0:s}\" {1:s}".format(application, feeds[desired_feed])
        if verbose:
            print command
        subprocess.call(command, shell=True)

sys.exit()

