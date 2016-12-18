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

import bcrypt

from tornado.escape import utf8

from webanimeupdater import DATABASE_PATH
from webanimeupdater.commons import logger as log
from webanimeupdater.databases.sqlite_database import SQLiteDb
from webanimeupdater.notifiers import notify_login


class UserManager:
    def __init__(self, database_path=DATABASE_PATH):
        self.db = SQLiteDb(database_path)

    def get_user_details(self, username):
        return self.db.find_user(username)

    def check_user(self, username, password):
        user = self.get_user_details(username)

        if user is not None:
            if bcrypt.hashpw(utf8(password), utf8(user['password'])) == user['password']:
                log.debug("Password matches!")
                notify_login(username, True, '')
                return True
            else:
                log.debug("Password does not match!")
                notify_login(username, False, "Password didn't matched")
                return False
        else:
            log.debug('User does not exists!')
            notify_login(username, False, "User not found")

            return False

    def get_user_settings(self, username):
        user_settings = {'username': username}

        external_settings = self.db.find_user_settings(username)
        user_settings['services'] = external_settings

        return user_settings

    def set_user_settings(self, username, settings):
        for service in settings['services']:
            service_settings = settings['services'][service]
            log.debug("'%s' service updated settings: %s" % (service, str(service_settings)))

            if 'settings_id' in service_settings.keys():
                log.debug("Settings should be updated")
                sid = service_settings.pop('settings_id')
            else:
                log.debug("Settings should be inserted")

            self.db.update_user_settings(username, service, service_settings)
