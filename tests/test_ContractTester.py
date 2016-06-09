from serpent_tests import ContractTester, Assert, Accounts

CODE = '''\
def foo():
    return(text("foo"):str)

def double(x):
    return(x*2)

def echo_sender():
    return(msg.sender)'''


class TestContractTester(object):
    def test(self):
        a0 = Accounts[0]
        a1 = Accounts[1]
        tester = ContractTester(CODE)
        tester.foo(expects="foo")
        tester.foo(expects="bar", asserts=Assert.unequal)
        tester.double(args=(3,), expects=6)
        tester.double(args=(4,), expects=10, asserts=Assert.lt)
        tester.echo_sender(expects=a0.as_int)
        tester.echo_sender(expects=a1.as_int, kwds={'sender': a1.privkey})
        tester.echo_sender(expects=a0.as_int/2, asserts=Assert.gt)
