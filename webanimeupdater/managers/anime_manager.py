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

from webanimeupdater import DATABASE_PATH
from webanimeupdater.commons import logger as log
from webanimeupdater.databases.sqlite_database import SQLiteDb
from webanimeupdater.notifiers import send_episode_link
from webanimeupdater.scrapers.anime1_scraper import Anime1Scraper


class AnimeManager:
    def __init__(self, database_path=DATABASE_PATH):
        self.db = SQLiteDb(database_path)
        self.scraper = Anime1Scraper()

    def get_anime_series(self):
        return self.db.find()

    def get_anime_series_by_id(self, anime_id):
        return self.db.find_by_id(anime_id)

    def get_anime_episodes_by_id(self, anime_id):
        return self.db.find_subentries(anime_id)

    def add_anime_from_url(self, url, username):
        log.debug("add_anime_from_url(url:%s) called...", url)
        anime_details = self.scraper.search_anime(url)
        log.debug("anime_details found: %s", anime_details)
        return self.db.insert_anime(anime_details, username) > 0

    def search_episodes(self):
        series = self.db.find()
        for s in series:
            episodes = []

            log.info('Searching new episode for series %s' % s['title'])

            try:
                episodes.extend(self.scraper.search_episodes(s['url']))
            except Exception as e:
                log.warn('Exception while scraping: %s' % e)

            for episode in episodes:
                inserted = self.db.insert_episode(episode)
                if inserted:
                    try:
                        send_episode_link(episode)
                    except Exception as e:
                        log.warn('Exception while sending Telegram notification: %s' % e)
