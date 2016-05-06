from . import Tester
from ethereum.tester import a0, a1, k1
from ethereum.utils import coerce_to_int

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
    
    t.run_tests([('foo', (), {}, "foo"),
                 ('double', (3,), {}, 6),
                 ('echo_sender', (), {}, coerce_to_int(a0)),
                 ('echo_sender', (), {'sender': k1}, coerce_to_int(a1))])

if __name__ == '__main__':
    main()
