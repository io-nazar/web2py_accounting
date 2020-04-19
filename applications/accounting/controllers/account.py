from applications.accounting.modules.gateway.io_gateway import IOGateway
from applications.accounting.modules.accounting.accounting import Account
import logging
logger = logging.getLogger('web2py.app.accounting')
logger.setLevel(logging.DEBUG)
USER_ID = auth.user.id


@auth.requires_login()
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


@auth.requires_login()
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
    overview_table = SQLFORM.grid(db.account, left=db.account.on(
                                 (db.account.created_by == db.auth_user.id) &
                                 (db.auth_user.id == USER_ID)))
    account_form = account_form + overview_table
    return dict(form=account_form)


@auth.requires_login()
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
    overview_table = SQLFORM.grid(db.sector, left=db.sector.on(
                                 (db.sector.created_by == db.auth_user.id) &
                                 (db.auth_user.id == USER_ID)))
    sector_form = sector_form + overview_table
    return dict(form=sector_form)

@auth.requires_login()
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

    overview_table = SQLFORM.grid(db.income, left=db.income.on(
                                 (db.income.created_by == db.auth_user.id) &
                                 (db.auth_user.id == USER_ID)))

    income_form = income_form + overview_table
    return dict(form=income_form)


def create_income_outcome(account, income_form):
    account.account_id = income_form.vars.account_id
    account.sector_type_id = income_form.vars.sector_type_id
    account.creation_date = income_form.vars.income_date
    account.amount = income_form.vars.amount
    return account


@auth.requires_login()
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
    overview_table = SQLFORM.grid(db.outcome, left=db.outcome.on(
                                 (db.outcome.created_by == db.auth_user.id) &
                                 (db.auth_user.id == USER_ID)))
    outcome_form = outcome_form + overview_table
    return dict(form=outcome_form)


def balance():
    overview_table = create_overview_table(query=(db.balance.id > 0))
    return dict(form=overview_table)


def get_msg(msg_type, msg_str):
    if msg_type == 'success':
        return '{} Success! New record was sucessfuly added!'.format(msg_str)
    elif msg_type == 'error':
        return '{} Error! Please fill all required fields'.format(msg_str)
