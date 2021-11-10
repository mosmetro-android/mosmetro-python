import sys
from datetime import datetime

from .providers import match as match_provider
from .gen204 import Gen204
from .utils import response_to_str


def main(args=None):
    print(datetime.now())

    print('Checking connection...')
    res204 = Gen204.check()

    if res204.is_connected:
        print('Already connected')
        sys.exit(0)

    try:
        provider = match_provider(res204.response)
    except Exception as ex:
        print('----')
        print(response_to_str(res204.response))
        print('----')
        print(ex)
        sys.exit(1)

    if provider.run():
        print("Connected successfully! :3")
        sys.exit(0)
    else:
        print("Connection failed :(")
        sys.exit(1)


if __name__ == '__main__':
    main()
