'''A small module for testing Serpent code, for use with py.test.'''
import sys
import os
import enum

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


Assert = enum.Enum("Asserts", "equal,unequal,lt,gt,le,ge")


class ContractTesterError(Exception): pass


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
        return "Account({!r}, {!r})".format(self.rawaddr, self.privkey)


Accounts = map(Account, t.accounts, t.keys)

class ContractTester(object):
    """A class for testing the results of Serpent contracts."""
    # TODO: replace pyethereum test state with geth or parity based testnet.

    global_state = t.state()
    expected_types = int, long, str, list, type(None)
    arg_types = int, long, str, list, tuple

    def __init__(self, code, global_state=False):
        self.code = code
        if not global_state:
            self.state = t.state()
        start_gas = self.state.block.gas_used
        self.contract = self.state.abi_contract(self.code)
        self.contractAccount = Account(self.contract.address, None)
        self.gas_cost = self.state.block.gas_used - start_gas
        
        # pyethereum's AbiContracts don't name their functions correctly >:(
        for name, obj in vars(self.contract).items():
            if getattr(obj, '__name__', '') == 'kall':
                obj.__name__ = str(name)

    def __getattr__(self, name):
        # wraps abi functions for easy testing
        contract_func = getattr(self.contract, name, None)
        if contract_func is None:
            err_msg = "No contract function with that name: {}"
            raise ContractTesterError(err_msg.format(name))

        def tester_func(**kwds):
            args = kwds.get('args', ())
            for arg in args:
                if not isinstance(arg, ContractTester.arg_types):
                    err_msg = "Invalid argument type, must be int, str, list, or tuple: <arg: {}>; <type: {}>"
                    raise ContractTesterError(err_msg.format(arg, type(arg)))

            expects = kwds.get('expects', None)
            if not isinstance(expects, ContractTester.expected_types):
                err_msg = "Invalid expected-value type, must be int, str, list, or tuple: <val: {}>; <type: {}>"
                raise ContractTesterError(err_msg.format(expects, type(expects)))        

            raises = kwds.get('raises', None)
            if raises is not None and not issubclass(Exception, raises):
                raise ContractTestError("'raises' argument must be a subclass of Exception")

            asserts = kwds.get('asserts', None)
            if asserts not in Assert:
                raise ContractTestError("Invalid value for 'asserts' keyword: {}".format(asserts))

            other_kwds = kwds.get('kwds', {})
            if not isinstance(other_kwds, dict):
                raise ContractTestError("'other_kwds' argument must be a dict.")

            try:
                result = contract_func(*args, **other_kwds)
            except Exception as exc:
                if not isinstance(exc, raises):
                    raise ContractTesterError("Unexpected exception: {}: {}".format(type(exc), exc))

            if asserts is Assert.equal:
                assert result == expects
            elif asserts is Assert.unequal:
                assert result != expects
            elif asserts is Assert.lt:
                assert result < expects
            elif asserts is Assert.le:
                assert result <= expects
            elif asserts is Assert.gt:
                assert result > expects
            elif asserts is Assert.ge:
                assert result >= expects
            else:
                raise ContractTesterError("black magic is afoot!")
                
        tester_func.__name__ = name
        tester_func.__doc__ = 'Wrapper for testing the {} function.'
        setattr(self, name, tester_func)
        return tester_func
