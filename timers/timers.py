#!/usr/bin/python
#
# The MIT License (MIT)
# Copyright (c) 2016 Eric Ball
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime
from dateutil.relativedelta import relativedelta
import os.path
import sys


class Timer():
    def __init__(self):
        usage = """Usage: timers [add|update|delete args]
 Options:
    add "Event description (past tense)" YYYY/MM/DD
    delete "Event description\""""
        timersFile = os.path.expanduser("~") + "/.timers"
        argsLen = len(sys.argv)
        if argsLen == 1:
            self.printTimers(timersFile)
        elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print usage
            exit(0)
        elif sys.argv[1] == "add":
            if argsLen != 4:
                print usage
                exit(1)
            self.addTimer(timersFile, sys.argv[3], sys.argv[2])

    def printTimers(self, timersFile):
        timerLines = open(timersFile, "r").readlines()
        for n, line in enumerate(timerLines):
            timerWords = line.split()
            if len(timerWords) < 2:
                continue
            date = datetime.strptime(timerWords[0], "%Y%m%d")
            delta = relativedelta(datetime.today(), date)
            years = ""
            months = ""
            days = ""
            if delta.years > 0:
                years = str(delta.years) + " years"
            if delta.months > 0:
                if years:
                    months = ", "
                months += str(delta.months) + " months"
            if delta.days > 0:
                if years or months:
                    days = ", "
                days += str(delta.days) + " days"
            event = " ".join(timerWords[1:])
            print str(n+1) + ". It has been " + years + months + days + \
                " since " + event

    def addTimer(self, timersFile, date, event):
        if date.find("/") > 0:
            dateFormat = "%Y/%m/%d"
        elif date.find("-") > 0:
            dateFormat = "%Y-%m-%d"
        else:
            dateFormat = "%Y%m%d"
        try:
            newDate = datetime.strptime(date, dateFormat)
        except ValueError:
            print "Error: Date should be formatted YYYY/MM/DD"
            exit(1)
        newline = datetime.strftime(newDate, "%Y%m%d") + " " + event + "\n"
        open(timersFile, "a").write(newline)

#    def updateTimer(self, timersFile):

if __name__ == "__main__":
    timer = Timer()
