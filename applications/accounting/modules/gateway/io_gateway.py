class IOGateway:

    def __init__(self, db, user_id=None):
        self._db = db
        self._user_id = user_id

    def add_account(self, account):
        self._db.account.insert(account_name=account.account_name)

    def add_category(self, account):
        self._db.category.insert(category=account.category)

    def add_income(self, account):
        self._db.income.insert(account_id=account.account_id,
                               category_id=account.category_id,
                               income_date=account.creation_date,
                               amount=account.amount)

    def get_income(self):
        query = ((self._db.income.created_by == self._db.auth_user.id) &
                 (self._db.auth_user.id == self._user_id))
        income_rows = self._db(query=query).select()
        incomes = []
        for income_row in income_rows:
            incomes.append(dict(amount=income_row['income'].amount))
        return incomes

    def add_outgoing(self, account):
        self._db.outgoing.insert(account_id=account.account_id,
                                 category_id=account.category_id,
                                 income_date=account.creation_date,
                                 amount=account.amount)

    def get_outgoing(self):
        query = ((self._db.outgoing.created_by == self._db.auth_user.id) &
                 (self._db.auth_user.id == self._user_id))
        outgoing_rows = self._db(query=query).select()

        outgoing = []
        for outgoing_row in outgoing_rows:
            outgoing.append(dict(amount=outgoing_row['outgoing'].amount))
        return outgoing

