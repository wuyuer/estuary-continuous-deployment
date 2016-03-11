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
import pdb

job_map = {}

def parser_all_files(result_dir):
    whole_summary_name = 'whole_summary.txt'
    summary_path = os.path.join(result_dir, whole_summary_name)
    if os.path.exists(summary_path):
        os.remove(summary_path)
    for root, dirs, files in os.walk(result_dir):
        for filename in files:
            if filename.endswith(whole_summary_name):
                continue
            if 'boot' in filename or 'BOOT' in filename:
                continue
            if 'summary' in filename:
                test_case_name = re.findall('[A-Z]+_?[A-Z]*', filename)
                if test_case_name:
                    test_kind = test_case_name[0]
                else:
                    test_kind = ''
                if test_kind:
                    board_type = filename.split(test_kind)[0][:-1]
                else:
                    board_type = filename.split('_summary.txt')[0]
                if test_kind and board_type:
                    with open(board_type + '#' + test_kind, 'a') as f:
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

if __name__ == '__main__':
    try:
        result_dir = sys.argv[1]
    except IndexError:
        print "Need to point out where the outputs store"
        raise
    #print result_dir
    if result_dir:
        parser_all_files(result_dir)
