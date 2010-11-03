# -*- coding:utf-8 -*-

class Comment(object):
    pass

class Category(object):
    pass

class Article(object):
    """
        博客文章
    """
    def __init__(self):
        self.title = None
        self.content = None
        self.addon = None

