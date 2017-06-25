import json

from datetime import datetime
from itertools import combinations

import numpy as np
from geopy.distance import vincenty

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

    def get_all_distances(self):
        users = self.get_all_users()
        user_pairs = combinations(users, r=2)
        distances = (self.get_distance(user1, user2)
                     for (user1, user2) in user_pairs)
        return np.fromiter(distances, np.float)

    def get_distance(self, user1, user2):
        return vincenty((float(user1['latitude']), float(user1['longitude'])),
                        (float(user2['latitude']), float(user2['longitude']))).kilometers
