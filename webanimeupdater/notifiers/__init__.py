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
from webanimeupdater.notifiers.telegram_notifier import Telegram

__NOTIFIERS = {
    'telegram': Telegram()
}


def send_message(user, msg):
    for name, notifier in __NOTIFIERS.items():
        try:
            log.debug('Sending message to %s using %s: %s' % (user, name, msg))
            notifier.send_message(user, msg)
        except Exception as e:
            log.warn('Exception while sending notification: %s' % e)


def notify_login(user, successfull, details):
    if successfull:
        msg = "User '%s' successfully logged in!" % (user,)
    else:
        msg = "Failed login detected for User '%s': %s" % (user, details)

    send_message(user, msg)


def send_episode_link(user, episode):
    log.debug('Sending Episode link notification: %s' % (episode,))
    send_message(user, "Found new episode for %s @ %s. Watch it now! %s" % (episode.series, episode.provider, episode.link))
