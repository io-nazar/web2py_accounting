class IOGateway:

    def __init__(self, db, user_id=None):
        self._db = db
        self._user_id = user_id

    def add_account(self, account):
        self._db.account.insert(account_name=account.account_name)

    def add_sector(self, account):
        self._db.sector.insert(sector_type=account.sector_type)

    def add_income(self, account):
        self._db.income.insert(account_id=account.account_id,
                               sector_type_id=account.sector_type_id,
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

    def add_outcome(self, account):
        self._db.outcome.insert(account_id=account.account_id,
                                sector_type_id=account.sector_type_id,
                                income_date=account.creation_date,
                                amount=account.amount)

    def get_outcome(self):
        query = ((self._db.outcome.created_by == self._db.auth_user.id) &
                 (self._db.auth_user.id == self._user_id))
        outcome_rows = self._db(query=query).select()

        outcomes = []
        for outcome_row in outcome_rows:
            outcomes.append(dict(amount=outcome_row['outcome'].amount))
        return outcomes

