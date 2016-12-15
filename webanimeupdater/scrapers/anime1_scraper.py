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

import cfscrape

from bs4 import BeautifulSoup as Html

from webanimeupdater.commons import logger as log
from webanimeupdater.scrapers.base_scraper import BaseScraper


class Anime1Scraper(BaseScraper):
    def __init__(self):
        self.scraper = cfscrape.create_scraper()

    def search_anime(self, page_url):
        anime_details = {'page_url': page_url}

        page_src = self.scraper.get(page_url).content
        html = Html(page_src, 'html.parser')

        anime_title_elems = html.select('.anime > .detail-left > h1.blue-main-title')

        if len(anime_title_elems) > 0:
            anime_title = anime_title_elems[0].string
            log.info('Anime title found: %s', anime_title)
            anime_details['title'] = anime_title

        return anime_details

    def search_episodes(self, page_url):
        found_episodes = []

        page_src = self.scraper.get(page_url).content
        html = Html(page_src, 'html.parser')

        episode_elems = html.select('ul.anime-list > li > a')
        log.info('Links found:')

        for e in episode_elems:
            log.debug('> Element text: %s', e.string)

            episode = BaseScraper.anime_details_from_element(e, "Anime1.com")

            log.info(
                '>> Found %s episode %s @ %s [%s]' % (episode.series, episode.title, episode.provider, episode.link))

            found_episodes.append(episode)

        return found_episodes
