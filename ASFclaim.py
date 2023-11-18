#!/usr/bin/python3
# -*- coding: utf-8 -*-

# pylint: disable=C0103,C0301,W0703

"""
Python translation of https://github.com/C4illin/ASFclaim but doesn't require node.js or any dependencies, only python and its standard, preinstalled libraries.
"""

import sys
import time
import os
import json
import urllib.request
import pprint

ASFPORT = os.environ.get("ASF_PORT", "1242")
ASFHOST = os.environ.get("ASF_HOST", "localhost")
PASSWORD = os.environ.get("ASF_PASSWORD", "")

GIST = "https://gist.githubusercontent.com/C4illin/e8c5cf365d816f2640242bf01d8d3675/raw/Steam%2520Codes"

def checkGame(lastLength):
    with urllib.request.urlopen(GIST) as uh:
        data = uh.read().decode()
    codes = data.split("\n")

    #THIS IS BAD, and definitely not scalable.
    if lastLength < len(codes):
        if lastLength + 10 < len(codes):
            print("Only runs on the last 10 games")
            lastLength = len(codes) - 10

        asfcommand = "!addlicense asf "
        while lastLength < len(codes):
            asfcommand += codes[lastLength] + ","
            lastLength += 1
        asfcommand = asfcommand[:-1]

        command = {'Command': asfcommand}
        url = "http://" + ASFHOST + ":" + ASFPORT + "/Api/Command"
        req = urllib.request.Request(url)
        req.add_header("Content-Type", "application/json")
        if PASSWORD:
            req.add_header("Authentication", PASSWORD)

        try:
            with urllib.request.urlopen(req, json.dumps(command).encode()) as uh:
                res = uh.read().decode()
            body = json.loads(res)
            if body["Success"]:
                print("Success: " + asfcommand)
                pprint.pprint(body)
                with open("lastlength", "w") as f:
                    f.write("{}".format(lastLength))
            else:
                print("Error: ")
                pprint.pprint(body)
        except Exception as err:
            print("error running '{}':".format(command))
            print(err)
    else:
        print("Found: {} and has: {}".format(len(codes), lastLength))
    return lastLength

if __name__ == "__main__":
    lastLength = 0
    try:
        with open("lastlength") as f:
            lastLength=int(f.read())
    except Exception as e:
        print("Error with lastlength: {}".format(e))
        lastLength = 0
        with open("lastlength", "w") as f:
            f.write("{}".format(lastLength))

    while True:
        lastLength = checkGame(lastLength)
        time.sleep(6 * 60 * 60) # Runs every six hours
