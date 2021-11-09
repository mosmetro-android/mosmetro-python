from typing import Dict, List, Any, Type

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
