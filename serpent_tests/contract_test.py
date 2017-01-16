from serpent_tests.source_info import SourceInfo
from typing import Dict
from collections import OrderedDict
import ethereum.tester
import unittest


class ContractTest(unittest.TestCase):
    source_map: Dict[str, str] = None
    source_info_map: Dict[str, SourceInfo] = None

    @classmethod
    def setUpClass(cls):

        cls.state = ethereum.tester.state()
        cls.creator_private_key = ethereum.tester.k0

        cls.creator_address = ethereum.tester.a0
        start_nonce = cls.state.block.get_nonce(cls.creator_address)

        cls.source_info_map = OrderedDict()
        for i, path in enumerate(cls.source_map):
            source = cls.source_map[path]
            cls.source_info_map[path] = SourceInfo(
                path=path,
                impure_source=source,
                creator=cls.creator_address,
                nonce=(start_nonce + i)
            )

        for source in cls.source_info_map.values():
            setattr(
                cls,
                source.name,
                cls.state.abi_contract(
                    source.compilable_source,
                    sender=cls.creator_private_key
                )
            )

    def setUp(self):
        # avoids hitting block gas limit
        self.state.mine(coinbase=self.creator_address)

    @staticmethod
    def run_tests():
        unittest.main()
