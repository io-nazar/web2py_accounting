from applications.accounting.modules.application.gateway.io_gateway import IOGateway
from applications.accounting.modules.application.accounting.accounting import (
     Account, AccountOutgoing, AccountIncoming, AccountBalance)
from applications.accounting.modules.application.plots.charts.charts import (
     PieChart)
import logging

logger = logging.getLogger('web2py.app.accounting')
logger.setLevel(logging.DEBUG)
USER_ID = auth.user.id


@auth.requires_login()
def create_factory_form(ftype=None):
    if ftype == 'incoming' or ftype == 'outgoing':
        form = SQLFORM.factory(
            Field(fieldname='account_id',
                  type='reference account',
                  requires=IS_IN_DB(db, 'account.id', '%(account_name)s'),
                  label='Account Name'),
            Field(fieldname='category_id',
                  type='reference category',
                  requires=IS_IN_DB(db, 'category.id', '%(category)s'),
                  label='Category'),
            Field(fieldname='incoming_date',
                  type='datetime',
                  requires=IS_NOT_EMPTY()),
            Field(fieldname='amount',
                  type='double',
                  requires=IS_FLOAT_IN_RANGE(-1e100, 1e100),
                  label='Amount'),
            Field(fieldname='comment_field',
                  type='string',
                  label='Comment'))
        logger.debug('Created {} form'.format(ftype))
        return form

    if ftype == 'account':
        form = SQLFORM.factory(Field(fieldname='account_name',
                                     type='reference account',
                                     requires=IS_NOT_EMPTY(),
                                     label='Account Name'))
        logger.debug('Created {} form'.format(ftype))
        return form

    if ftype == 'category':
        form = SQLFORM.factory(Field(fieldname='category',
                                     type='reference category',
                                     requires=IS_NOT_EMPTY(),
                                     label='Category'))
        logger.debug('Created {} form'.format(ftype))
        return form


@auth.requires_login()
def create_account():
    logger.debug('Calling Create Account')
    account = Account()
    gateway_io = IOGateway(db=db)
    account_form = create_factory_form(ftype='account')
    if account_form.process().accepted:
        response.flash = get_msg(msg_type='success', msg_str='Account')
        account.account_name = account_form.vars.account_name
        gateway_io.add_account(account=account)
        db.commit()
    elif account_form.errors:
        response.flash = get_msg(msg_type='error', msg_str='Account')
    fields = [db.account.account_name, db.auth_user.first_name]
    overview_table = SQLFORM.grid(db.account, left=db.account.on(
        (db.account.created_by == db.auth_user.id) &
        (db.auth_user.id == USER_ID)), fields=fields,
                                  create=False, details=False, csv=False)
    account_form = account_form + overview_table
    return dict(form=account_form)


@auth.requires_login()
def add_category():
    logger.debug('Calling Add Category')
    account = Account()
    gateway_io = IOGateway(db=db)
    category_form = create_factory_form(ftype='category')
    if category_form.process().accepted:
        response.flash = get_msg(msg_type='success', msg_str='Category')
        account.category = category_form.vars.category
        gateway_io.add_category(account=account)
        db.commit()
    elif category_form.errors:
        response.flash = get_msg(msg_type='error', msg_str='Category')
    fields = [db.category.category, db.auth_user.first_name]
    overview_table = SQLFORM.grid(query=db.category, left=db.category.on(
        (db.category.created_by == db.auth_user.id) &
        (db.auth_user.id == USER_ID)), fields=fields,
                                  create=False, details=False, csv=False)
    category_form = category_form + overview_table
    return dict(form=category_form)


@auth.requires_login()
def incoming():
    logger.debug('Calling Incoming Section')
    acc_in = AccountIncoming()
    gateway_io = IOGateway(db=db, user_id=USER_ID)
    incoming_form = create_factory_form(ftype='incoming')
    if incoming_form.process().accepted:
        response.flash = get_msg(msg_type='success', msg_str='Incoming')
        acc_in = get_data_from_in_out_going_form(
                 account=acc_in, incoming_outgoing_form=incoming_form)
        gateway_io.add_incoming(account=acc_in)
        db.commit()
    elif incoming_form.errors:
        response.flash = get_msg(msg_type='error', msg_str='Incoming')
    fields = [db.incoming.account_id, db.incoming.category_id,
              db.incoming.incoming_date, db.incoming.amount,
              db.incoming.comment_field, db.auth_user.first_name]
    overview_table = SQLFORM.grid(query=db.incoming, left=db.incoming.on(
        (db.incoming.created_by == db.auth_user.id) &
        (db.auth_user.id == USER_ID)), fields=fields,
                                  create=False, details=False, csv=False)

    incoming_form = incoming_form + overview_table
    incoming = gateway_io.get_incoming_data()
    acc_in.accounts_data = incoming
    amount_per_category = acc_in.get_amount_sum_per_category()
    plot_data = amount_per_category
    plot_html = draw_plot(plot_data=plot_data, plot_type='PieChart')
    return dict(form=incoming_form, plot_html=plot_html)


