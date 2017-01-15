import serpent_tests


class MyTest(serpent_tests.ContractTest):
    source_map = {
        'primes': '''\
def is_prime(n):
    if n < 2:
        return(0:bool)
    if n == 2:
        return(1:bool)
    if !(n&1):
        return(0:bool)
    with i = 3:
        while i*i < n:
            if n%i == 0:
                return(0:bool)
            i += 2
        return(1:bool)
''',
        'fibs': '''\
def fib(n):
    with a = 0:
        with b = 1:
            while n > 0:
                with temp = a + b:
                    a = b
                    b = temp
                n -= 1
            return(a)
''',
        'prime_fibs': '''\
import fibs as FIBS
import primes as PRIMES

def prime_fib_gt(n):
    with i = 0:
        with m = FIBS.fib(i):
            while !((m > n) and PRIMES.is_prime(m)):
                i += 1
                m = FIBS.fib(i)
            return(m)
'''
    }

    def test_is_prime(self):
        self.assertFalse(self.primes.is_prime(-1))
        self.assertTrue(self.primes.is_prime(2))
        self.assertTrue(self.primes.is_prime(3))
        self.assertTrue(self.primes.is_prime(23))
        self.assertFalse(self.primes.is_prime(24))
        self.assertFalse(self.primes.is_prime(8))

    def test_fib(self):
        self.assertEqual(self.fibs.fib(1), 1)
        self.assertEqual(self.fibs.fib(5), 5)
        self.assertEqual(self.fibs.fib(10), 55)

    def test_prime_fib_gt(self):
        self.assertEqual(self.prime_fibs.prime_fib_gt(3), 5)
        self.assertEqual(self.prime_fibs.prime_fib_gt(6), 13)


if __name__ == '__main__':
    MyTest.run_tests()
