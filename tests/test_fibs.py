from serpent_tests import ContractTest, default_accounts


class FibsTest(ContractTest):
    source = 'fibs.se'

    def test_fib(self):
        self.assertEqual(self.contract.fib(1), 1)
        self.assertEqual(self.contract.fib(5), 5)
        self.assertEqual(self.contract.fib(10), 55)

    def test_saveFib(self):
        with self.assertTxFail():
            baddie = default_accounts[1].private_key
            self.contract.saveFib(self.creator.address, 10, sender=baddie)
        self.assertEqual(self.contract.saveFib(self.creator.address, 10), 55)

    def test_loadMyFib(self):
        self.assertEqual(self.contract.loadMyFib(), 55)

if __name__ == '__main__':
    FibsTest.run_tests()
