"""Serpent contract testing class."""
from .contract_test import ContractTest
from .utils import sources_from_dir
from ethereum.tester import TransactionFailed, ContractCreationFailed
import warnings as _w
_w.simplefilter('ignore')

__author__ = 'Chris Calderon'
__email__ = 'chris-da-dev@augur.net'
__version__ = '2.4'
__license__ = 'MIT'
