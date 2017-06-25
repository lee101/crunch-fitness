# coding=utf-8
from cr.api import validator


def test_validate_latlng_valid():
    valid, message = validator.validate_latlng(90, 90.1)
    assert valid, message
    valid, message = validator.validate_latlng(-90, -90.1)
    assert valid, message
    valid, message = validator.validate_latlng(-90, -180)
    assert valid, message
    valid, message = validator.validate_latlng(90, 180)
    assert valid, message
    valid, message = validator.validate_latlng(89.123123123, 180)
    assert valid, message
    valid, message = validator.validate_latlng('89.123123123', '180')
    assert valid, message


def test_validate_latlng_invalid():
    valid, message = validator.validate_latlng(90.1, 90)
    assert not valid, message
    valid, message = validator.validate_latlng(-90.1, -90)
    assert not valid, message
    valid, message = validator.validate_latlng('89.123123123A', '180')
    assert not valid, message


def test_validate_password():
    valid, message = validator.validate_password('A' * 10)
    assert not valid, message
    valid, message = validator.validate_password('A' * 12)
    assert valid, message
    valid, message = validator.validate_password('A' * 9999)
    assert not valid, message


def test_validate_name():
    valid, message = validator.validate_name(u'¿')
    assert not valid, message
    valid, message = validator.validate_name(u'Řon')
    assert valid, message
    valid, message = validator.validate_name('A;')
    assert not valid, message
    valid, message = validator.validate_name('A\t')
    assert not valid, message


def test_validate_company():
    valid, message = validator.validate_company(u'¿Corp')
    assert valid, message
    valid, message = validator.validate_company(u'Řon')
    assert valid, message
    valid, message = validator.validate_company('A;')
    assert valid, message
    valid, message = validator.validate_company('A\t')
    assert not valid, message
    valid, message = validator.validate_name(u'\racme')
    assert not valid, message


def test_validate_email():
    valid, message = validator.validate_email(u'leepenkman@gmail.com')
    assert valid, message

    valid, message = validator.validate_email(u'test@example.com')
    assert valid, message

    valid, message = validator.validate_email(u'e@e.c')
    assert valid, message

    valid, message = validator.validate_email(u'Řon')
    assert not valid, message
    valid, message = validator.validate_email('A;')
    assert not valid, message
    valid, message = validator.validate_email('asdf@asdf@asdf.com')
    assert not valid, message
    valid, message = validator.validate_email(u'A@A.')
    assert not valid, message
