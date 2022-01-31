from requests.models import Response

from .providers import match as match_provider
from .providers.base import Redirect
from .gen204 import Gen204
from .utils import any_redirect, response_to_str
from .session import session as s


def connect(res: Response) -> bool:
    while True:
        provider = match_provider(res)

        if not provider:
            redirect = any_redirect(res)

            if redirect:
                print(f'Following unknown redirect: {redirect}')
                res = s.get(redirect, allow_redirects=False)
                continue
            else:
                print('----')
                print(response_to_str(res))
                print('----')
                print('No more redirects')
                break

        print(f'Provider: {provider.__class__.__name__}')
        result = provider.run()

        if isinstance(result, Redirect):
            print(f'Following post-auth redirect: {result.url}')
            res = s.get(result.url, allow_redirects=False)
            continue

        if not result.success:
            return False

        break

    print('Checking connection...')
    return Gen204.check().is_connected
