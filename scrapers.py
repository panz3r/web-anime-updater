import cfscrape

from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup as Html

from commons import Episode
from commons import logger as log

class BaseScraper(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def anime_details_from_element(episode_element):
        ret = Episode()

        episode_title = episode_element.string
        slice_index = episode_title.find('Episode')
        ret.series = episode_title[:slice_index].strip()
        episode_num = episode_title[slice_index:]
        ret.title = episode_num[episode_num.find(' '):].strip()
        ret.provider = "Anime1.com"
        ret.link = episode_element.get('href')

        return ret

    @abstractmethod
    def search_episodes(self, page_url):
        raise NotImplementedError()


class Anime1Scraper(BaseScraper):

    def __init__(self):
        self.scraper = cfscrape.create_scraper()

    def search_episodes(self, page_url):
        found_episodes = []

        page_src = self.scraper.get(page_url).content
        html = Html(page_src, 'html.parser')

        episode_elems = html.select('ul.anime-list > li > a')
        log.info('Links found:')

        for e in episode_elems:
            log.debug('> Element text: %s', e.string)

            episode = BaseScraper.anime_details_from_element(e)

            log.info('>> Found %s episode %s @ %s [%s]' % (episode.series, episode.title, episode.provider, episode.link))

            found_episodes.append(episode)

        return found_episodes


if __name__ == '__main__':
    a1s = Anime1Scraper()
    a1s.search_episodes('http://www.anime1.com/watch/arslan-senki-tv-fuujin-ranbu')