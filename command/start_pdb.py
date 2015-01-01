#!/usr/bin/python2.7
import subprocess
child1 = subprocess.Popen(["sudo", "lsof", "-i"], stdout=subprocess.PIPE)
child2 = subprocess.Popen(["grep", "5000"], stdin=child1.stdout, stdout=subprocess.PIPE)
result = child2.communicate()
for elem in result:
    print elem
