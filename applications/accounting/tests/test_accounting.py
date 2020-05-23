import unittest
from applications.accounting.modules.accounting.accounting import Account


class TestAccounting(unittest.TestCase):

    def test_sum_up_amount(self):
        account = Account()
        amounts = [3.351, 8.351, 1.0]
        total_amount = account.sum_up_amount(amounts=amounts)
        self.assertEqual(first=12.70,
                         second=total_amount)


if __name__ == '__main__':
    unittest.main()
