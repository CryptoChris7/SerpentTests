import os as _os
import keyword as _keyword
import re as _re
from typing import Dict

VALID_ID_P = _re.compile('[_a-zA-Z][_a-zA-Z0-9]*')


def is_valid_source_name(name: str) -> bool:
    """Checks a name to see if it is a valid Serpent source name."""
    return (
        name.endswith('.se') and
        VALID_ID_P.match(name.rsplit('.se', 1)[0]) and
        not _keyword.iskeyword(name)
    )


def sources_from_dir(path: str) -> Dict[str, str]:
    """Collects all the Serpent code into a dict."""
    path = _os.path.abspath(path)
    if _os.path.isfile(path):
        path = _os.path.dirname(path)
    assert _os.path.isdir(path), 'supplied dir is not a directory: {}'.format(path)

    source_map = {}
    for entry in _os.scandir(path):
        if entry.is_file() and is_valid_source_name(entry.name):
            source_map[entry.path] = open(entry.path).read()
        elif entry.is_dir():
            source_map.update(sources_from_dir(entry.path))

    return source_map


def path_to_name(path: str) -> str:
    """Extracts the module name of the Serpent code at path."""
    basename = _os.path.basename(path)
    if basename.endswith('.se'):
        return basename[:-3]
