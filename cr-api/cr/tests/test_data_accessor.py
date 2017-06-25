# coding=utf-8
import fake_data
from cr.api import data_accessor

accessor = data_accessor.DataAccessor('settings.json')


def test_get_users():
    users = accessor.get_all_users()
    admin_user = accessor.get_user('admin@crunch.io')
    assert admin_user['email'] in map(lambda u: u['email'], users)


def test_add_user():
    new_user = fake_data.get_user()

    accessor.add_user(new_user)
    expected_user = accessor.get_user(new_user['email'])

    assert new_user['email'] == expected_user['email']


def test_get_distances():
    users = list(accessor.get_all_users())
    distances = list(accessor.get_all_distances())

    assert len(distances) == (len(users) * (len(users) - 1)) / 2
