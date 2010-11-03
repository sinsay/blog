#! -*- coding:utf-8 -*-

from unittest import TestCase, FunctionTestCase, TestSuite, TextTestRunner, defaultTestLoader
import article

def run():
    suites = TestSuite((article.test()))
    TextTestRunner().run(suites)

