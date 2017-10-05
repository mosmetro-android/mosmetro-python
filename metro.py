#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
from datetime import datetime

import requests

class Provider():
    def __init__(self, session):
        self.session = session;

    @staticmethod
    def generate_204(session):
        r = session.get("http://google.com/generate_204",
                        allow_redirects=False)
        if r.status_code != 204:
            return r

        r = session.get("https://google.com/generate_204",
                        allow_redirects=False, verify=False)
        if r.status_code != 204:
            return r

        return True

    @staticmethod
    def find(session):
        r = Provider.generate_204(session)

        if r is True:
            print("Already connected")
            return


if __name__ == '__main__':
    print(datetime.now())

    with requests.Session() as session:
        p = Provider.find(session)

        if p is True:
            sys.exit(0)
