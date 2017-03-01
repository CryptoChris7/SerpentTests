from serpent_tests import ContractTest, run_tests


class FibsTest(ContractTest):
    source = 'fibs.se'

    def test_fib(self):
        self.assertEqual(self.contract.fib(1), 1)
        self.assertEqual(self.contract.fib(5), 5)
        self.assertEqual(self.contract.fib(10), 55)

if __name__ == '__main__':
    run_tests()
