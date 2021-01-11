import logging
logger = logging.getLogger('web2py.app.accounting')
logger.setLevel(logging.DEBUG)

class IOGateway:

    def __init__(self, db, user_id=None):
        self._db = db
        self._user_id = user_id

    def add_account(self, account):
        self._db.account.insert(account_name=account.account_name)

    def add_category(self, account):
        self._db.category.insert(category=account.category)

    def add_incoming(self, account):
        self._db.incoming.insert(account_id=account.account_id,
                                 category_id=account.category_id,
                                 incoming_date=account.creation_date,
                                 amount=account.amount,
                                 comment_field=account.comment)

    def get_incoming_data(self):
        logger.debug('selecting incoming data from the database')
        query = ((self._db.incoming.created_by == self._db.auth_user.id) &
                 (self._db.auth_user.id == self._user_id))
        incoming_rows = self._db(query=query).select()
        incoming = []
        for incoming_row in incoming_rows:
            account_id = incoming_row['incoming'].account_id
            category_id = incoming_row['incoming'].category_id
            account_row = self._db(
                self._db.account.id == account_id).select().first()
            category_row = self._db(
                self._db.category.id == category_id).select().first()
            incoming.append(
                dict(account=account_row.account_name,
                     category=category_row.category,
                     incoming_date=incoming_row['incoming'].incoming_date,
                     amount=incoming_row['incoming'].amount,
                     comment=incoming_row['incoming'].comment_field))
        return incoming

    def add_outgoing(self, account):
        logger.debug('inserting outgoing data in to the database')
        self._db.outgoing.insert(account_id=account.account_id,
                                 category_id=account.category_id,
                                 outgoing_date=account.creation_date,
                                 amount=account.amount,
                                 comment_field=account.comment)

    def get_outgoing_data(self):
        logger.debug('selecting outgoing data from the database')
        query = ((self._db.outgoing.created_by == self._db.auth_user.id) &
                 (self._db.auth_user.id == self._user_id))
        outgoing_rows = self._db(query=query).select()
        outgoing = []
        for outgoing_row in outgoing_rows:
            account_id = outgoing_row['outgoing'].account_id
            category_id = outgoing_row['outgoing'].category_id
            account_row = self._db(
                self._db.account.id == account_id).select().first()
            category_row = self._db(
                self._db.category.id == category_id).select().first()
            outgoing.append(
                dict(account=account_row.account_name,
                     category=category_row.category,
                     outgoing_date=outgoing_row['outgoing'].outgoing_date,
                     amount=outgoing_row['outgoing'].amount,
                     comment=outgoing_row['outgoing'].comment_field))
        return outgoing
