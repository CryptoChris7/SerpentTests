'''A small module for testing Serpent code, for use with py.test.'''
import sys
import os
import enum
import operator
from types import MethodType

# Stop the warning about python cache
# without disabling warnings system wide
old_io = sys.stdout, sys.stderr

with open(os.devnull, 'w') as fake_stdout:
    sys.stdout = fake_stdout
    sys.stderr = fake_stdout
    from ethereum import tester as t
    from ethereum.utils import coerce_to_int

sys.stdout, sys.stderr = old_io
del fake_stdout
del old_io


Assert = enum.Enum("Assert", "eq,ne,lt,gt,le,ge")
compare_ops = {
    Assert.eq: operator.eq,
    Assert.ne: operator.ne,
    Assert.lt: operator.lt,
    Assert.gt: operator.gt,
    Assert.le: operator.le,
    Assert.ge: operator.ge,
}


class ContractTestError(Exception): pass


class Account(object):
    """A class for easily dealing with accounts in ethereum.tester."""
    def __init__(self, rawaddr, privkey):
        self.hexaddr = rawaddr.encode('hex')
        self.privkey = self.private_key = privkey
        self.address = rawaddr
        self.as_int = coerce_to_int(rawaddr)

    def __str__(self):
        return "<account: 0x{}>".format(self.hexaddr)

    def __repr__(self):
        return "Account(rawaddr={!r}, privkey={!r})".format(self.address, self.privkey)


Accounts = map(Account, t.accounts, t.keys)


def tester(func, name):
    """A wrapper function for testing serpent functions in an AbiContract."""

    def test_func(args=(), kwds={}, asserts=Assert.eq, compare=None):
        """Test function {!r}.

        Keyword Arguments:
        args -- a tuple or list of arguments to pass to the function.
        kwds -- a dict of keywords to pass to the function.
        asserts -- a member of the Assert enum that specifies the comparison to make.
        expects -- a value to compare against the result of the function call.
        """
        for arg in args:
            if not isinstance(arg, ContractTest.arg_types):
                err_msg = "Invalid argument type, must be int, long, str, list, or tuple: <arg: {}>; <type: {}>"
                raise ContractTestError(err_msg.format(arg, type(arg)))

        if not isinstance(kwds, dict):
            raise ContractTestError("'kwds' argument must be a dict.")

        if asserts not in Assert:
            raise ContractTestError("Invalid value for 'asserts' keyword: {}".format(asserts))

        if not isinstance(compare, ContractTest.allowed_types):
            err_msg = "Invalid type for 'compare', must be int, str, list, or tuple: {!r}"
            raise ContractTestError(err_msg.format(compare))

        result = func(*args, **kwds)
        comparison = compare_ops[asserts]
        assert comparison(result, compare)

    test_func.__name__ = name
    test_func.__doc__ = test_func.__doc__.format(name)
    return test_func



class ContractTest(object):
    """A class for testing the results of Serpent contracts."""
    # TODO: replace pyethereum test state with geth or parity based testnet.

    global_state = t.state()
    allowed_types = int, long, str, list, type(None)
    arg_types = int, long, str, list, tuple

    def __init__(self, code, global_state=False):
        self.code = code
        if not global_state:
            self.state = t.state()
        start_gas = self.state.block.gas_used
        self.contract = self.state.abi_contract(self.code)
        self.contractAccount = Account(self.contract.address, None)
        self.gas_cost = self.state.block.gas_used - start_gas
        
        for name, obj in vars(self.contract).items():
            if isinstance(obj, MethodType) and obj.__func__.__name__ == 'kall':
                setattr(self, name, tester(obj, name))
