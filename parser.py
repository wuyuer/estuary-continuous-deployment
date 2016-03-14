#!/usr/bin/env python
# -*- coding: utf-8 -*-
#                      
#    E-mail    :    wu.wu@hisilicon.com 
#    Data      :    2016-03-11 14:26:46
#    Desc      :

# this file is just for the result parsing
# the input is files in the directory named ''

import os
import subprocess
import fnmatch
import time
import re
import sys
import shutil
import pdb

job_map = {}

parser_result = 'parser_result'
board_type_pre = 'board_type_'
summary_post = '_summary.txt'
board_pre = 'board#'
whole_summary_name = 'whole_summary.txt'
match_str = '[A-Z]+_?[A-Z]*'

def summary_for_kind(result_dir):
    for root, dirs, files in os.walk(result_dir):
        for filename in files:
            if filename.endswith(whole_summary_name):
                continue
            if 'boot' in filename or 'BOOT' in filename:
                if not re.findall(match_str, filename):
                   print filename
                continue
            if 'summary' in filename:
                test_case_name = re.findall(match_str, filename)
                if test_case_name:
                    test_kind = test_case_name[0]
                else:
                    test_kind = ''
                if test_kind:
                    board_type = filename.split(test_kind)[0][:-1]
                else:
                    board_type = filename.split(summary_post)[0]
                if test_kind and board_type:
                    board_class = os.path.join(parser_result, board_type_pre + board_type)
                    if not os.path.exists(parser_result):
                        os.mkdir(parser_result)
                    # create the directory for the special kind of board
                    if not os.path.exists(board_class):
                        os.makedirs(board_class)
                    # create the test for each kind test, each file with one file
                    test_kind_name = os.path.join(board_class, test_kind)
                    if os.path.exists(test_kind_name):
                        os.remove(test_kind_name)
                    with open(test_kind_name, 'a') as f:
                        with open(os.path.join(root, filename), 'r') as rfd:
                            contents = rfd.read()
                        f.write(board_type + '_' + test_kind + '\n')
                        for case in contents.split('\n\n'):
                            test_case = re.findall("=+\s*\n(.*)\s*\n=+", case, re.DOTALL)
                            if test_case:
                                testname = test_case[0]
                                fail_flag = re.findall('FAIL', case)
                                if fail_flag:
                                    f.write( '\t' + testname + '     ' + 'FAIL\n')

def summary_for_board(result_dir):
    for root, dirs, files in os.walk(result_dir):
        for dirname in dirs:
            if board_type_pre in dirname:
                board_type = dirname.split(board_type_pre)[-1]
                board_summary_name = board_pre + board_type
                if os.path.exists(board_summary_name):
                    os.remove(board_summary_name)
                for root, dirs, files in os.walk(root):
                    for filename in files:
                        with open(board_summary_name, 'ab') as fd:
                            with open(os.path.join(root, filename), 'rb') as rfd:
                                lines = rfd.read()
                                fd.write(lines)
                        shutil.move(board_summary_name, result_dir)

def parser_all_files(result_dir):
    summary_path = os.path.join(result_dir, whole_summary_name)
    if os.path.exists(summary_path):
        os.remove(summary_path)
    # get the each kind tests in each file
    summary_for_kind(result_dir)
    # summary each file for each kind of board
    if os.path.exists(parser_result):
        summary_for_board(parser_result)
    if os.path.exists(os.path.join(result_dir, parser_result)):
        shutil.rmtree(os.path.join(result_dir, parser_result))
    shutil.move(parser_result, result_dir)

if __name__ == '__main__':
    try:
        result_dir = sys.argv[1]
    except IndexError:
        print "Need to point out where the outputs store"
        raise
    #print result_dir
    if result_dir:
        parser_all_files(result_dir)
