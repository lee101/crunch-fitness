# coding=utf-8
import random
import string


def get_user(name=None):
    if not name:
        name = ''.join(random.choice(string.ascii_lowercase) for _ in xrange(5))
    return {
        "longitude": "-42.081022",
        "latitude": "43.175753",
        "email": "{}@example.com".format(name),
        "company": "test",
        "last_name": "testuser",
        "first_name": name,
        "password": '12345678910'
    }


def get_unicode_char_user():
    return get_user(u'¿unicode_person')


def get_special_char_user():
    return get_user(u' ¿!@#$%^&*()')
