"""
    This is a client rest for openfire
"""
import requests
from django.confg import settings


class Openfire:
    def __init__(self):
        self.key = settings.OPENFIRE_AUTH = "YWRtaW46djIxMTQ2MDIzLg=="


