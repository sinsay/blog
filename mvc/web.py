#!/usr/bin/env python
# -*- coding:utf-8 -*-

import httplib
from urllib import urlencode
from os.path import exists as path_exists, join as path_join
from tornado.web import RequestHandler
from tornado.template import Template, Loader
from settings import *
from utils import *

class BaseHandler(RequestHandler):
    """
        BaseHandler
    """

    # static members
    loader = Loader(TEMPLATE_PATH)

    # override methods ####################################
    def initialize(self, **kwargs):
        pass

    def prepare(self):
        self._check_login()

    def render_string(self, template_name, **kwargs):
        html = super(BaseHandler, self).render_string(template_name, **kwargs)
        return html

    def get_error_html(self, status_code, **kwargs):
        name = "%d.html" % status_code
        if path_exists(path_join(TEMPLATE_PATH, name)):
            self.set_status(status_code)
            kwargs.update({
                    "status_code": status_code, 
                    "message": httplib.responses[status_code],
                    "url": self.request.full_url(),
            })

            return self.loader.load(name).generate(**kwargs)
        else:
            return super(BaseHandler, self).get_error_html(status_code, **kwargs)

    # action methods #######################################
    def view(self, template_name, **kwargs):
        self.render(template_name, **kwargs)

    def json(self, **kwargs):
        self.write(kwargs)

    def content(self, s):
        self.write(s)

    def partial(self, template_name, **kwargs):
        s = self.loader.load(template_name).generate(**kwargs)
        self.content(s)

    def template(self, template_string, **kwargs):
        s = Template(template_string).generate(**kwargs)
        self.content(s)

    # login methods #######################################
    def _check_login(self):
        if not hasattr(self, "auth"): return
        if not self.current_user:
            self.redirect(LOGIN_URL + "?" + urlencode({"next" :self.request.uri }))
        elif not self.current_user in self.auth:
            self.send_error(401)

    def get_current_user(self):
        return self.get_secure_cookie(COOKIE_USERID)

    def get_next_url(self):
        return self.get_argument("next", default = "/")

    def signin(self, username):
        self.set_secure_cookie(COOKIE_USERID, username, expires_days = None)
        self.redirect(self.get_next_url())

    def signout(self):
        self.clear_cookie(COOKIE_USERID)
        self.redirect(self.get_next_url())

    # cache methods ######################################
    # use Nginx cache module


def url(url, order = -1):
    """
        Class Decorator: Handler, url mapping
    """
    def wrap(handler):
        handler.url = url
        handler.order = order
        return handler

    return wrap


def auth(users = None):
    """
        Class Decorator: Handler, Authenticate
    """
    def wrap(handler):
        handler.auth = users
        return handler

    return wrap


def nocache(method):
    """
        Method Decorator: Handler, action method, No-Cache Control
    """
    def wrap(self, *args, **kwargs):
        self.set_header("Cache-Control", "No-Cache")
        method(self, *args, **kwargs)

    return wrap


class NotFoundHandler(RequestHandler):
    def prepare(self):
        f = path_join(TEMPLATE_PATH, ERROR_404)
        if path_exists(f):
            self.set_status(404)
            self.render(ERROR_404, url = self.request.full_url())
        else:
            self.send_error(404)

