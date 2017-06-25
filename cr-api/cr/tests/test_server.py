import json

import cherrypy
from cherrypy.test import helper
from cr.api import server
import fake_data


def to_http_post_body(data):
    return '&'.join(['{}={}'.format(key, value) for key, value in data.iteritems()])


class SimpleCPTest(helper.CPWebCase):
    def setup_server():
        settings_filename = 'settings.json'
        cherrypy.tree.mount(server.Root(settings_filename), config=server.cherrypy_server_config)

    setup_server = staticmethod(setup_server)

    def getReturnedCookie(self):
        for name, value in self.headers:
            if name == 'Set-Cookie':
                return value[:value.find(';')]

    def test_index(self):
        self.getPage("/")
        self.assertStatus('200 OK', msg=self.body)

    def test_login_route(self):
        self.getPage("/login")
        self.assertStatus('200 OK', msg=self.body)

    def test_not_logged_in(self):
        self.getPage("/login", method="POST", body=to_http_post_body({
            'email': 'incorrect_email',
            'password': 'incorrect_password'
        }))
        self.assertStatus('403 Forbidden', msg=self.body)

        self.getPage("/users", headers=[('Cookie', self.getReturnedCookie())])
        self.assertStatus('403 Forbidden', msg=self.body)

    def test_logging_in(self):
        self.getPage("/login", method="POST", body=to_http_post_body({
            'email': 'admin@crunch.io',
            'password': '123456'
        }))
        self.assertStatus('200 OK', msg=self.body)

        self.getPage("/users", headers=[('Cookie', self.getReturnedCookie())])
        self.assertStatus('200 OK', msg=self.body)

    def test_logging_out(self):
        self.getPage("/login", method="POST", body=to_http_post_body({
            'email': 'admin@crunch.io',
            'password': '123456'
        }))
        self.assertStatus('200 OK', msg=self.body)

        cookie = self.getReturnedCookie()
        self.getPage("/users", headers=[('Cookie', cookie)])
        self.assertStatus('200 OK', msg=self.body)

        self.getPage("/logout", headers=[('Cookie', cookie)])

        self.assertTrue(self.status.startswith('30'))

        self.getPage("/users", headers=[('Cookie', cookie)])
        self.assertStatus('403 Forbidden', msg=self.body)

    def test_can_add_new_user(self):
        new_user = fake_data.get_user()

        self.getPage("/login", method="POST", body=to_http_post_body({
            'email': 'admin@crunch.io',
            'password': '123456'
        }))
        self.assertStatus('200 OK', msg=self.body)

        cookie = self.getReturnedCookie()
        self.getPage("/users", headers=[('Cookie', cookie)])
        self.assertStatus('200 OK', msg=self.body)
        results = json.loads(self.body)
        users = results['users']
        for user in users:
            self.assertNotEqual(user['email'], new_user['email'])

        self.getPage("/users", method="POST", headers=[('Cookie', cookie)],
                     body=to_http_post_body(new_user))
        self.assertStatus('200 OK', msg=self.body)

        self.getPage("/users", headers=[('Cookie', cookie)])
        self.assertStatus('200 OK', msg=self.body)
        results = json.loads(self.body)
        users = results['users']

        self.assertIn(new_user['email'], map(lambda user: user['email'], users))
