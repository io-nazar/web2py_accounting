import unittest
import datetime
from applications.accounting.modules.application.accounting.accounting import (
     Account)


class TestAccounting(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls._acc_dat = [
            {
             'account': 'Stocks', 'category': 'Other',
             'outgoing_date': datetime.datetime(2020, 5, 10, 11, 39, 7),
             'amount': 5.0,
             'comment': 'Some comment 1'
            },
            {
             'account': 'Stocks', 'category': 'Other',
             'outgoing_date': datetime.datetime(2020, 5, 10, 11, 39, 7),
             'amount': 50.0,
             'comment': 'Some comment 2'
            },
            {
             'account': 'Stocks', 'category': 'Dividend',
             'outgoing_date': datetime.datetime(2020, 5, 20, 14, 23, 49),
             'amount': 3.3, 'comment': 'test'
            },
            {
             'account': 'Household', 'category': 'Dividend',
             'outgoing_date': datetime.datetime(2020, 5, 5, 14, 26, 25),
             'amount': 3.31, 'comment': 'test'
            }]

    def test_extract_amounts(self):
        account = Account()
        account.amounts = account.extract_amounts(values=self._acc_dat,
                                                  key='amount')
        tot_amounts = account.sum_up_amounts()
        self.assertEqual(first=61.61,
                         second=tot_amounts)

    def test_sum_up_amount(self):
        account = Account()
        account.amounts = [3.351, 8.351, 1.0]
        total_amount = account.sum_up_amounts()
        self.assertEqual(first=12.70,
                         second=total_amount)

    def test_determine_categories_of_account_data(self):
        account = Account()
        account.accounts_data = self._acc_dat
        account.determine_categories_of_account_data()
        self.assertTrue(
            {'Dividend', 'Other'}.issuperset(account._categories.category_set))


if __name__ == '__main__':
    unittest.main()
