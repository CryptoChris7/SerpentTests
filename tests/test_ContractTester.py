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
        tester.foo(expects="foo",
                   asserts=Assert.equal)
        tester.double(args=(3,), expects=6, asserts=Assert.equal)
        tester.echo_sender(expects=a0.as_int, asserts=Assert.equal)
        tester.echo_sender(expects=a1.as_int,
                           asserts=Assert.equal,
                           kwds={'sender': a1.privkey})

        
# def main():
    
#     t = ContractTester(code)

#     print 'Contract code:'
#     print '--------------'
#     print code
#     print '--------------'
#     print 'Gas cost:', t.gas_cost
#     print '--------------'
#     print 'Contract address:', str(t.contractAccount)
#     print '--------------'
    
#     a0 = t.accounts[0].address_as_int
#     a1 = t.accounts[1].address_as_int
#     k1 = t.accounts[1].privkey

#     # t.run_tests([('foo', (), {}, "foo"),
#     #              ('double', (3,), {}, 6),
#     #              ('echo_sender', (), {}, a0),
#     #              ('echo_sender', (), {'sender': k1}, a1)])

# if __name__ == '__main__':
#     main()
