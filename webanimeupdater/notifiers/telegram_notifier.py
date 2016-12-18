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

from telegram import Bot

from webanimeupdater import DATABASE_PATH
from webanimeupdater.commons import logger as log
from webanimeupdater.databases.sqlite_database import SQLiteDb
from webanimeupdater.notifiers.base_notifier import BaseNotifier


class Telegram(BaseNotifier):
    def __init__(self):
        self.db = SQLiteDb(DATABASE_PATH)

    def send_message(self, username, message):
        user_settings = self.db.find_user_settings_by_service(username, 'telegram')

        if 'telegram' in user_settings.keys():
            api_key = user_settings['telegram']['api_key']
            chat_id = user_settings['telegram']['chat_id']
            Bot(token=api_key).send_message(chat_id=chat_id, text=message)
        else:
            log.debug("Can't notify user %s because no telegram setup was found" % (username,))
