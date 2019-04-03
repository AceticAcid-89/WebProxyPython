#!/usr/bin/python3.6
# encoding:utf-8

import inspect
import os


def print_ext(msg):
    stack = inspect.stack()
    file_name = "[" + os.path.basename(stack[1][1]) + ":"
    func_name = stack[1][3] + "]"
    line_num = str(stack[1][2])
    print(" ".join([file_name + line_num, func_name, str(msg)]))
