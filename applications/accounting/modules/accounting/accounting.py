class Accounting:
    def __init__(self):
        pass


class Account(Accounting):

    def __init__(self, account_id=None, account_name=None, category_id=None,
                 category=None, creation_date=None, amount=None,
                 total_balance=None):

        self._account_id = account_id
        self._account_name = account_name
        self._category_id = category_id
        self._category = category
        self._creation_date = creation_date
        self._amount = amount
        self._total_balance = total_balance

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        if not account_id:
            raise ValueError('Error! account_id ')
        self._account_id = account_id

    @property
    def account_name(self):
        return self._account_name

    @account_name.setter
    def account_name(self, account_name):
        if not account_name:
            raise ValueError('Error! account_name ')
        self._account_name = account_name

    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        if not category_id:
            raise ValueError('Error! category_id')
        self._category_id = category_id

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if not category:
            raise ValueError('Error! category')
        self._category = category

    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        if not creation_date:
            raise ValueError('Error! creation_date')
        self._creation_date = creation_date

    @property
    def amount(self):
        return round(self._amount, 2)

    @amount.setter
    def amount(self, amount):
        if not amount:
            raise ValueError('Error! amount')
        self._amount = amount

    @property
    def total_balance(self):
        return round(self._total_balance, 2)

    @total_balance.setter
    def total_balance(self, total_balance):
        if not total_balance:
            raise ValueError('Error!', total_balance)
        self._total_balance = total_balance

    @staticmethod
    def extract_amount(values, key):
        amounts = []
        for value in values:
            amounts.append(value[key])
        return amounts

    @staticmethod
    def sum_up_amount(amounts):
        totalized_amount = 0.0
        for amount in amounts:
            totalized_amount += amount
        return round(totalized_amount, 2)
