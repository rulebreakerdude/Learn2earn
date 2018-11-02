#helper functions for the asterisk menu system.
#Meant to be import *'d

import os
import sys

def debugPrint(str):
# stderr goes only to where asterisk was started
    sys.stderr.write(str+'\n')
    sys.stderr.flush()
#    sys.stdout.write("VERBOSE " + str + '\n');
#    sys.stdout.flush()

class KeyPressException(Exception):
    def __init__(self, key):
        self.key = key
    def __str__(self):
        return repr(self.key) + ' was pressed.'

def newKeyDict():
    return {'0':RaiseZero,'#':Nop}

def RaiseZero():
    raise KeyPressException('0')

def RaiseKey(key):
    raise KeyPressException(key)

def Nop():
    pass

def removeTempFile(fname):
    os.remove(fname)
