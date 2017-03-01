"""Serpent contract testing class."""
import ethereum.tester
import attr
import binascii
import unittest
from types import MethodType

__author__ = 'Chris Calderon'
__email__ = 'chris-da-dev@augur.net'
__version__ = '3.0.0'
__license__ = 'MIT'


@attr.s
class Account:
    raw_address = attr.ib(
        validator=attr.validators.instance_of(bytes)
    )
    private_key = attr.ib(
        validator=attr.validators.instance_of(bytes)
    )

    @property
    def address(self):
        return binascii.hexlify(self.raw_address).decode()

default_accounts = list(
    map(
        Account,
        ethereum.tester.accounts,
        ethereum.tester.keys
    )
)

ETHEREUM_STATE = ethereum.tester.state()


def run_tests(warnings='ignore'):
    unittest.main(warnings=warnings)


class ContractTest(unittest.TestCase):
    creator: Account = default_accounts[0]
    source: str = None

    @classmethod
    def setUpClass(cls):
        cls.contract = ETHEREUM_STATE.abi_contract(
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
        ETHEREUM_STATE.mine()
