
import os
import json
import bcrypt
from abc import ABCMeta, abstractmethod

from tornado import web, ioloop, gen
from tornado.web import authenticated
from tornado.escape import json_encode, utf8

from commons import logger as log
from databases import db
from notifiers import Telegram


def notify_login(user, successfull, details):
    if successfull:
        msg = "User '%s' successfully logged in!" % (user, )
    else:
        msg = "Failed login detected for User '%s': %s" % (user, details)

    try:
        Telegram().send_message(msg)
    except Exception as e:
        log.warn('Exception while sending Telegram notification: %s' % e)


def check_user(username, password):
    user = db.find_user(username)

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

            if not check_user(user_id, utf8(self.get_argument("password"))):
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

            if not check_user(user_id, utf8(self.get_argument("password"))):
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
            entries = db.find()
            self.set_header("Content-Type", "application/json")
            self.write(json_encode(entries))

        def private_post(self):
            log.debug('Posted data: ' + str(self.request.body))
            story_data = json.loads(self.request.body)
            log.debug('Entry data: ' + str(story_data))
            story_id = db.insert(story_data)
            log.info('Entry created with id: %s' % str(story_id))
            self.set_header("Content-Type", "application/json")
            self.set_status(201)

    class EntryAPIHandler(PrivateAPIHandler):

        def private_get(self, entry_id):
            log.debug('Get called with id ' + str(entry_id))
            entries = db.find_by_id(entry_id)
            self.set_header("Content-Type", "application/json")
            self.write(entries)

        def private_post(self):
            pass

    class SubEntriesAPIHandler(PrivateAPIHandler):

        def private_get(self, entry_id):
            log.debug('Get SubEntries called with entry_id: %s' % entry_id)
            entries = db.find_subentries(entry_id)
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
