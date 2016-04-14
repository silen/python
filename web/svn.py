#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    svn up 文件
'''

import web, json, re, sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')
from lib.sftp import *
urls = (
    '/svn.index', 'index',
)
hostname = '192.168.31.12'
port = 22
username= 'root'
password= 'root1206'
localpath = '/data/'
ftp = Connection(host = hostname,port = port, username = username, password = password)



app = web.application(urls, globals())
render = web.template.render('/data/python/baby.com/web/templates/', cache=False)


# web.template.Template.globals['config'] = config
# web.template.Template.globals['render'] = render
class index:
    def GET(self):
        return render.index()
    def POST(self):
        input = web.input()
        name = input.get('content')
        web.header('Content-Type', 'application/json')
        x = name.encode("utf-8").split("\n")
        _newArr = []
        for x1 in x:
            if x1:
                m = re.match(r'svn up', x1)
                if m is not None:
                    x1 = " && " + x1
                    _newArr.append(x1)

        cmd = 'cd /data/dbx ' + ' '.join(_newArr)
        x_1 = ftp.execute(cmd)


        return json.dumps(x_1)




if __name__ == "__main__":
    app.run()
