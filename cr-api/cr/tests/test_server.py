import cherrypy
from cherrypy.test import helper
from cr.api import server

def to_http_post_body(data):
    return '&'.join(['{}={}'.format(key, value) for key, value in data.iteritems()])



class SimpleCPTest(helper.CPWebCase):
    def setup_server():
        settings_filename = 'settings.json'
        cherrypy.tree.mount(server.Root(settings_filename), config=server.cherrypy_server_config)

    setup_server = staticmethod(setup_server)

    def test_login_route(self):
        self.getPage("/login")
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'text/html;charset=utf-8')

    def test_not_logged_in(self):
        self.getPage("/login", method="POST", body=to_http_post_body({
            'email': 'incorrect_email',
            'password': 'incorrect_password'
        }))
        self.assertStatus('403 Forbidden')

        self.getPage("/users")
        self.assertStatus('403 Forbidden')

    def test_logging_in(self):
        self.getPage("/login", method="POST", body=to_http_post_body({
            'email': 'admin@crunch.io',
            'password': '123456'
        }))
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'text/html;charset=utf-8')

        self.getPage("/users")

        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'text/html;charset=utf-8')

