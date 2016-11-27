import telegram

from abc import ABCMeta, abstractmethod

from commons import logger as log
from configs import TELEGRAM_API_KEY, TELEGRAM_CHAT_ID


class BaseNotifier(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_message(self, message):
        raise NotImplementedError()

    @abstractmethod
    def send_episode_link(self, episode):
        raise NotImplementedError()


class Telegram:

    def __init__(self):
        self.bot = telegram.Bot(token=TELEGRAM_API_KEY)

    def send_message(self, message):
        self.bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=message)

    def send_episode_link(self, episode):
        log.debug('Sending Episode link message using Telegram: %s' % episode)
        self.send_message("Found new episode for %s @ %s. Watch it now! %s" % (episode.series, episode.provider, episode.link))
