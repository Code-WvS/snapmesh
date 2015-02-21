# Copyright (C) 2013 Connor Hudson, Tim Radvan

"""Module for writing Snap! extensions.

See example.py for usage.

Handler functions should return unicode. Non-unicode strings are assumed to
be UTF-8 encoded.

"""

__version__ = '0.1.4'

import inspect
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from urlparse import urlsplit, parse_qs
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import TCPServer



class SnapHandler(SimpleHTTPRequestHandler):
    """An HTTP handler with Flask-style routing."""

    routes = {}

    special = {
        'true': True,
        'True': True,
        'false': False,
        'False': False,
    }

    @classmethod
    def prettify_arg(cls, value):
        value = value.decode('utf-8')
        value = cls.special.get(value, value)
        if isinstance(value, bool):
            return value
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value # str

    def send_head(self):
        split_url = urlsplit(self.path)
        path = split_url.path
        params = parse_qs(split_url.query)
        params = dict((k, self.prettify_arg(v[0])) for (k, v) in params.items())
        print 'params', params
        is_browser = "text/html" in self.headers['Accept']

        (status, mime_type, response) = self.get_response(path, params,
                                                          is_browser)
        if isinstance(response, str):
            response = response.decode('utf-8')
        else:
            response = unicode(response)

        if is_browser and mime_type == "text/plain":
            mime_type = "text/html"
            response = u"""{response}""".format(title=path, response=response)

        if isinstance(response, unicode):
            response = response.encode('utf-8')

        self.send_response(status)
        self.send_header("Content-Type", mime_type)
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        return StringIO(response)

    def get_response(self, path, params, is_browser):
        mime_type = "text/plain"
        if path in self.routes:
            f = self.routes[path]
            try:
                response = f(**params)
                if response is None:
                    response = ""
                elif response is True:
                    response = "true"
                elif response is False:
                    response = "false"
                return (200, mime_type, response)
            except KeyboardInterrupt:
                raise
            except TypeError, e:
                for param in inspect.getargspec(f).args:
                    if param not in params:
                        response = "ERROR: Missing argument %r" % param
                        return (400, mime_type, response)
                else:
                    raise
        elif path == '/':
            return self.index(is_browser)
	elif path == '/crossdomain.xml':
	    return """
<?xml version="1.0"?>
<cross-domain-policy>
    <allow-access-from domain="*" to-ports="*"/>
</cross-domain-policy>
	    """
        else:
            return (404, mime_type, "ERROR: Route not found")

    def index(self, is_browser):
        """Return the list of routes in plain text format."""
        if is_browser:
            html = u"""<!DOCTYPE html>
            <meta charset="utf8">
            <title>/</title>
            <ul>
            """
            for path in sorted(self.routes):
                f = self.routes[path]
                params = inspect.getargspec(f).args
                qs = "&".join("%s=" % p for p in params)
                if qs:
                    path += "?" + qs
                html += u'<li><a href="{path}">{path}</a>'.format(path=path)
            return (200, "text/html", html)
        else:
            response = "\n".join(sorted(self.routes))
            return (200, "text/plain", response)

    @classmethod
    def add_route(self, path, f):
        """Same as the :meth:`route` decorator.

            @handler.route('/')
            def index():
                pass

        Is equivalent to:

            def index():
                pass
            handler.add_url_rule('/', 'index', index)

        """
        if path in self.routes and path != '/':
            raise ValueError, "route already exists"
        self.routes[path] = f

    @classmethod
    def route(self, path, **options):
        def decorator(f):
            self.add_route(path, f, **options)
            return f
        return decorator


class Server(TCPServer):
    allow_reuse_address = True


def main(handler, port, silent=False):
    """Runs the server for Snap! to connect to."""
    httpd = Server(("", port), handler)
    if not silent:
        print "Serving at port %i" % port
        print "Go ahead and launch Snap!"
    httpd.serve_forever()

