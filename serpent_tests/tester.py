'''A small module for testing Serpent code.'''
import warnings; warnings.simplefilter('ignore')
from ethereum import tester as t
from ethereum.utils import coerce_to_int
from colorama import Fore, Style, init; init()
import sys

passed = Fore.GREEN + 'passed' + Style.RESET_ALL + ';'
failed = Style.BRIGHT + Fore.RED + 'failed' + Style.RESET_ALL + ';'


class Account(object):
    def __init__(self, rawaddr, privkey):
        self.hexaddr = rawaddr.encode('hex')
        self.privkey = self.private_key = privkey
        self.address = rawaddr
        self.address_as_int = coerce_to_int(rawaddr)

    def __str__(self):
        return "<account: 0x{}>".format(self.hexaddr)

    def __repr__(self):
        return "Account({}, {})".format(self.rawaddr, self.privkey)


class Tester(object):
    state = t.state()
    accounts = map(Account, t.accounts, t.keys)
    def __init__(self, code, global_state=False):
        self.code = code
        if not global_state:
            self.state = t.state()
        self.contract = self.state.abi_contract(self.code)
        for name, obj in vars(self.contract).items():
            if getattr(obj, '__name__', '') == 'kall':
                obj.__name__ = str(name)
        
    def run_tests(self, test_cases):
        '''Runs a list of test cases.

        A test case is simple a 4-tuple with the following format:
            
            (name: str, args: tuple, kwds: dict, expected: object)

        where "name" is the name of the function you want to test,
        "args" is a tuple of arguments to pass to the function,
        "kwds" is a dict of keywords to use, useful for changing the
        sending address, and "expected" is the expected result of
        calling the function.'''
        for i, case in enumerate(test_cases):
            try:
                name, args, kwds, expected = case
            except Exception as exc:
                print "malformed test case!"
                print "  test number:", i
                print "  test case", case
                print
                print "See documentation for Tester.run_tests."
                sys.exit(1)

            sys.stdout.write('testing {}: '.format(name))
            sys.stdout.flush()
            if not hasattr(self.contract, name):
                print failed
                print '  invalid function name in test {}.'.format(i)
                print name
                sys.exit(1)

            func = getattr(self.contract, name)

            try:
                result = func(*args, **kwds)
            except Exception as exc:
                print failed
                print '  caught unknown exception during test {}'.format(i)
                print '  test case:', case
                print '  exception:', type(exc), exc
                sys.exit(1)

            if result == expected:
                print passed
            else:
                print failed
                print 'got unexpected result!'
                print '  result:', result
                print '  expected:', expected
                print '  test case number:', i
                print '  test case:', case
                sys.exit(1)
