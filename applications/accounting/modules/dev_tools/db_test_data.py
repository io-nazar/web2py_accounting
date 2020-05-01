from datetime import datetime


class InsertTestData:

    def __init__(self, db):
        self.db = db

    def _load_test_data(self):
        accounts_ids = self.db.account.bulk_insert([
                        dict(account_name='Household'),
                        dict(account_name='private account 1'),
                        dict(account_name='private account 2')])

        category_ids = self.db.category.bulk_insert([
                        dict(category='Salary'),
                        dict(category='Sponsorship'),
                        dict(category='Some Category')])

        self.db.income.bulk_insert([
                        dict(account_id=accounts_ids[0],
                             category_id=category_ids[0],
                             income_date=datetime.today(),
                             amount=10.1),
                        dict(account_id=accounts_ids[1],
                             category_id=category_ids[1],
                             income_date=datetime.today(),
                             amount=100.2),
                        dict(account_id=accounts_ids[2],
                             category_id=category_ids[2],
                             income_date=datetime.today(),
                             amount=1000.3)])

        self.db.outgoing.bulk_insert([
                        dict(account_id=accounts_ids[0],
                             category_id=category_ids[0],
                             outgoing_date=datetime.today(),
                             amount=10.0),
                        dict(account_id=accounts_ids[1],
                             category_id=category_ids[1],
                             outgoing_date=datetime.today(),
                             amount=100.0),
                        dict(account_id=accounts_ids[2],
                             category_id=category_ids[2],
                             outgoing_date=datetime.today(),
                             amount=1000.0)])

    def start_insertion(self):
        self._load_test_data()
