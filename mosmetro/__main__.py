import sys
from datetime import datetime

from .providers import match as match_provider
from .gen204 import Gen204


def main(args=None):
    print(datetime.now())

    res204 = Gen204.check()

    if res204.is_connected:
        print('Already connected')
        sys.exit(0)

    provider = match_provider(res204.response)

    if provider.run() and Gen204.check().is_connected:
        print("Connected successfully! :3")
        sys.exit(0)
    else:
        print("Connection failed :(")
        sys.exit(1)


if __name__ == '__main__':
    main()
