from serpent_tests import ContractTest, Assert, Accounts

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
        tester = ContractTest(CODE)
        tester.foo(compare="foo")
        tester.foo(compare="bar", asserts=Assert.ne)
        tester.double(args=(3,), compare=6)
        tester.double(args=(4,), compare=10, asserts=Assert.lt)
        tester.echo_sender(compare=a0.as_int)
        tester.echo_sender(compare=a1.as_int, kwds={'sender': a1.privkey})
        tester.echo_sender(compare=a0.as_int/2, asserts=Assert.gt)
