from collections import OrderedDict
from serpent_tests.utils import path_to_name
from typing import List, Tuple, T, Callable
import ethereum.utils
import rlp
import re
import serpent
import binascii
import json
import os

Pred = Callable[[T], bool]
IMPORT = re.compile('^import (.+) as (.+)$', re.MULTILINE)
INSET = re.compile('^inset\(\'(\w+\.sem)\'\)$', re.MULTILINE)


def lookup_inset(path: str, _dict={}) -> str:
    """Returns the code of a serpent macro file."""
    if path not in _dict:
        with open(path) as code:
            _dict[path] = code.read()
    return _dict[path]


def group(n: int, lst: List[T]) -> List[List[T]]:
    """Groups a list into lists of length n."""
    groups = []
    for i in range(0, len(lst), n):
        groups.append(lst[i:i+n])
    return groups


def partition(pred: Pred, lst: List[T]) -> Tuple[List[T], List[T]]:
    """Partitions a list into two lists based on the result of pred."""
    yes, no = [], []
    for elem in lst:
        if pred(elem):
            yes.append(elem)
        else:
            no.append(elem)
    return yes, no


class SourceInfo:
    _address: bytes = None
    _pure_source: str = None
    _compilable_source: str = None
    _serpent_signature: str = None
    _abi_signature: str = None
    _dependencies: List[Tuple[str, str]] = None
    instance_map = OrderedDict()

    def __init__(
            self, *,
            path: str, impure_source: str,
            creator: bytes, nonce: int):
        self.path = os.path.abspath(path)
        self.impure_source = impure_source
        self.creator = creator
        self.nonce = nonce
        self.name = path_to_name(self.path)
        SourceInfo.instance_map[self.name] = self

    def __repr__(self):
        param_dict = {
            'name': self.name,
            'impure_source': self.impure_source,
            'creator': self.creator,
            'nonce': self.nonce,
            'path': self.path
        }
        return 'SourceInfo(**{})'.format(json.dumps(param_dict, indent=4))

    def __str__(self):
        return '<contract {} w/ address {}>'.format(self.name, self.address)

    @staticmethod
    def _is_dep(e: str) -> bool:
        return '\n' not in e and e

    def _parse_impure_source(self):
        deps, src_chunks = partition(self._is_dep,
                                     IMPORT.split(self.impure_source))
        self._dependencies = group(2, deps)
        self._pure_source = ''.join(filter(None, src_chunks))
        self._pure_source = INSET.sub(
            lambda match: lookup_inset(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(self.path),
                        match.group(1)
                    )
                )
            ),
            self._pure_source
        )

    @property
    def pure_source(self):
        if self._pure_source is None:
            self._parse_impure_source()
        return self._pure_source

    @property
    def serpent_signature(self):
        if self._serpent_signature is None:
            self._serpent_signature = (
                serpent.mk_signature(self.pure_source)
                .decode()
                .replace(' main: ', ' {}: '.format(self.name))
            )
        return self._serpent_signature

    @property
    def abi_signature(self):
        if self._abi_signature is None:
            self._abi_signature = (
                serpent.mk_full_signature(self.pure_source)
                .decode()
            )
        return self._abi_signature

    @property
    def address(self):
        if self._address is None:
            self._address = binascii.hexlify(
                ethereum.utils.sha3_256(
                    rlp.encode([
                        self.creator,
                        self.nonce
                    ])
                )
            ).decode()
        return self._address

    @property
    def dependencies(self):
        if self._dependencies is None:
            self._parse_impure_source()
        return self._dependencies

    @property
    def compilable_source(self):
        if self._compilable_source is None:
            externs = []
            for name_alias in self.dependencies:
                name, alias = name_alias
                info = SourceInfo.instance_map[name]
                addr_macro = 'macro {}: 0x{}'.format(alias, info.address)
                externs.append(info.serpent_signature)
                externs.append(addr_macro)
            self._compilable_source = '\n'.join(externs) + self.pure_source
        return self._compilable_source
