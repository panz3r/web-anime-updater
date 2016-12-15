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

from webanimeupdater.commons import logger as log
from webanimeupdater.tornadoApp import TornadoApp
from webanimeupdater.workers import EPISODE_SEARCH_SCHEDULER

if __name__ == "__main__":
    log.info("Starting episodeSearchScheduler...")
    # start the daily search scheduler
    EPISODE_SEARCH_SCHEDULER.enable = True
    EPISODE_SEARCH_SCHEDULER.start()
    log.info("Started episodeSearchScheduler.")

    log.info("Starting TornadoApp...")
    # start tornado WebApp
    webapp = TornadoApp()
    webapp.start()