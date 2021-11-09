from requests import Response
from .base import Provider
from .mosmetro import *
from ..utils import all_subclasses


def match(response: Response) -> Provider:
    for subcls in all_subclasses(Provider):
        try:
            if subcls.match(response):
                print(f'Detected provider: {subcls.__name__}')
                return subcls(response)
        except Exception:
            pass

    raise Exception('Provider not recognized')
