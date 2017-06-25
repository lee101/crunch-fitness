# coding=utf-8
from cr.api import data_accessor
import fake_data

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


