#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import inspect
import sys
from datetime import datetime

if sys.version_info > (3, 0):
    from urllib.parse import urlparse, urljoin, parse_qs
else:
    from urlparse import urlparse, urljoin, parse_qs

import requests
from pyquery import PyQuery

try:
    from fake_useragent import UserAgent
except ImportError:
    UserAgent = None
    pass


ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


class Provider(object):
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
            return True

        for provider in Provider.__subclasses__():
            if (provider.match(r)):
                print("Detected provider: " + provider.__name__)
                return provider(session, r);

        print("Wrong network")
        return False

class MosMetroV2(Provider):
    def __init__(self, session, response):
        super(MosMetroV2, self).__init__(session)
        self.response = response

    def connect(self):
        print("Parsing initial redirect")
        redirect = urlparse(self.response.headers.get("Location"))

        if "segment" in redirect.query:
            segment = parse_qs(redirect.query)["segment"][0]
        else:
            segment = "metro"

        # Check if device is not registered
        if "identification" in redirect.path:
            print("Registration is required. Please go to " + redirect.geturl())
            return False

        print("Following initial redirect")
        r = session.get(redirect.geturl(), allow_redirects=False)

        if r.status_code in (301, 302) and "auto_auth" in r.headers.get("Location"):
            print("You probably have been temporary banned.")
            return False

        print("Following JavaScript redirect")
        r = session.get(urljoin(redirect.geturl(), "/auth?segment=" + segment))

        # Parsing CSRF token
        csrf = PyQuery(r.content)("meta[name=csrf-token]").attr("content")
        session.headers["X-CSRF-Token"] = csrf

        # Setting additional Cookies (probably required)
        requests.Session().cookies.set("afVideoPassed", "0")

        print("Sending auth request")
        r = session.get(urljoin(redirect.geturl(),
                                "/auth/init?mode=0&segment=" + segment))

        print("Checking internet connection")
        return Provider.generate_204(session) is True

    @staticmethod
    def match(response):
        if response.status_code not in (301, 302):
            return False

        redirect = response.headers.get("Location")

        return ".wi-fi.ru" in redirect and "login.wi-fi.ru" not in redirect

def main(args=None):
    print(datetime.now())

    with requests.Session() as session:
        if UserAgent:
            session.headers['User-Agent'] = UserAgent(
                path=ROOT + "/res/user-agent.json"
            ).random
        else:
            print("Random User-Agent disabled. Please install 'fake-useragent'.")

        p = Provider.find(session)

        if p is True or p is False:
            sys.exit(p)

        if p.connect():
            print("Connected successfully! :3")
            sys.exit(0)
        else:
            print("Connection failed :(")
            sys.exit(1)

if __name__ == '__main__':
    main()
