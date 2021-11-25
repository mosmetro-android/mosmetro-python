from requests import Response
from typing import Union
from .base import Provider
from .mosmetro import *
from ..utils import all_subclasses


def match(response: Response) -> Union[Provider, None]:
    for subcls in all_subclasses(Provider):
        try:
            if subcls.match(response):
                return subcls(response)
        except Exception:
            pass

    return None
