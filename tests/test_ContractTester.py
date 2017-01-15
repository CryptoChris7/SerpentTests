import serpent_tests


class MyTest(serpent_tests.ContractTest):
    source_map = serpent_tests.sources_from_dir(__file__)

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
