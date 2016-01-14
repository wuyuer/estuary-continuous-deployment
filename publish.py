#!/usr/bin/env python
# -*- coding: utf-8 -*-
#                      
#    E-mail    :    wu.wu@hisilicon.com 
#    Data      :    2016-01-08 14:51:06
#    Desc      :
import os
import sys
import json
import time
import getopt
import requests
from urlparse import urljoin

url = "http://192.168.1.108:8888/"
token = "76e91b9b-d85e-4c2b-a102-fc6bdb8efe86"

if not os.environ.has_key('TREE_NAME'):
    os.environ['TREE_NAME'] = 'master'
job = os.environ["TREE_NAME"]

def publish( platform='d02', directory=None, job=None):
    global url
    publish_path = os.path.join(job, directory, platform)
    headers = {
            'Authorization': token
            }
    data = {
            'path': publish_path
            }
    count = 1
    artifacts = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            name = file_name
            # get the relative subdir path
            subdir = os.path.relpath(root, directory)
            name = os.path.join(subdir, file_name)
            artifacts.append(('file' + str(count), 
                (name, open(os.path.join(root, file_name), 'rb'))))
            count += 1
    url = urljoin(url, '/upload')
    retry = True
    while retry:
        response = requests.post(url, data=data, headers=headers, files=artifacts)
        if response.status_code != 200:
            print "ERROR: Failed to publish"
            print response.content
            time.sleep(10)
        else:
            print "INFO: published artifacts"
            for publish_result in json.loads(response.content)["result"]:
                print "%s/%s" % (publish_path, publish_result['filename'])
            retry = False


if __name__ == "__main__":
    git_des = None
    direc = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:d:j:")
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    for option, value in opts:
        if option == '-p':
            platform = value
        if option == '-d':
            direc = value
        if option == '-j':
            job = value
    publish(platform=platform, directory=direc, job=job)
