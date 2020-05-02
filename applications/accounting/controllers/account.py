from applications.accounting.modules.gateway.io_gateway import IOGateway
from applications.accounting.modules.accounting.accounting import Account
import logging
logger = logging.getLogger('web2py.app.accounting')
logger.setLevel(logging.DEBUG)
USER_ID = auth.user.id


@auth.requires_login()
def get_factory_form(ftype=None):
    if ftype == 'income' or ftype == 'outgoing':
        form = SQLFORM.factory(
            Field(fieldname='account_id',
                  type='reference account',
                  requires=IS_IN_DB(db, 'account.id', '%(account_name)s'),
                  label='Account Name'),
            Field(fieldname='category_id',
                  type='reference category',
                  requires=IS_IN_DB(db, 'category.id', '%(category)s'),
                  label='Category'),
            Field(fieldname='income_date',
                  type='datetime',
                  requires=IS_NOT_EMPTY()),
            Field(fieldname='amount',
                  type='double',
                  requires=IS_FLOAT_IN_RANGE(-1e100, 1e100),
                  label='Amount'),
            Field(fieldname='comment_field',
                  type='text',
                  label='Comment'))
        return form

    if ftype == 'account':
        form = SQLFORM.factory(Field(fieldname='account_name',
                                     type='reference account',
                                     requires=IS_NOT_EMPTY(),
                                     label='Account Name'))
        return form

    if ftype == 'category':
        form = SQLFORM.factory(Field(fieldname='category',
                                     type='reference category',
                                     requires=IS_NOT_EMPTY(),
                                     label='Category'))
        return form


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
                                 (db.auth_user.id == USER_ID)),
                                 create=False, details=False, csv=False)
    account_form = account_form + overview_table
    return dict(form=account_form)


@auth.requires_login()
def add_category():
    account = Account()
    gateway_io = IOGateway(db=db)
    category_form = get_factory_form(ftype='category')
    if category_form.process().accepted:
        response.flash = get_msg(msg_type='success', msg_str='Category')
        account.category = category_form.vars.category
        gateway_io.add_category(account=account)
        db.commit()
    elif category_form.errors:
        response.flash = get_msg(msg_type='error', msg_str='Category')
    overview_table = SQLFORM.grid(query=db.category, left=db.category.on(
                                 (db.category.created_by == db.auth_user.id) &
                                 (db.auth_user.id == USER_ID)),
                                 create=False, details=False, csv=False)
    category_form = category_form + overview_table
    return dict(form=category_form)


@auth.requires_login()
def income():
    account = Account()
    gateway_io = IOGateway(db=db)
    income_form = get_factory_form(ftype='income')
    if income_form.process().accepted:
        response.flash = get_msg(msg_type='success', msg_str='Income')
        account = create_income_outgoing(account=account,
                                         income_outgoing_form=income_form)
        gateway_io.add_income(account=account)
        db.commit()
    elif income_form.errors:
        response.flash = get_msg(msg_type='error', msg_str='Income')

    overview_table = SQLFORM.grid(query=db.income, left=db.income.on(
                                    (db.income.created_by == db.auth_user.id) &
                                    (db.auth_user.id == USER_ID)),
                                  create=False, details=False, csv=False)

    income_form = income_form + overview_table
    return dict(form=income_form)


def create_income_outgoing(account, income_outgoing_form):
    account.account_id = income_outgoing_form.vars.account_id
    account.category_id = income_outgoing_form.vars.category_id
    account.creation_date = income_outgoing_form.vars.income_date
    account.amount = income_outgoing_form.vars.amount
    account.comment = income_outgoing_form.vars.comment_field
    return account


@auth.requires_login()
def outgoing():
    account = Account()
    gateway_io = IOGateway(db=db)
    outgoing_form = get_factory_form(ftype='outgoing')
    if outgoing_form.process().accepted:
        response.flash = get_msg(msg_type='success', msg_str='Outgoing')
        account = create_income_outgoing(account=account,
                                         income_outgoing_form=outgoing_form)
        gateway_io.add_outgoing(account=account)
        db.commit()
    elif outgoing_form.errors:
        response.flash = get_msg(msg_type='error', msg_str='Outgoing')
    overview_table = SQLFORM.grid(query=db.outgoing, left=db.outgoing.on(
                                 (db.outgoing.created_by == db.auth_user.id) &
                                 (db.auth_user.id == USER_ID)),
                                 create=False, details=False, csv=False)
    outgoing_form = outgoing_form + overview_table
    return dict(form=outgoing_form)


@auth.requires_login()
def balance():
    account = Account()
    gateway_io = IOGateway(db=db, user_id=USER_ID)

    outgoing = gateway_io.get_outgoing()
    outgoing_amount = account.extract_amount(values=outgoing, key='amount')
    tot_outgoing_amount = account.sum_up_amount(amounts=outgoing_amount)
    logger.debug('balance > total outgoing amount: {}'.
                 format(tot_outgoing_amount))

    incomes = gateway_io.get_income()
    incomes_amount = account.extract_amount(values=incomes, key='amount')
    tot_income_amount = account.sum_up_amount(amounts=incomes_amount)
    logger.debug('balance > total income amount: {}'.format(tot_income_amount))

    total_balance = tot_income_amount - tot_outgoing_amount
    total_balance = round(total_balance, 2)
    account.total_balance = total_balance
    logger.debug('balance > total balance: {}'.format(account.total_balance))

    return dict(form=dict(balance=total_balance))


@auth.requires_login()
def get_msg(msg_type, msg_str):
    if msg_type == 'success':
        return '{} Success! New record was sucessfuly added!'.format(msg_str)
    elif msg_type == 'error':
        return '{} Error! Please fill all required fields'.format(msg_str)
