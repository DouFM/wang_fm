#!/usr/bin/python2.7
import subprocess

rc = subprocess.call("python manager.py runserver -h 0.0.0.0", shell=True)
if not rc:
    print "fail"
