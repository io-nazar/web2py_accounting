from applications.accounting.models.io_gateway import IOGateway
from applications.accounting.modules.accounting.accounting import Account


def get_factory_form(ftype=None):
    if ftype == 'income' or ftype == 'outcome':
        form = SQLFORM.factory(
            Field(fieldname='account_id',
                  type='reference account',
                  requires=IS_IN_DB(db, 'account.id', '%(account_name)s'),
                  label='Account Name'),
            Field(fieldname='sector_type_id',
                  type='reference sector',
                  requires=IS_IN_DB(db, 'sector.id', '%(sector_type)s'),
                  label='Sector Type'),
            Field(fieldname='income_date',
                  type='datetime',
                  requires=IS_NOT_EMPTY()),
            Field(fieldname='amount',
                  type='double',
                  requires=IS_FLOAT_IN_RANGE(-1e100, 1e100),
                  label='Amount'))
        return form

    if ftype == 'balance':
        form = SQLFORM.factory(
            Field(fieldname='account_name',
                  type='reference account',
                  requires=IS_IN_DB(db, 'account.id', '%(account_name)s'),
                  label='Account Name'),
            Field(fieldname='amount',
                  type='double',
                  requires=IS_NOT_EMPTY(),
                  label='Amount'))
        return form

    if ftype == 'account':
        form = SQLFORM.factory(Field(fieldname='account_name',
                                     type='reference account',
                                     requires=IS_NOT_EMPTY(),
                                     label='Account Name'))
        return form

    if ftype == 'sector':
        form = SQLFORM.factory(Field(fieldname='sector_type',
                                     type='reference sector',
                                     requires=IS_NOT_EMPTY(),
                                     label='Sector Type'))
        return form


def create_overview_table(query):
    return SQLFORM.grid(query, showbuttontext=True, editable=True)


def create_account():
    account = Account()
    gateway_io = IOGateway(db=db)
    account_form = get_factory_form(ftype='account')
    if account_form.process().accepted:
        response.flash = get_msg(msg_type='success', msg_str='Account')
        account.account_name = account_form.vars.account_name
        gateway_io.add_account(account=account)
        db.commit()
    elif account_form.errors:
        response.flash = get_msg(msg_type='error', msg_str='Account')
    overview_table = create_overview_table(query=(db.account.id > 0))
    account_form = account_form + overview_table
    return dict(form=account_form)


def add_sector():
    account = Account()
    gateway_io = IOGateway(db=db)
    sector_form = get_factory_form(ftype='sector')
    if sector_form.process().accepted:
        response.flash = get_msg(msg_type='success', msg_str='Sector')
        account.sector_type = sector_form.vars.sector_type
        gateway_io.add_sector(account=account)
        db.commit()
    elif sector_form.errors:
        response.flash = get_msg(msg_type='error', msg_str='Sector')
    overview_table = create_overview_table(query=(db.sector.id > 0))
    sector_form = sector_form + overview_table
    return dict(form=sector_form)


def income():
    account = Account()
    gateway_io = IOGateway(db=db)
    income_form = get_factory_form(ftype='income')
    if income_form.process().accepted:
        response.flash = get_msg(msg_type='success', msg_str='Income')
        account = create_income_outcome(account=account,
                                        income_form=income_form)
        gateway_io.add_income(account=account)
        db.commit()
    elif income_form.errors:
        response.flash = get_msg(msg_type='error', msg_str='Income')
    overview_table = create_overview_table(query=(db.income.id > 0))
    income_form = income_form + overview_table
    return dict(form=income_form)


def create_income_outcome(account, income_form):
    account.account_id = income_form.vars.account_id
    account.sector_type_id = income_form.vars.sector_type_id
    account.creation_date = income_form.vars.income_date
    account.amount = income_form.vars.amount
    return account


def outcome():
    account = Account()
    gateway_io = IOGateway(db=db)
    outcome_form = get_factory_form(ftype='outcome')
    if outcome_form.process().accepted:
        response.flash = get_msg(msg_type='success', msg_str='Outcome')
        account = create_income_outcome(account=account,
                                        income_form=outcome_form)
        gateway_io.add_outcome(account=account)
        db.commit()
    elif outcome_form.errors:
        response.flash = get_msg(msg_type='error', msg_str='Outcome')
    overview_table = create_overview_table(query=(db.outcome.id > 0))
    outcome_form = outcome_form + overview_table
    return dict(form=outcome_form)


def balance():
    balance_form = get_factory_form(ftype='balance')
    return dict(form=balance_form)


def process_form(form):
    if form.process().accepted:
        response.flash = 'New record was sucessfuly added!'
    elif form.errors:
        response.flash = 'Error! Please fill all required fields'
    return form


def get_msg(msg_type, msg_str):
    if msg_type == 'success':
        return '{} Success! New record was sucessfuly added!'.format(msg_str)
    elif msg_type == 'error':
        return '{} Error! Please fill all required fields'.format(msg_str)
