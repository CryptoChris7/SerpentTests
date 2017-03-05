"""Serpent contract testing class."""
import ethereum.tester
import attr
import binascii
import unittest
import collections
from types import MethodType
from typing import List

__author__ = 'Chris Calderon'
__email__ = 'chris-da-dev@augur.net'
__version__ = '3.1.1'
__license__ = 'MIT'

GLOBAL_STATE = ethereum.tester.state()


@attr.s
class Account:
    raw_address = attr.ib(
        validator=attr.validators.instance_of(bytes)
    )
    private_key = attr.ib(
        validator=attr.validators.instance_of(bytes)
    )

    @property
    def address(self) -> bytes:
        return binascii.hexlify(self.raw_address)

default_accounts = list(
    map(
        Account,
        ethereum.tester.accounts,
        ethereum.tester.keys
    )
)


class ContractTestMeta(type):
    """Metaclass for ContractTest which ensures tests are run in order."""
    @classmethod
    def __prepare__(mcs, name, bases, **kwds):
        result = collections.OrderedDict()
        if kwds.get('globalState', False):
            result['state'] = GLOBAL_STATE
        else:
            result['state'] = ethereum.tester.state()
        return result

    def __new__(mcs, name, bases, cls_dict):
        test_order = []
        for name in cls_dict:
            if name.startswith('test_') and callable(cls_dict[name]):
                test_order.append(name)
        cls_dict['__test_order__'] = test_order
        return super().__new__(mcs, name, bases, cls_dict)


class ContractTestLoader(unittest.TestLoader):
    def getTestCaseNames(self, test_case_class: 'ContractTest'):
        try:
            return test_case_class.__test_order__
        except AttributeError:
            return super().getTestCaseNames(test_case_class)


def run_tests(warnings='ignore'):
    loader = ContractTestLoader()
    unittest.main(testLoader=loader, warnings=warnings, verbosity=2)


class ContractTest(unittest.TestCase, metaclass=ContractTestMeta):
    __test_order__: List[str]
    creator: Account = default_accounts[0]
    source: str
    state: ethereum.tester.state
    contract: ethereum.tester.ABIContract
    address: str

    @classmethod
    def setUpClass(cls):
        cls.contract = cls.state.abi_contract(
            cls.source,
            sender=cls.creator.private_key
        )
        cls.address = cls.contract.address

        # renames functions so they make more sense in errors
        for name, obj in vars(cls.contract).items():
            if isinstance(obj, MethodType):
                if obj.__func__.__name__ == 'kall':
                    obj.__func__.__name__ = name

    def setUp(self):
        # avoids hitting block gas limit
        self.state.mine()
