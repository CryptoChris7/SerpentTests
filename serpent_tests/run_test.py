from serpent_tests import Tester

def main():
    code = '''\
def foo():
    return(text("foo"):str)

def double(x):
    return(x*2)

def echo_sender():
    return(msg.sender)'''
    t = Tester(code)

    print 'Contract code:'
    print '--------------'
    print code
    print '--------------'
    print 'Gas cost:', t.gas_cost
    print '--------------'
    
    a0 = t.accounts[0].address_as_int
    a1 = t.accounts[1].address_as_int
    k1 = t.accounts[1].privkey

    t.run_tests([('foo', (), {}, "foo"),
                 ('double', (3,), {}, 6),
                 ('echo_sender', (), {}, a0),
                 ('echo_sender', (), {'sender': k1}, a1)])

if __name__ == '__main__':
    main()
