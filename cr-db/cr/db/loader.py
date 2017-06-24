import os
import json
import sys

from cr.db.store import global_settings, connect

users_filename = os.path.join(os.path.dirname(__file__), 'users.json')

def load_data(settings=None, clear=None):
    if settings is None:
        settings = global_settings
        global_settings.update(json.load(file('settings.json')))

    db = connect(settings)


    if clear:
        db.users.remove()

    with file(users_filename) as users_file:
        users = json.load(users_file)
        for user in users:
            db.users.insert(user)


