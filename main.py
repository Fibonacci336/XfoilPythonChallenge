import subprocess as sp
#import os
import shutil
import sys
import string

ps = sp.Popen(['/Users/fibonacci/Xfoil/bin/xfoil'],stdin=sp.PIPE,stdout=None, stderr=None)

def issueCmd(cmd,echo=True):
    cmdBytes = bytes(cmd+'\n', 'utf-8')
    ps.stdin.write(cmdBytes)
    if echo:
        print(cmd)
        
issueCmd('load naca633618.dat')
issueCmd('oper')
issueCmd('alfa 0.0')
issueCmd('')
issueCmd('QUIT')
