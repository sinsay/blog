#!/usr/bin/env python
# -*-coding:utf-8 -*-

from os import popen
from cmd import Cmd

import utest

class MyBlog(Cmd, object):
    intro = "\n".join((
            "MyBlog Shell, version 0.9", 
            "Copyright (c) RainTrail Studio. 2000-2010",
            "Syntax:",
            "  help: list commands",
            "  !cmd: execute shell command",
            "  exit: exit shell"
    ))

    prompt = "> "

    def do_EOF(self, line):
        print "bye!"
        return True

    def do_shell(self, line):
        print popen(line).read()

    def do_clean(self, line):
        """
            Remove *.pyc & *.pyo
        """
        print popen("""find . -name "*.py[co]" | xargs rm -rf""").read()

    def default(self, line):
        if line in ("bye", "quit", "q", "exit"):
            self.do_EOF(line)
            exit()

    # Command ##################

    def do_utest(self, line):
        """
            Unit Test
        """
        utest.run()


if __name__ == "__main__":
    MyBlog().cmdloop()
