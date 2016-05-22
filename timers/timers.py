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
'''
timers is a simple command line application written for GNU/Linux that gives
information on how much time has passed since a past date, or how much time
there is until a future date.
'''
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os.path
import sys


class Timer():
    def __init__(self):
        usage = """Usage: timers [-h|--help|-e|--examples|add|update|delete args]

    -h|--help      Show this help message
    -e|--examples  Show usage examples
    add "Event description (future/past tense)" YYYY/MM/DD
    delete <event_number>
    update <event_number> "Event description" YYYY/MM/DD"""

        examples = """Examples:
    Command: timers add "the beginning of our expedition to the center of the \
Earth" 2040/01/01
    timers Output: "It is X years, X months, and X days until the beginning \
of our expedition to the center of the Earth"
    Command: timers add "we drunkenly applied for a grant to travel to the \
center of the Earth" 2014/05/24
    timers Output: "It has been X years, X months, and X days since we \
drunkenly applied for a grant to travel to the center of the Earth"

    Command: timers delete 1
    Result: Deletes timer numbered 1 (print timers to see numbers)
    Command: timers update 1 "we will get drunk and apply for additional \
shovel funding" 2025/11/09
    Result: Timer 1 will be changed to the text and date specified"""

        timersFile = os.path.expanduser("~") + "/.timers"
        argsLen = len(sys.argv)
        if argsLen == 1 and os.path.exists(timersFile) and \
           len(open(timersFile, "r").read()) > 0:
            self.printTimers(timersFile)
        elif argsLen == 1:
            print """*** ERROR: No timers found; try using the "timers add" \
command. ***"""
            print usage
            exit(0)
        elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print usage
            exit(0)
        elif sys.argv[1] == "-e" or sys.argv[1] == "--examples":
            print examples
            exit(0)
        elif sys.argv[1] == "add":
            if argsLen != 4:
                print usage
                exit(1)
            self.addTimer(timersFile, sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "delete":
            if argsLen != 3 or not sys.argv[2].isdigit():
                print usage
                exit(1)
            self.deleteTimer(timersFile, int(sys.argv[2])-1)
        elif sys.argv[1] == "update":
            if argsLen != 5 or not sys.argv[2].isdigit():
                print usage
                exit(1)
            self.updateTimer(timersFile, int(sys.argv[2])-1, sys.argv[3],
                             sys.argv[4])

    def printTimers(self, timersFile):
        timerLines = open(timersFile, "r").readlines()
        for n, line in enumerate(timerLines):
            timerWords = line.split()
            if len(timerWords) < 2:
                continue
            date = datetime.strptime(timerWords[0], "%Y%m%d")
            delta = relativedelta(date, datetime.today())

            pastTense = False
            today = False
            if delta.years < 0 or delta.months < 0 or delta.days < 0:
                pastTense = True
            elif delta.years == 0 and delta.months == 0 and delta.days == 0:
                today = True
            years = ""
            months = ""
            days = ""
            dYears = abs(delta.years)
            dMonths = abs(delta.months)
            dDays = abs(delta.days)
            if dYears > 0:
                if dYears == 1:
                    years = str(dYears) + " year"
                else:
                    years = str(dYears) + " years"
            if dMonths > 0:
                if years:
                    months = ", "
                if dMonths == 1:
                    months += str(dMonths) + " month"
                else:
                    months += str(dMonths) + " months"
            if dDays > 0:
                if years or months:
                    days = ", "
                if dDays == 1:
                    days += str(dDays) + " day"
                else:
                    days += str(dDays) + " days"
            event = " ".join(timerWords[1:])
            if pastTense:
                print str(n+1) + ". It has been " + years + months + days + \
                    " since " + event
            elif today:
                print str(n+1) + ". Today (is)" + event
            else:
                print str(n+1) + ". It is " + years + months + days + \
                    " until " + event

    def addTimer(self, timersFile, event, date):
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

    def updateTimer(self, timersFile, eventNum, event, date):
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
        timerLines = open(timersFile, "r").readlines()
        newTimerLines = []
        for index, line in enumerate(timerLines):
            if index == eventNum:
                newTimerLines += newline
            else:
                newTimerLines += line
        open(timersFile, "w").writelines(newTimerLines)

    def deleteTimer(self, timersFile, eventNum):
        timerLines = open(timersFile, "r").readlines()
        newTimerLines = []
        for index, line in enumerate(timerLines):
            if index != eventNum:
                newTimerLines += line
        open(timersFile, "w").writelines(newTimerLines)

if __name__ == "__main__":
    timer = Timer()
