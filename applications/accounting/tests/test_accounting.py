import unittest
import datetime
from applications.accounting.modules.application.accounting.accounting import (
     Account)


class TestAccounting(unittest.TestCase):

    def test_sum_up_amount(self):
        account = Account()
        account.amounts = [3.351, 8.351, 1.0]
        total_amount = account.sum_up_amounts()
        self.assertEqual(first=12.70,
                         second=total_amount)

    def test_determine_categories_of_account_data(self):
        acc_dat = [{'account': 'Stocks', 'category': 'Other',
                    'outgoing_date': datetime.datetime(2020, 5, 10, 11, 39, 7),
                    'amount': 5.0,
                    'comment': 'Some comment 1'
                    },
                   {'account': 'Stocks', 'category': 'Other',
                    'outgoing_date': datetime.datetime(2020, 5, 10, 11, 39, 7),
                    'amount': 50.0,
                    'comment': 'Some comment 2'
                    },
                   {'account': 'Stocks', 'category': 'Dividend',
                    'outgoing_date': datetime.datetime(2020, 5, 20, 14, 23, 49),
                    'amount': 3.3, 'comment': 'test'
                    },
                   {'account': 'Household', 'category': 'Dividend',
                    'outgoing_date': datetime.datetime(2020, 5, 5, 14, 26, 25),
                    'amount': 3.31, 'comment': 'test'
                    }]
        account = Account()
        account.accounts_data = acc_dat
        categories_set = account.determine_categories_of_account_data()
        categories_lst = list(categories_set)
        self.assertEqual(first='Dividend',
                         second=categories_lst[0])
        self.assertEqual(first='Other',
                         second=categories_lst[1])


if __name__ == '__main__':
    unittest.main()