@auth.requires_login()
def outgoing():
    logger.debug('Calling Outgoing Section')
    acc_out = AccountOutgoing()
    gateway_io = IOGateway(db=db, user_id=USER_ID)
    outgoing_form = create_factory_form(ftype='outgoing')
    if outgoing_form.process().accepted:
        response.flash = get_msg(msg_type='success', msg_str='Outgoing')
        acc_out = get_data_from_in_out_going_form(
                  account=acc_out, incoming_outgoing_form=outgoing_form)
        gateway_io.add_outgoing(account=acc_out)
        db.commit()
    elif outgoing_form.errors:
        response.flash = get_msg(msg_type='error', msg_str='Outgoing')
    fields = [db.outgoing.account_id, db.outgoing.category_id,
              db.outgoing.outgoing_date, db.outgoing.amount,
              db.outgoing.comment_field, db.auth_user.first_name]
    overview_table = SQLFORM.grid(query=db.outgoing, left=db.outgoing.on(
        (db.outgoing.created_by == db.auth_user.id) &
        (db.auth_user.id == USER_ID)), fields=fields,
                                  create=False, details=False, csv=False)
    outgoing_form = outgoing_form + overview_table
    outgoing = gateway_io.get_outgoing_data()
    acc_out.accounts_data = outgoing
    amount_per_category = acc_out.get_amount_sum_per_category()
    plot_data = amount_per_category
    plot_html = draw_plot(plot_data=plot_data, plot_type='PieChart')
    return dict(form=outgoing_form, plot_html=plot_html)


def get_data_from_in_out_going_form(account, incoming_outgoing_form):
    logger.debug('Getting data from incoming/outgoing forms.'
                 'Received Data: {}'.format(incoming_outgoing_form.vars))
    account.account_id = incoming_outgoing_form.vars.account_id
    account.category_id = incoming_outgoing_form.vars.category_id
    account.creation_date = incoming_outgoing_form.vars.incoming_date
    account.amount = incoming_outgoing_form.vars.amount
    account.comment = incoming_outgoing_form.vars.comment_field
    return account


@auth.requires_login()
def balance():
    logger.debug('Generating Account Balance')
    account = Account()
    gateway_io = IOGateway(db=db, user_id=USER_ID)
    outgoing = gateway_io.get_outgoing_data()
    tot_acc_amount_out = account.get_account_amounts(acc_type='outgoing',
                                                     values=outgoing)

    incoming = gateway_io.get_incoming_data()
    tot_acc_amount_in = account.get_account_amounts(acc_type='incoming',
                                                    values=incoming)
    total_balance = (tot_acc_amount_in['total_amounts'] -
                     tot_acc_amount_out['total_amounts'])
    total_balance = round(total_balance, 2)
    account.total_balance = total_balance
    logger.debug('balance > total balance: {}'.format(account.total_balance))

    return dict(form=dict(balance=total_balance))


@auth.requires_login()
def get_msg(msg_type, msg_str):
    logger.debug('Getting message >  Message Type: {}, Message {}'.format(
                 msg_type, msg_str))
    if msg_type == 'success':
        return '{} Success! New record was sucessfuly added!'.format(msg_str)
    elif msg_type == 'error':
        return '{} Error! Please fill all required fields'.format(msg_str)


@auth.requires_login()
def draw_plot(plot_data, plot_type):
    logger.debug('Draw Plot > Plot Data: {} Plot Type: {}'.format(plot_data,
                                                                  plot_type))
    if plot_type == 'PieChart':
        pie_chart = PieChart()
        pie_chart.pie_chart_data = plot_data
        pie_chart.pie_chart_conf = dict(xrange=(-1, 1.0), plot_height=500,
                                        x=0, y=1, radius=0.4)
    pie_chart.chart_title = "Pie Chart: Category / Amount"
    plot_html = pie_chart.create_pie_chart()
    return plot_html
