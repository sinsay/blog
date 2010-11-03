#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime

class Logging(object):
    pass

def log_info(message):
    print "[{0}] {1}".format(datetime.now().isoformat(" "), message)
