#!/usr/bin/python3

"""This is a library that provides a class to print statusbars

              It is a part of mammoth-world project
            (https://github.com/vasalf/mammoth-world)

"""

import sys

"""A place to import modules is up to that comment.

"""

__author__ = "vasalf"


class statusbar:
    def __init__(self, classes, length=25, task_length=25):
        self.classes = classes
        self.state = 0
        self.state_status = 0
        self.length = length
        self.task_length = 25

    def __get_string(self, status):
        res = str(int(100 * status)).rjust(3, " ") + "% ["
        for i in range(self.length):
            if status >= (i + 1) / self.length:
                res += "#"
            else:
                res += "-"
        res += "]"
        return res

    def Print(self):
        print(self.classes[self.state][0].ljust(self.task_length, " "), end = " ")
        print(self.__get_string(self.state_status), end="")
        sys.stdout.flush()

    def update(self, k):
        self.state_status += k
        print("\b" * (self.task_length + 1 + 7 + self.length), end="")
        self.Print()

    def finish(self):
        self.state_status = 1
        self.update(0)
        print()
        print(self.classes[self.state][1])
        self.state += 1
        if self.state < len(self.classes):
            self.state_status = 0
            self.Print()

