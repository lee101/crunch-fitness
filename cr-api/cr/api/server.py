import hashlib
from functools import wraps

import cherrypy
import json
import sys
from data_accessor import DataAccessor
import utils

session_key = 'cr-api-user'


class Root(object):
    def __init__(self, settings_filename):
        self.data_accessor = DataAccessor(settings_filename)

    def error_401(self):
        cherrypy.response.status = 401
        return '401 Unauthorized'

    def error_403(self):
        cherrypy.response.status = 403
        return '403 Forbidden'

    def authenticated(func):
        @wraps(func)
        def authenticated_func(self, *args, **kwargs):

            if 'email' in cherrypy.request and 'password' in cherrypy.request:
                email = cherrypy.request.email
                password = cherrypy.request.password
                self.current_user = self.data_accessor.get_user(email)
                hash = hashlib.sha1(password).hexdigest()
                if self.current_user and self.current_user['hash'] == hash:
                    cherrypy.session[session_key] = self.current_user
                    return func(*args, **kwargs)
                else:
                    return self.error_403()
            else:
                self.current_user = cherrypy.session[session_key]
                if self.current_user:
                    return func(*args, **kwargs)
                else:
                    return self.error_403()  # redirect to login page?

        return authenticated_func

    def index(self):
        return 'Welcome to Crunch.  Please <a href="/login">login</a>.'

    index.exposed = True

    @authenticated
    def users(self):
        """
        for GET: update this to return a json stream defining a listing of the users
        for POST: should add a new user to the users collection, with validation

        Only logged-in users should be able to connect.  If not logged in, should return the
        appropriate HTTP response.  Password information should not be revealed.

        note: Always return the appropriate response for the action requested.
        """

        if cherrypy.request.method == 'GET':
            return json.dumps({'users': [u for u in self.data_accessor.get()]})

    users.exposed = True

    @authenticated
    def auth_login(self):
        return 'success'

    def login(self, email=None, password=None):
        """
        a GET to this endpoint should provide the user login/logout capabilities

        a POST to this endpoint with credentials should set up persistence tokens for the user,
        allowing them to access other pages.

        hint: this is how the admin's password was generated:
              import hashlib; hashlib.sha1('123456').hexdigest()
        """
        if cherrypy.request.method == 'POST':
            self.current_user = self.data_accessor.get_user(email)
            hash = hashlib.sha1(password).hexdigest()
            if self.current_user and self.current_user['hash'] == hash:
                cherrypy.session[session_key] = self.current_user
                return 'worked'
            else:
                return self.error_403()
        if cherrypy.request.method == 'GET':
            return """
                <form class="form-horizontal" action="" method="POST">
                  <fieldset>
                    <div id="legend">
                      <legend class="">Login</legend>
                    </div>
                    <div class="control-group">
                      <label class="control-label" for="email">Email</label>
                      <div class="controls">
                        <input type="text" id="email" name="email" placeholder="" class="input-xlarge">
                      </div>
                    </div>
                    <div class="control-group">
                      <label class="control-label" for="password">Password</label>
                      <div class="controls">
                        <input type="password" id="password" name="password" placeholder="" class="input-xlarge">
                      </div>
                    </div>
                    <div class="control-group">
                      <div class="controls">
                        <input type="submit" class="btn btn-success">Login</input>
                      </div>
                    </div>
                  </fieldset>
                </form>
            """

    login.exposed = True

    def logout(self):
        """
        Should log the user out, rendering them incapable of accessing the users endpoint, and it
        should redirect the user to the login page.
        """

    def distances(self):
        """
        Each user has a lat/lon associated with them.  Using only numpy, determine the distance
        between each user pair, and provide the min/max/average/std as a json response.
        This should be GET only.

        Don't code, but explain how would you scale this to 1,000,000 users, considering users
        changing position every few minutes?
        """


def run():
    settings_filename = sys.argv[1] or 'settings.json'

    config = {'tools.sessions.on': True}
    cherrypy.quickstart(Root(settings_filename), config={'/': config})


if __name__ == "__main__":
    run()
