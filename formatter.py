#!/opt/local/bin/python

import fileinput
import sys
import calendar
import re
import string


class Formatter:

    def __init__(self, filename, inputlines):
        temp_word_list = []
        length = 0
        fmt_mode = 1
        maxwidth = 0
        margin = 0
        temp_margin = 0
        capital = 0
        space = ' '
        print_word_list = []
        width_tracker = 0
        space_count = 0
        mode = 0
        firstline = 0
        margin_c = 0
        date_mode = 0
        replace = 0
        pattern = ""
        pattern1 = ""
        date = []
        month = ""
        d = ""
        l = -1
        firstline = 0
        temp_string = ""
        flag = 0
        self.list = []
        if filename == None and inputlines != None:
            self.inputlines = inputlines
        if filename != None and inputlines == None:
            for line in fileinput.input():
                if l is -1:
                    self.list.append("")
                    firstline = 1
                    l = 0
                if line in ['\n', '\r\n']:
                    if len(print_word_list) > 0:
                        if margin_c == 1:
                            for x in range(margin):
                                self.list[0] += " "
                            flag = 1
                            width_tracker+=len(print_word_list)
                            self.print_line(print_word_list, space, temp_margin, width_tracker,flag)
                            margin_c = 0
                            temp_margin = margin
                            flag = 0
                        else:
                            #for x in range(margin):
                               #self.list[0] += " "
                            width_tracker += len(print_word_list)
                            self.print_line(print_word_list, space, margin, width_tracker,flag)
                        self.list[0] += "\n"
                    else:
                        self.list[0] += "\n"
                    print_word_list.clear()
                    width_tracker = maxwidth-margin
                    continue

                temp_word_list = line.split()
                # ?maxwidth
                if temp_word_list[0] == '?maxwidth':
                    try:
                        right_pattern = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                        for char in temp_word_list[1]:
                            if char not in right_pattern:
                                raise Exception("value of maxwidth must be integer")
                    except Exception:
                        print("value of maxwidth must be integer")
                        sys.exit(-1)
                    maxwidth = int(temp_word_list[1])
                    width_tracker = maxwidth
                # ?fmt
                elif temp_word_list[0] == '?fmt':
                    try:
                        if temp_word_list[1] == 'on':
                            fmt_mode = 1
                        elif temp_word_list[1] == 'off':
                            fmt_mode = 0
                        else:
                            raise Exception("?fmt must be only followed by on or off")
                    except Exception:
                        print("?fmt must be only followed by on or off")
                        sys.exit(-1)
                # ?mrgn
                elif temp_word_list[0] == '?mrgn':
                    try:
                        right_pattern = ['+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                        if temp_word_list[1][0] not in right_pattern:
                            raise Exception("the input must be +, - or integers")
                        pattern = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                        for char in temp_word_list[1][1:]:
                            if char not in pattern:
                                raise Exception("the value of margin must be integer")
                    except Exception:
                        print("the value of margin must be integer")
                        sys.exit(-1)
                    if temp_word_list[1][0] == '+' or temp_word_list[1][0] == '-':
                        margin += int(temp_word_list[1])
                    else:
                        margin = int(temp_word_list[1])
                    if margin > int(maxwidth) - 20 and int(maxwidth) > 0:
                        margin = int(maxwidth) - 20
                    if margin < 0:
                        margin = 0
                    if temp_margin is not margin:
                        margin_c = 1
                # ?monthabbr
                elif temp_word_list[0] == '?monthabbr':
                    try:
                        if temp_word_list[1] == 'on':
                            replace_mode = 1
                        elif temp_word_list[1] == 'off':
                            replace_mode = 0
                        else:
                            raise Exception("the only two valid command after ?monthabbr are on and off")
                    except Exception:
                        print("the only two valid command after ?monthabbr are on and off")
                        sys.exit(-1)
                    date_mode = 1
                # ?replace
                elif temp_word_list[0] == '?replace':
                    try:
                        if len(temp_word_list) is not 3:
                            raise Exception("there must be two patterns for this command to compile")
                    except Exception:
                        print("there must be two patterns for this command to compile")
                        sys.exit(-1)
                    pattern = temp_word_list[1]
                    pattern1 = temp_word_list[2]
                    replace = 1
                # start to format
                else:
                    if fmt_mode == 0:
                        self.list[0] += line
                        self.list[0] += ""
                    else:
                        if maxwidth == 0:
                            if margin >= 0:
                                for x in range(margin):
                                    self.list[0] += " "
                            if replace == 1:
                                line = re.sub(pattern,pattern1,line)
                            if date_mode == 1:
                                date = re.findall(r"\d\d\S\d\d\S\d\d\d\d", line)
                                for x in date:
                                    month = calendar.month_abbr[int(x[0:2])] + '. '
                                    d = str(x[3:5]) + ', '
                                    line = re.sub(x[0:3], month, line)
                                    line = re.sub(x[3:6], d, line)
                            self.list[0] += line
                            self.list[0] += ""
                        else:
                            if replace == 1:
                                line = re.sub(pattern, pattern1, line)
                            if date_mode == 1:
                                date = re.findall(r"\d\d\S\d\d\S\d\d\d\d", line)
                                for x in date:
                                    month = calendar.month_abbr[int(x[0:2])] + '. '
                                    d = str(x[3:5]) + ', '
                                    line = re.sub(x[0:3], month, line)
                                    line = re.sub(x[3:6], d, line)
                            temp_word_list = line.split()
                            if firstline == 1:
                                width_tracker -= margin
                                firstline = 0
                            for word in temp_word_list:
                                if temp_word_list[-1] in ['\n', '\r\n']:
                                    temp_word_list[-1] = ""
                                if len(word) < width_tracker:
                                    print_word_list.append(word)
                                    width_tracker = width_tracker - len(word) - 1
                                elif len(word) == width_tracker:
                                    print_word_list.append(word)
                                    width_tracker = maxwidth - margin
                                    for x in print_word_list:
                                        width_tracker -= len(x)
                                    self.print_line(print_word_list, space, margin, width_tracker,flag)
                                    print_word_list.clear()
                                    width_tracker = maxwidth - margin
                                else:
                                    width_tracker = maxwidth - margin
                                    for x in print_word_list:
                                        width_tracker -= len(x)
                                    # self.list[0]+=str(width_tracker)
                                    self.print_line(print_word_list, space, margin, width_tracker,flag)
                                    print_word_list.clear()
                                    print_word_list.append(word)
                                    width_tracker = maxwidth-len(word) - margin - 1

            if len(print_word_list) > 0:
                width_tracker = maxwidth - margin
                for x in print_word_list:
                    width_tracker -= len(x)
                self.print_line(print_word_list, space, margin, width_tracker, flag)
                print_word_list.clear()

    def print_line(self, mylist, space, margin, width,flag):
        count = 0
        if flag == 0:
            for x in range(margin):
                self.list[0] += space

        if len(mylist) == 1:
            self.list[0] += mylist[0]
        else:
            if width % (len(mylist) - 1) == 0:
                count = int(width / (len(mylist) - 1))
                for word in mylist[0:-1]:
                    self.list[0] += word
                    for x in range(count):
                        self.list[0] += space
                self.list[0] += mylist[-1]
            else:
                remainder = width % (len(mylist) - 1)
                count = int(width / (len(mylist) - 1))
                for word in mylist[0:remainder]:
                    self.list[0] += word
                    for x in range(count + 1):
                        self.list[0] += space
                for word in mylist[remainder:-1]:
                    self.list[0] += word
                    for x in range(count):
                        self.list[0] += space
                self.list[0] += mylist[-1]
        self.list[0] += "\n"

    def get_lines(self):
        return self.list