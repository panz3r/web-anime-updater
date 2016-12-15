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
import sqlite3
import unittest

from webanimeupdater.managers import anime_manager

ANIME_DETAILS_TEST_CASES = {
    'http://www.anime1.com/watch/chis-sweet-home-2016': "Chi's Sweet Home (2016)",
    'http://www.anime1.com/watch/arslan-senki-tv-fuujin-ranbu': "Arslan Senki (TV): Fuujin Ranbu"
}

TEST_DB_NAME = 'test.db'


class AnimeManagerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AnimeManagerTests, self).__init__(*args, **kwargs)
        self.instance = anime_manager.AnimeManager(TEST_DB_NAME)

    def test_add_anime_from_url(self):
        for url, anime_title in ANIME_DETAILS_TEST_CASES.items():
            self.assertTrue(self.instance.add_anime_from_url(url))

    def test_add_anime_from_url_repeat(self):
        for url, anime_title in ANIME_DETAILS_TEST_CASES.items():
            self.assertRaises(sqlite3.IntegrityError, self.instance.add_anime_from_url, url)

    @classmethod
    def tearDownClass(cls):
        # Remove test.db
        os.remove(TEST_DB_NAME)
