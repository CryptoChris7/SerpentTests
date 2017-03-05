from serpent_tests import ContractTest, run_tests


class FibsTest(ContractTest):
    source = 'fibs.se'

    def test_fib(self):
        self.assertEqual(self.contract.fib(1), 1)
        self.assertEqual(self.contract.fib(5), 5)
        self.assertEqual(self.contract.fib(10), 55)

    def test_saveMyFib(self):
        self.assertEqual(self.contract.saveMyFib(10), 55)

    def test_loadMyFib(self):
        self.assertEqual(self.contract.loadMyFib(), 55)

if __name__ == '__main__':
    run_tests()
