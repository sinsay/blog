# -*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
from library import *

class LogicBase(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, db):
        self.db = db

    def _execute(self, callback):
        if not self.db:
            with DB() as db: return callback(db)
        else:
            return callback(self.db)

