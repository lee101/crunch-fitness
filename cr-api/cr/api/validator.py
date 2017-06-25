import re
import unicodedata


def contains_only_letters(text):
    if type(text) == str:
        unicode_text = unicode(text, "utf-8")
    else:
        unicode_text = text
    return all(unicodedata.category(ch)[0] == "L" for ch in unicode_text)


def contains_control_characters(text):
    if type(text) == str:
        unicode_text = unicode(text, "utf-8")
    else:
        unicode_text = text
    return any(unicodedata.category(ch)[0] == "C" for ch in unicode_text)


def validate_name(name):
    if contains_only_letters(name):
        return True, ''
    else:
        return False, 'Invalid: name must not contain special characters, only letters'


def validate_password(password):
    if 10 < len(password) < 256:
        return True, ''
    else:
        return False, 'Invalid password, must be between 10 and 256 characters'


def validate_company(company):
    if contains_control_characters(company):
        return False, 'Invalid company name, must have no control characters'

    if 1 < len(company) < 256:
        return True, ''
    else:
        return False, 'Invalid company name, must be between 1 and 256 characters and have no control characters'


def validate_email(email):
    if contains_control_characters(email):
        return False, 'Invalid email, must have no control characters'

    email_pattern = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if email_pattern.match(email):
        return True, ''
    else:
        return False, 'Invalid email'


def validate_latlng(lat, lng):
    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        return False, 'Invalid lat:{} lng:{}, must be a number'.format(lat, lng)
    if lat > 90 or lat < -90:
        return False, 'Invalid lat:{} lng:{}, lat must be between -90 and 90'.format(lat, lng)
    if lng > 180 or lng < -180:
        return False, 'Invalid lat:{} lng:{}, lng must be between -180 and 180'.format(lat, lng)
    return True, ''
