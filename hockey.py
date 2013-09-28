#!/usr/bin/env python

"""hockey.py -- tool to open hockey streams from the command line

Usage:
    hockey.py
    hockey.py [<team>] [-q QUALITY | --quality=QUALITY] [-a APPLICATION] [-v | --verbose]
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
import xml.etree.ElementTree as ET

arguments = docopt.docopt(__doc__)

list_games = arguments['--list']
list_streams = arguments['--streams']
quality = arguments['--quality'] 
desired_feed = arguments['<team>']
verbose = arguments['--verbose']
if desired_feed:
    desired_feed = desired_feed.lower()
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
        if list_streams:
            output.append("{0:s}: {1:s}".format(feed_team.upper(), formatted_url))

if not desired_feed:
    output = "\n".join(output)+"\n"
    sys.stdout.write(output)
else:
    command = "open -a \"{0:s}\" {1:s}".format(application, feeds[desired_feed])
    if verbose:
        print command
    subprocess.call(command, shell=True)

sys.exit()

