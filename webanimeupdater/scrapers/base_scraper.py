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

from abc import ABCMeta, abstractmethod

from webanimeupdater.commons import Episode


class BaseScraper(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def anime_details_from_element(episode_element, provider_name):
        ret = Episode()

        episode_title = episode_element.string
        slice_index = episode_title.find('Episode')
        ret.series = episode_title[:slice_index].strip()
        episode_num = episode_title[slice_index:]
        ret.title = episode_num[episode_num.find(' '):].strip()
        ret.provider = provider_name  # "Anime1.com"
        ret.link = episode_element.get('href')

        return ret

    @abstractmethod
    def search_anime(self, page_url):
        raise NotImplementedError()

    @abstractmethod
    def search_episodes(self, page_url):
        raise NotImplementedError()
