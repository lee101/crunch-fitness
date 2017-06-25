import json

from datetime import datetime

from cr.db.store import global_settings as settings, connect


class DataAccessor(object):
    def __init__(self, settings_filename):
        settings.update(json.load(file(settings_filename)))
        self.db = connect(settings)

    def get_all_users(self):
        return self.db.users.find()

    def get_user(self, email):
        return self.db.users.find_one({'email': email})

    def add_user(self, user):
        registered = datetime.now()
        user['registered'] = registered
        return self.db.users.insert_one(user)
