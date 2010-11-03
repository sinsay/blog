# -*- coding:utf-8 -*-

from os import listdir
from os.path import join as pathjoin, dirname, abspath
import settings

BASEPATH = dirname(dirname(abspath(__file__)))

def get_settings(name, default=None):
    return settings.__dict__.get(name, default)

