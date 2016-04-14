"""
This is sample example code for track file which have no data is moved to zero data files directory.
"""
import os,json,sys,time

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')


from lib.sftp import *

from config.config import *
hostname = '192.168.31.12'
port = 22
username= 'root'
password= 'root1206'
localpath = '/data/'

ftp = Connection(host = hostname,port = port, username = username, password = password)
x = ftp.execute('cd /data/ && svn co http://bbelephant.imwork.net:8010/svn/dbx/trunk/dbx  --username silen --password 1206 --no-auth-cache ')

for i in x:
    print i