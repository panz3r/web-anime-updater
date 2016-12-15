import unittest

from webanimeupdater.scrapers.anime1_scraper import Anime1Scraper

ANIME_DETAILS_TEST_CASES = {
    'http://www.anime1.com/watch/chis-sweet-home-2016': "Chi's Sweet Home (2016)",
    'http://www.anime1.com/watch/arslan-senki-tv-fuujin-ranbu': "Arslan Senki (TV): Fuujin Ranbu"
}


class Anime1ScraperTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Anime1ScraperTests, self).__init__(*args, **kwargs)
        self.scraper = Anime1Scraper()

    def test_search_anime(self):
        for url, anime_title in ANIME_DETAILS_TEST_CASES.items():
            self.assertEqual(self.scraper.search_anime(url)['title'], anime_title)

    def test_search_episodes(self):
        for url, anime_title in ANIME_DETAILS_TEST_CASES.items():
            self.assertIsNotNone(self.scraper.search_episodes(url))
