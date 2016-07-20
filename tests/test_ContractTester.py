from serpent_tests import ContractTest, Assert, ACCOUNTS, ContractTestError
import pytest

CODE = '''\
def foo():
    return(text("foo"):str)

def double(x):
    return(x*2)

def echo_sender():
    return(msg.sender)'''


def test_ContractTest():
        a0 = ACCOUNTS[0]
        a1 = ACCOUNTS[1]
        test = ContractTest(CODE)
        test.foo(compare="foo")
        test.foo(compare="bar", asserts=Assert.ne)
        test.double(args=(3,), compare=6)
        test.double(args=(4,), compare=10, asserts=Assert.lt)
        test.echo_sender(compare=a0.as_int)
        test.echo_sender(compare=a1.as_int, kwds={'sender': a1.privkey})

        with pytest.raises(ContractTestError):
            test.double(args=(1.2,))

        with pytest.raises(ContractTestError):
            test.echo_sender(kwds={'sender': a1.privkey})

        with pytest.raises(ContractTestError):
            test.foo(compare="bar", asserts=False)

        with pytest.raises(ContractTestError):
            test.foo(compare=bytearray("bar"), asserts=Assert.ne)
