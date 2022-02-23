__ALL__ = ['AuthWifiRu', 'AuthWifiRuMsk', 'AuthWifiRuSpb']


from furl import furl
from requests import Response
from .base import Provider, Result, Redirect
from ..session import session as s
from ..utils import any_redirect, merge_urls, safeget


class AuthWifiRu(Provider):
    @staticmethod
    def match(response: Response):
        url = furl(any_redirect(response))
        return url.host == 'auth.wi-fi.ru' and url.path == '/auth'


class AuthWifiRuMsk(Provider):
    PATHS = {
        'start': '/gapi/auth/start',
        'init': '/gapi/auth/init',
        'check': '/gapi/auth/check'
    }

    @staticmethod
    def match(response: Response):
        url = furl(any_redirect(response))
        return url.host == 'auth.wi-fi.ru' and url.path in ['', '/', '/new']

    def run(self) -> Result:
        url = furl(any_redirect(self.response))

        segment = url.args.get('segment') or 'metro'
        # client_mac has higher priority
        mac = url.args.get('client_mac') or url.args.get('mac')

        # Follow first redirect
        print('Opening auth page')
        res = s.get(url)
        s.headers['referer'] = str(url)

        # Get auth page
        print('Starting session')
        url.args.clear()
        url.args['segment'] = segment
        if mac:
            url.args['clientMac'] = mac
        url.path = self.PATHS['start']
        res = s.get(url)

        after_auth = safeget(res.json(), 'data', 'segmentParams', 'common',
                             'redirectUrl', 'afterAuth')
        if after_auth:
            print(f'Post-auth redirect: {after_auth}')
            after_auth = merge_urls(self.response.request.url, after_auth)

        # Send login form
        print('Initializing connection')
        url.path = self.PATHS['init']
        url.args.clear()
        res = s.post(url, data={'mode': 0, 'segment': segment})
        res_data = res.json()
        print(res_data)

        error_code = safeget(res_data, 'auth_error_code', default='')
        if error_code.startswith('err_device_not_identified'):
            print('Error: Device is not registered. Please go to https://wi-fi.ru')
            return Result(False)

        # Checking auth state
        print('Checking connection')
        url.path = self.PATHS['check']
        res = s.get(url)
        res_data = res.json()
        print(res_data)

        if after_auth:
            return Redirect(after_auth)
        else:
            return Result(True)


class AuthWifiRuSpb(AuthWifiRuMsk):
    PATHS = {
        'start': '/spb/gapi/auth/start',
        'init': '/spb/gapi/auth/init',
        'check': '/spb/gapi/auth/check'
    }

    @staticmethod
    def match(response: Response):
        url = furl(any_redirect(response))
        return url.host == 'auth.wi-fi.ru' and url.path == '/spb/'
