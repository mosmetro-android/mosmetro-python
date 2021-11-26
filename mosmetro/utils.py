import re
from bs4.element import Tag
from furl import furl, Path
from requests import Response
from bs4 import BeautifulSoup as BS
from typing import Dict, List, Any, Type, Union


def safeget(data: Dict[Any, Any], *keys, default: Any = None) -> Any:
    """Recursively and safely get a value from nested dictionaries."""
    if not data:
        return None

    res = data

    for key in keys:
        if key in res:
            res = res[key]
        else:
            return default

    return res


def all_subclasses(cls) -> List[Type]:
    """Find all subclasses recursively."""
    res = list()

    for subcls in cls.__subclasses__():
        res.append(subcls)
        res.extend(all_subclasses(subcls))

    return res


def response_to_str(res: Response) -> str:
    return '\n'.join([
        f'{res.status_code} {res.reason}',
        '\n'.join(f'{name}: {value}' for name, value in res.headers.items()),
        '',
        res.text
    ])


def merge_urls(base: Union[str, None], url: Union[str, None]) -> str:
    u1 = furl(base)
    u2 = furl(url)

    if u2.path and not u2.path.isabsolute:
        if u1.path == '':
            raise ValueError('Not enough information to reconstruct URL')

        u2.path = Path(u1.path).add(u2.path)

    if not u2.host:
        if not u1.host:
            raise ValueError('Not enough information to reconstruct URL')

        u2.host = u1.host

    if not u2.scheme:
        if not u1.scheme:
            u1.scheme = 'http'

        u2.scheme = u1.scheme

    return u2.url


PATTERN_META_REDIR = re.compile('^[0-9]+[;,] ?(URL=|url=)?[\'"]?(.*?)[\'"]?$')


def meta_redirect(res: Response) -> Union[str, None]:
    soup = BS(res.content, features="html.parser")
    tag = soup.find('meta', attrs={'http-equiv': re.compile('refresh', re.I)})

    if not tag or not isinstance(tag, Tag):
        return None

    content = tag.attrs['content']
    match = PATTERN_META_REDIR.fullmatch(content)

    if not match:
        return None

    return merge_urls(res.request.url, match.group(2))


def any_redirect(res: Response) -> Union[str, None]:
    """Extract 3xx or meta redirect from Response."""
    if 'location' in res.headers:
        return merge_urls(res.request.url, res.headers['location'])

    return meta_redirect(res)
