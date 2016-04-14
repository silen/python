#!/usr/bin/env python
#_*_coding:utf8_*_
"""
    svn log 内容写入文件  专注author is huangwz
"""
import sys
import os
import subprocess
import re
import time,inspect

s_path = os.path.abspath(os.path.dirname(inspect.stack()[0][1]))

def run():
    filename = conversion2path(s_path+ '/../document/svnlog/' + time.strftime('%Y%m',time.localtime(time.time()))+'/' + time.strftime('%Y%m%d',time.localtime(time.time())) + '.txt')
    TIME,txt = svncmd()
    if TIME:

        if os.path.isfile(filename):
            f = open(filename, 'r')
            for line in f.readlines():
                if TIME == line:
                    print '\n'+txt
                    print '这次更新已经写入文件了 ---->'+filename + '\n'
                    return '';
        else:
        	if os.path.isdir(os.path.dirname(filename)) == False:os.mkdir(os.path.dirname(filename))
            
        file_object = open(filename, 'a')
        file_object.write(txt)
        file_object.close( )
        print '\n\n写入文件 -->' + filename;
        print txt
    else:
        print txt

def conversion2path(filename):
    xx = []
    filename = filename.split('/')
    for i in range(len(filename)):
        if filename[i] == '..':
            del xx[i-1]
        else:
            xx.append(filename[i])
    return '/'.join(xx)
def svncmd():

    cmd = 'svn up';
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    cmd = 'svn log -l 1 -v';
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #r9802 | licy | 2014-04-01 10:23:41 +0800 (二, 2014-04-01) | 1 行
    # M /trunk/
    path = '';
    TIME = None;
    for line in p.stdout.readlines():
        
        t = re.match(r'.*silen.*', line)
        if t is not None:
            TIME = line
        m = re.match(r'\s*\w\s+\/trunk/python/baby.com', line)
        if m is not None:
            newpath = re.sub(r'\s*\w\s+\/trunk/python/baby.com/', 'svn up ', line)
            if newpath:
                path +=  newpath
    if TIME is None:
        return 0, '\n\nIn this svnlog ,Not find author is silen \n\n';
    return (TIME, TIME + '------------------------------------------------------------------------------\n' + path)

def main():
    run()
    return '';


if __name__ == '__main__':
    main()
