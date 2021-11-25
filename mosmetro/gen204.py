import random
from typing import List
from requests import Response, RequestException
from requests.exceptions import SSLError
from .session import session as s


class Gen204Res:
    def __init__(self, response: Response = None, false_negative: Response = None):
        self.response = response
        self.false_negative = false_negative

    @property
    def is_connected(self) -> bool:
        if not self.response:
            return False

        return self.response.status_code == 204


class Gen204:
    URL_DEFAULT = [
        'connectivitycheck.gstatic.com/generate_204',
        'www.gstatic.com/generate_204',
        'connectivitycheck.android.com/generate_204',
        'play.googleapis.com/generate_204',
        'clients1.google.com/generate_204'
    ]

    URL_RELIABLE = [
        'www.google.ru/generate_204',
        'www.google.ru/gen_204',
        'google.com/generate_204',
        'gstatic.com/generate_204',
        'maps.google.com/generate_204',
        'mt0.google.com/generate_204',
        'mt1.google.com/generate_204',
        'mt2.google.com/generate_204',
        'mt3.google.com/generate_204',
        'www.google.com/generate_204',
    ]

    @staticmethod
    def request(schema: str, urls: List[str]) -> Response:
        res = None
        last_ex = None

        for base_url in random.choices(urls, k=3):
            url = f'{schema}://{base_url}'

            try:
                res = s.get(url, allow_redirects=False)
                last_ex = None
                print(f'Gen204 | {url} | {res.status_code}')
                break
            except SSLError as ex:
                print(f'Gen204 | {url} | {ex}')
                last_ex = ex
                break
            except RequestException as ex:
                print(f'Gen204 | {url} | {ex}')
                last_ex = ex

        if last_ex:
            raise last_ex

        return res

    @staticmethod
    def check() -> Gen204Res:
        """Returns gen204 response and false negative (if exists)."""
        # Unreliable HTTP check (needs to be verified by HTTPS)
        try:
            unrel = Gen204.request("http", Gen204.URL_DEFAULT)
        except RequestException:
            # network is most probably unreachable
            return Gen204Res()

        # Reliable HTTPS check
        try:
            rel_https = Gen204.request("https", Gen204.URL_RELIABLE)
        except RequestException:
            rel_https = None

        if unrel.status_code == 204:
            if not rel_https or rel_https.status_code != 204:
                # Reliable HTTP check
                try:
                    rel_http = Gen204.request("http", Gen204.URL_RELIABLE)
                except RequestException:
                    rel_http = None

                if rel_http and rel_http.status_code != 204:
                    return Gen204Res(rel_http)  # false positive
            else:
                return Gen204Res(rel_https)  # confirmed positive
        else:
            if not rel_https:
                return Gen204Res(unrel)  # confirmed negative
            elif rel_https.status_code == 204:
                return Gen204Res(rel_https, unrel)  # false negative

        print('Gen204 | Unexpected state')
        return Gen204Res()


if __name__ == '__main__':
    res_204 = Gen204.check()
    print(f'Connected: {res_204.is_connected}')
    print(f'False negative: {res_204.false_negative is not None}')
