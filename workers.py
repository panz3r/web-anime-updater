from abc import ABCMeta, abstractmethod

from scrapers import Anime1Scraper


class BaseWorker(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self, force=False):
        raise NotImplementedError()


class SearchEpisodesWorker(BaseWorker):

    def __init__(self):
        self.amActive = False
        self.scrapers = [Anime1Scraper()]

    def run(self, force=False):
        """
        Runs episode search

        :param force: Force search
        """
        from commons import logger as log
        from databases import db
        from notifiers import Telegram

        if self.amActive:
            return

        self.amActive = True

        series = db.find()
        for s in series:
            episodes = []

            log.info('Searching new episode for series %s' % s['title'])
            for scraper in self.scrapers:
                try:
                    episodes.extend(scraper.search_episodes(s['url']))
                except Exception as e:
                    log.warn('Exception while scraping: %s' % e)

            for episode in episodes:
                inserted = db.insert_episode(episode)
                if inserted:
                    try:
                        Telegram().send_episode_link(episode)
                    except Exception as e:
                        log.warn('Exception while sending Telegram notification: %s' % e)

        # Worker ended
        self.amActive = False
