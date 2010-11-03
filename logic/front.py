# -*- coding:utf-8 -*-

from library import *
from model import *
from base import *

class ArticleLogic(LogicBase):
    def __init__(self, article, db=None):
        super(ArticleLogic, self).__init__(db)
        self.article = article

    def post(self):
        def callback(db):
            return db.article.insert(self.article.__dict__)

        return self._execute(callback)

