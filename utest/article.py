#!/usr/bin/env python
# -*- coding:utf-8 -*-

from unittest import TestCase, FunctionTestCase, TestSuite, TextTestRunner, defaultTestLoader
from datetime import datetime
from settings import *
from library import *
from logic import *

class ArticleTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_post(self):
        a = Article()
        a.title = "title..."
        a.content = "content..."
        a.addon = datetime.now()

        with DB() as db:
            for i in range(10):
                id = ArticleLogic(a, db).post()
                print id
                self.assertTrue(id)

def test():
    return TestSuite(map(ArticleTest, ["test_post"]))
