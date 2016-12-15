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

import json
import os
from abc import ABCMeta, abstractmethod

from tornado import web, ioloop, gen
from tornado.escape import json_encode, utf8
from tornado.web import authenticated

from webanimeupdater.commons import logger as log
from webanimeupdater.managers import anime_manager, user_manager

ANIME_MANAGER = anime_manager.AnimeManager()
USER_MANAGER = user_manager.UserManager()


class TornadoApp:
    WWW_PATH = os.path.join(os.path.dirname(__file__), "ui", "dist")

    settings = {
        "template_path": os.path.join(WWW_PATH, "templates"),
        "static_path": os.path.join(WWW_PATH, "static"),
        "login_url": "/login",
        "cookie_secret": "wkhatanLb]5j4fqVAfuzdk%4npviSdmuGrd",
        "debug": True
    }

    class IndexHandler(web.RequestHandler):
        def get_current_user(self):
            return self.get_secure_cookie("webanimeupdater_user")

        @authenticated
        def get(self):
            self.render("index.html")

    class LoginHandler(web.RequestHandler):
        def get(self):
            self.render("login.html")

        @gen.coroutine
        def post(self):
            user_id = utf8(self.get_argument("username"))

            if not USER_MANAGER.check_user(user_id, utf8(self.get_argument("password"))):
                self.render("login.html")
                return
            else:
                self.set_secure_cookie("webanimeupdater_user", str(user_id))
                self.redirect(self.get_argument("next", "/"))

    class LogoutHandler(web.RequestHandler):
        def get(self):
            self.clear_cookie("webanimeupdater_user")
            self.redirect("/")

    class LoginAPIHandler(web.RequestHandler):

        def get(self):
            log.debug('LoginAPIHandler.get() called...')
            if not self.current_user:
                self.set_status(403)
            else:
                self.set_status(201)

        @gen.coroutine
        def post(self):
            user_id = utf8(self.get_argument("username"))

            if not USER_MANAGER.check_user(user_id, utf8(self.get_argument("password"))):
                self.set_status(403)
            else:
                self.set_secure_cookie("webanimeupdater_user", str(user_id))
                self.set_status(201)

    class PrivateAPIHandler(web.RequestHandler):
        __metaclass__ = ABCMeta

        def get_current_user(self):
            return self.get_secure_cookie("webanimeupdater_user")

        def get(self, *args, **kwargs):
            log.debug('PrivateAPIHandler.get() called...')
            if not self.current_user:
                self.set_status(403)
            else:
                self.private_get(*args, **kwargs)

        @abstractmethod
        def private_get(self, *args, **kwargs):
            pass

        def post(self, *args, **kwargs):
            log.debug('PrivateAPIHandler.post() called...')
            if not self.current_user:
                self.set_status(403)
            else:
                self.private_post(*args, **kwargs)

        @abstractmethod
        def private_post(self, *args, **kwargs):
            pass

    class EntriesAPIHandler(PrivateAPIHandler):

        def private_get(self):
            log.debug('EntriesAPIHandler.get() called...')
            entries = ANIME_MANAGER.get_anime_series()
            self.set_header("Content-Type", "application/json")
            self.write(json_encode(entries))

        def private_post(self):
            log.debug('Posted data: ' + str(self.request.body))
            entry_data = json.loads(self.request.body)
            log.debug('Entry data: ' + str(entry_data))
            if not entry_data['page_url'] is None:
                entry_id = ANIME_MANAGER.add_anime_from_url(entry_data['page_url'])
                log.info('Entry created with id: %s' % str(entry_id))
                self.set_header("Content-Type", "application/json")
                self.set_status(201)
            self.set_status(200)

    class EntryAPIHandler(PrivateAPIHandler):

        def private_get(self, entry_id):
            log.debug('Get called with id ' + str(entry_id))
            entries = ANIME_MANAGER.get_anime_series_by_id(entry_id)
            self.set_header("Content-Type", "application/json")
            self.write(entries)

        def private_post(self):
            pass

    class SubEntriesAPIHandler(PrivateAPIHandler):

        def private_get(self, entry_id):
            log.debug('Get SubEntries called with entry_id: %s' % entry_id)
            entries = ANIME_MANAGER.get_anime_episodes_by_id(entry_id)
            self.set_header("Content-Type", "application/json")
            self.write(json_encode(entries))

        def private_post(self):
            pass

    def __init__(self):
        self.application = web.Application([
            (r"/", self.IndexHandler),
            (r"/index.html", self.IndexHandler),
            (r"/login", self.LoginHandler),
            (r"/logout", self.LogoutHandler),
            (r"/api/v1/login", self.LoginAPIHandler),
            (r"/api/v1/entries", self.EntriesAPIHandler),
            (r"/api/v1/entries/(.*)", self.EntryAPIHandler),
            (r"/api/v1/subentries/(.*)", self.SubEntriesAPIHandler),
        ], **self.settings)

    def start(self):
        self.application.listen(8888)
        ioloop.IOLoop.instance().start()
