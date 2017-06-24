import cherrypy
from cherrypy.test import helper
from cr.api import server


class SimpleCPTest(helper.CPWebCase):
    def setup_server():
        server.run()

    setup_server = staticmethod(setup_server)

    def test_login(self):
        self.getPage("/login")
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'text/html;charset=utf-8')
        self.assertBody('Hello world')

    def test_non_utf8_message_will_fail(self):
        """
        CherryPy defaults to decode the query-string
        using UTF-8, trying to send a query-string with
        a different encoding will raise a 404 since
        it considers it's a different URL.
        """
        self.getPage("/echo?message=A+bient%F4t",
                     headers=[
                         ('Accept-Charset', 'ISO-8859-1,utf-8'),
                         ('Content-Type', 'text/html;charset=ISO-8859-1')
                     ]
                     )
        self.assertStatus('404 Not Found')
