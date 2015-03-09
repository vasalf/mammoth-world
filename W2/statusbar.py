#!/usr/bin/python3

import sys

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


st = statusbar([("Task 1", "Finished task 1"), ("Task 2", "Finished task 2")])
st.Print()

from time import sleep

for i in range(2):
    sleep(0.5)
    st.update(0.5)

sleep(0.5)
st.finish()

for i in range(3):
    st.update(1 / 3)
    sleep(1)

st.finish()

