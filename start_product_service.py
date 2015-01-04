#!/usr/bin/pydoc2.7
import subprocess

rs = subprocess.call("uwsgi -c server_uwsgi.xml -d log/uwsgi.log", shell=True)
if not rs:
    print "Fail"

