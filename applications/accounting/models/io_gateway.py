class IOGateway:

    def __init__(self, db):
        self.db = db

    def add_account(self, account):
        self.db.account.insert(account_name=account.account_name)

    def add_sector(self, account):
        self.db.sector.insert(sector_type=account.sector_type)

    def add_income(self):
        pass

    def add_outcome(self):
        pass

    def add_balance(self):
        pass

