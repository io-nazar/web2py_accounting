class Accounting:
    def __init__(self):
        pass


class Account(Accounting):

    def __init__(self, account_id=None, account_name=None, sector_id=None,
                 sector_type=None, creation_date=None, amount=None):

        self.account_id = account_id
        self._account_name = account_name
        self.sector_type_id = sector_id
        self._sector_type = sector_type
        self._creation_date = creation_date
        self._amount = amount

    @property
    def account_name(self):
        return self._account_name

    @account_name.setter
    def account_name(self, account_name):
        if not account_name:
            raise ValueError('Error! account_name ')
        self._account_name = account_name

    @property
    def sector_type(self):
        return self._sector_type

    @sector_type.setter
    def sector_type(self, sector_type):
        if not sector_type:
            raise ValueError('Error! sector_type')
        self._sector_type = sector_type

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
        return self._amount

    @amount.setter
    def amount(self, amount):
        if not amount:
            raise ValueError('Error! amount')
        self._amount = amount
