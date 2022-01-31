import sys
from datetime import datetime

from . import __version__
from .gen204 import Gen204
from .providers import Provider
from .utils import all_subclasses
from .connect import connect


def main():
    print(datetime.now())
    print(f'Version: {__version__}')

    print('Loaded providers: ' +
          ', '.join(p.__name__ for p in all_subclasses(Provider)))

    print('Checking connection...')
    res204 = Gen204.check()

    if res204.is_connected:
        print('Already connected')
        sys.exit(0)

    if connect(res204.response):
        print("Connected successfully! :3")
        sys.exit(0)
    else:
        print("Connection failed :(")
        sys.exit(1)


if __name__ == '__main__':
    main()
