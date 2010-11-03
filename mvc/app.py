#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sys import modules
from os import listdir, chdir
from os.path import join as path_join, basename as path_basename, isdir, abspath
from inspect import isclass
from tornado.httpserver import HTTPServer
from tornado.web import Application as TornadoApplication, StaticFileHandler
from tornado.ioloop import IOLoop
from settings import *
from web import *
from logging import *
from utils import *

@singleton
class Application(object):

    def __init__(self, port = DEFAULT_PORT):
        self._port = port

        self._settings = {
            "static_path" : STATIC_PATH,
            "template_path" : TEMPLATE_PATH,
            "gzip" : GZIP,
            "debug" : DEBUG,
            "cookie_secret" : COOKIE_SECRET,
            "login_url" : LOGIN_URL,
        }

    @property
    def port(self):
        return self._port

    @property
    def settings(self):
        return self._settings

    def _find_handlers(self):
        handlers = []

        # handlers directory
        paths = [BASE_PATH] + \
                [p for (b, p) in subdirs(BASE_PATH) if b not in IGNORE_PATHS]

        # search & load handler
        for path in paths:
            pys = [f.split(".")[0] for f in listdir(path) if f.endswith(".py") and "__init__" not in f]
            package_prefix = path_basename(path) + "." if path != BASE_PATH else ""

            for py in pys:
                module = __import__(package_prefix + py)

                for n, o in module.__dict__.items():
                    if isclass(o) and issubclass(o, BaseHandler) and hasattr(o, "url"):
                        # support multi urls
                        urls = o.url if hasattr(o.url, "__iter__") else [o.url]
                        for url in urls: handlers.append((url, o))

                        log_info("Load {0} from module {1} ...".format(o.__name__, o.__module__))

        # support sorted order
        handlers.sort(cmp, lambda x: x[1].order)
        return handlers

    def _attached_handlers(self):
        # NotFoundHandler must be the last
        return [
            (TEMPLATE_URL, StaticFileHandler, dict(path = TEMPLATE_PATH)),
            (r"/.*", NotFoundHandler)
        ]

    def _start_server(self, handlers):
        app = TornadoApplication(handlers, **self._settings)
        server = HTTPServer(app)
        server.bind(self._port)
        server.start()
        IOLoop.instance().start()

    def start(self):
        handlers = self._find_handlers() + self._attached_handlers()
        self._start_server(handlers)


