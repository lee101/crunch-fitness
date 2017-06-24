import random
import string


def get_user():
    name = ''.join(random.choice(string.ascii_lowercase) for _ in xrange(5))
    return {
        "longitude": "-42.081022",
        "latitude": "43.175753",
        "email": "{}@example.com".format(name),
        "company": "test",
        "last_name": "testuser",
        "first_name": name,
        "password": '123456'
    }
