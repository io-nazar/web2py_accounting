class IOGateway:

    def __init__(self, db):
        self.db = db

    def add_account(self, account):
        self.db.account.insert(account_name=account.account_name)

    def add_sector(self, account):
        self.db.sector.insert(sector_type=account.sector_type)

    def add_income(self, account):
        self.db.income.insert(account_id=account.account_id,
                              sector_type_id=account.sector_type_id,
                              income_date=account.creation_date,
                              amount=account.amount)

    def add_outcome(self, account):
        self.db.outcome.insert(account_id=account.account_id,
                               sector_type_id=account.sector_type_id,
                               income_date=account.creation_date,
                               amount=account.amount)

