#!/usr/bin/env python

"""Tool to open NHL GameCenter streams from the command line.

Usage:
    hockey.py
    hockey.py [<team>] [-q QUALITY | --quality=QUALITY] [-a APPLICATION] [-v | --verbose]
    hockey.py [[--games | -g ] | [--feeds | -f]] 
    hockey.py (-h | --help)

Options:
    -h --help                     Show this screen.
    -g --games                    List available games today.       
    -f --feeds                    List available feeds today.
    -q QUALITY --quality=QUALITY  Set stream quality [default: 4500].
    -a APPLICATION                Application to open stream with.
    -v --verbose                  Turn on verbose messages.

"""

import sys
import docopt
import urllib
import subprocess
import xml.etree.ElementTree as ET

arguments = docopt.docopt(__doc__)

list_feeds = arguments['--feeds']
list_games = arguments['--games']
quality = arguments['--quality'] 
desired_feed = arguments['<team>']
verbose = arguments['--verbose']
if not desired_feed:
    desired_feed = "van"
application = arguments['-a']
if not application:
    application = "QuickTime Player.app"
if verbose:
    print arguments

url = "http://208.92.36.37/nlds/as3/get_games.php?client=nhl&playerclient=hop"
data = urllib.urlopen(url).read()
root = ET.fromstring(data)

feeds = {}
output = []

for game in root:
    game_date = game.attrib['game_date']
    home_team = game.find("home_team").text
    away_team = game.find("away_team").text
    output.append("{0:s}@{1:s} {2:s}".format(away_team, home_team, game_date))
    for assignment in game.find("assignments"):
        feed_display_name = assignment.attrib["feed_display_name"].capitalize()
        if feed_display_name == "Home":
            feed_team = home_team.lower()
        else:
            feed_team = away_team.lower()
        ipad_url = assignment.find("ipad_url").text
        formatted_url = ipad_url.replace("ipad", quality)
        feeds[feed_team] = formatted_url
        if list_feeds:
            output.append("{0:s}: {1:s}".format(feed_team.upper(), formatted_url))

if list_feeds or list_games:
    output = "\n".join(output)+"\n"
    sys.stdout.write(output)
else:
    command = "open -a \"{0:s}\" {1:s}".format(application, feeds[desired_feed])
    if verbose:
        print command
    subprocess.call(command, shell=True)

sys.exit()

