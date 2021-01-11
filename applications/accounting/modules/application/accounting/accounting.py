import logging
logger = logging.getLogger("web2py.app.accounting")
logger.setLevel(logging.DEBUG)


class Accounting:
    def __init__(self):
        pass


class Account(Accounting):

    def __init__(self, account_id=None, account_name=None, category_id=None,
                 category=None, creation_date=None, amount=None,
                 total_balance=None, comment=None):

        self._account_id = account_id
        self._account_name = account_name
        self._category_id = category_id
        self._category = category
        self._creation_date = creation_date
        self._amount = amount
        self._amounts = None
        self._total_balance = total_balance
        self._comment = comment
        self._accounts_data = list()

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        if not account_id:
            raise Exception('Error! account_id ')
        self._account_id = account_id

    @property
    def account_name(self):
        return self._account_name

    @account_name.setter
    def account_name(self, account_name):
        if not account_name:
            raise Exception('Error! account_name ')
        self._account_name = account_name

    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        if not category_id:
            raise Exception('Error! category_id')
        self._category_id = category_id

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if not category:
            raise Exception('Error! category')
        self._category = category

    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        if not creation_date:
            raise Exception('Error! creation_date')
        self._creation_date = creation_date

    @property
    def amount(self):
        return float('%.2f' % self._amount)

    @amount.setter
    def amount(self, amount):
        if not amount:
            raise Exception('Error! amount')
        self._amount = amount

    @property
    def amounts(self):
        return self._amounts

    @amounts.setter
    def amounts(self, amounts):
        if not amounts:
            raise Exception('Error! amounts')
        self._amounts = amounts

    @property
    def total_balance(self):
        return float('%.2f' % self._total_balance)

    @total_balance.setter
    def total_balance(self, total_balance):
        if not total_balance:
            raise Exception('Error! total_amount', total_balance)
        self._total_balance = total_balance

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = comment

    @property
    def accounts_data(self):
        return self._accounts_data

    @accounts_data.setter
    def accounts_data(self, accounts_data):
        if isinstance(accounts_data, list):
            logger.debug('Setting {} account data {}'
                         .format(self.__class__.__name__, accounts_data))
            self._accounts_data = accounts_data
        else:
            raise Exception(
                'Error {} account data'.format(self.__class__.__name__))

    @staticmethod
    def extract_amounts(values, key):
        amounts = []
        for value in values:
            amounts.append(value[key])
        return amounts

    def sum_up_amounts(self):
        totalized_amount = 0.0
        for amount in self.amounts:
            totalized_amount += amount
        return float('%.2f' % totalized_amount)

    def sum_up_catergory_amount(self, category):
        for account_data in self.accounts_data:
            for category_amount in category.categories_lst:
                if account_data['category'] == category_amount['category']:
                    category_amount['amount'] += account_data['amount']
        logger.debug('[sum_up_catergory_amount]: {}'.format(category_amount))
        return category_amount

    def get_amount_sum_per_category(self):
        category_set = self.determine_categories_of_account_data()
        catgr = Category()
        for category in category_set:
            catgr.categories_lst.append(dict(category=category, amount=0.0))
        logger.debug('Created Category / Amount list: {}'.format(
                     catgr.categories_lst))
        category_amount = self.sum_up_catergory_amount(category=catgr)
        logger.debug('Sum upped amount per category: {}'.format(
                     catgr.categories_lst))
        for category in catgr.categories_lst:
            category_amount = dict.fromkeys([category['category']],
                                            category['amount'])
            catgr.amount_per_category.update(category_amount)
        logger.debug('Created amount per category {}'
                     .format(catgr.amount_per_category))
        return catgr.amount_per_category

    def determine_categories_of_account_data(self):
        catgr = Category()
        for category in self.accounts_data:
            catgr.category_set.add(category['category'])
        logger.debug('Determined categories of account data: {}'
                     .format(catgr.category_set))
        return catgr.category_set


class Category:
    def __init__(self):
        self._categories_lst = list()
        self._amount_per_category = dict()
        self._category_set = set()

    @property
    def categories_lst(self):
        return self._categories_lst

    @categories_lst.setter
    def categories_lst(self, categories_lst):
        if isinstance(categories_lst, list) or not categories_lst:
            raise Exception('Class: {} Error Categories List '
                            .format(self.__class__.__name__))
        self._categories_lst = categories_lst

    @property
    def amount_per_category(self):
        return self._amount_per_category

    @amount_per_category.setter
    def amount_per_category(self, amount_per_category):
        if isinstance(amount_per_category, dict) or not amount_per_category:
            raise Exception('Class: {} Error Amount Per Category '
                            .format(self.__class__.__name__))
        self._amount_per_category = amount_per_category

    @property
    def category_set(self):
        return self._category_set

    @category_set.setter
    def category_set(self, category_set):
        if isinstance(category_set, set) or not category_set:
            raise Exception('Class: {} Error Category Set'
                            .format(self.__class__.__name__))
        self._category_set = category_set


class AccountOutgoing(Account):
    def __init__(self):
        super(AccountOutgoing, self).__init__(self)


class AccountIncoming(Account):
    def __init__(self):
        super(AccountIncoming, self).__init__(self)


class AccountBalance(Account):
    def __init__(self):
        super(AccountBalance, self).__init__(self)
