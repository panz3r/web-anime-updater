# coding=utf-8
# Author: Mattia Panzeri <panzeri333@gmail.com>
# URL: https://gitlab.com/panz3r/web-anime-updater
#
# This file is part of WebAnimeUpdater.
#
# WebAnimeUpdater is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebAnimeUpdater is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebAnimeUpdater. If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import getopt
import signal

import webanimeupdater


def sig_handler(signum=None, frame=None):
    from webanimeupdater.workers import EPISODE_SEARCH_SCHEDULER

    if not isinstance(signum, type(None)):
        print u"Signal {0:d} caught, saving and exiting...".format(int(signum))
        EPISODE_SEARCH_SCHEDULER.stop()
        # logger.log(u"Signal {0:d} caught, saving and exiting...".format(int(signum)))
        # Shutdown.stop(PID)


signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)


class WebAnimeUpdater:
    def __init__(self):
        from webanimeupdater.commons import logger
        from webanimeupdater.workers import EPISODE_SEARCH_SCHEDULER
        from webanimeupdater.tornadoApp import TornadoApp

        logger.info("Starting episodeSearchScheduler...")
        # start the daily search scheduler
        EPISODE_SEARCH_SCHEDULER.enable = True
        EPISODE_SEARCH_SCHEDULER.start()
        logger.info("Started episodeSearchScheduler.")

        logger.info("Starting TornadoApp...")
        # start tornado WebApp
        webapp = TornadoApp()
        webapp.start()


if __name__ == "__main__":
    try:
        opts, args_ = getopt.getopt(sys.argv[1:], 'hxd::', ['help', 'debug', 'datadir='])
    except getopt.GetoptError:
        sys.exit("Error reading options")

    for option, value in opts:
        # Prints help message
        if option in ('-h', '--help'):
            sys.exit("You won't find any help here :P")

        if option in ('-x', '--debug'):
            webanimeupdater.DEBUG = True

        # Specify folder to use as the data directory
        if option in ('-d', '--datadir'):
            webanimeupdater.DATABASE_PATH = os.path.join(os.path.abspath, value, 'wau.db')

    WebAnimeUpdater()
