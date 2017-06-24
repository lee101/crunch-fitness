import os, binascii

def get_random_token():
    return binascii.b2a_hex(os.urandom(16))
