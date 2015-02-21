#!/usr/bin/env python2
#Snap! extension base by Technoboy10
#features by Timo

data = dict()

import SimpleHTTPServer
class CORSHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.path
        ospath = os.path.abspath('')
        if '/put' in path:
            regex = re.compile("\/put\?value=(.*?)&key=(.*)")
            m = regex.match(path)
            value = urllib2.unquote(m.group(1))
            key = urllib2.unquote(m.group(2))
            data[key] = value
            return

        if '/check' in path:
            regex = re.compile("\/check\?key=(.*)")
            m = regex.match(path)
            key = urllib2.unquote(m.group(1))
            f = open(ospath + '/return', 'w+')
            f.write(str(key in data))
            f.close()
        if '/get' in path:
            regex = re.compile("\/get\?key=(.*)")
            m = regex.match(path)
            key = urllib2.unquote(m.group(1))
            if not key in data:
                return ''

            f = open(ospath + '/return', 'w+')
            f.write(str(data[key]))
            f.close()
	if '/list' in path:
            f = open(ospath + '/return', 'w+')
            f.write(data.keys().join('\n'))
            f.close()

        f = open(ospath + '/return', 'rb')
        ctype = self.guess_type(ospath + '/return')
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        return f

if __name__ == "__main__":
    import os
    import re
    import SocketServer
    import urllib2
    PORT = 9876 #Pick a port number

    Handler = CORSHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    httpd.serve_forever()
