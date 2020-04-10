def get_factory_form(ftype=None):
    if ftype == 'income' or ftype == 'outcome':
        form = SQLFORM.factory(
            Field(fieldname='account_id',
                  type='reference account',
                  requires=IS_IN_DB(db, 'account.id', '%(account_name)s'),
                  label='Account Name'),
            Field(fieldname='income_sector_id',
                  type='reference sector',
                  requires=IS_IN_DB(db, 'sector.id', '%(sector_type)s'),
                  label='Sector Type'),
            Field(fieldname='income_date',
                  type='datetime',
                  requires=IS_NOT_EMPTY()),
            Field(fieldname='amount',
                  type='double',
                  requires=IS_NOT_EMPTY(),
                  label='Amount'))
        return form

    if ftype == 'balance':
        form = SQLFORM.factory(
            Field(fieldname='account_id',
                  type='reference account',
                  requires=IS_IN_DB(db, 'account.id', '%(account_name)s'),
                  label='Account Name'),
            Field(fieldname='amount',
                  type='double',
                  requires=IS_NOT_EMPTY(),
                  label='Amount'))
        return form

    if ftype == 'account':
        form = SQLFORM.factory(Field(fieldname='account_id',
                                     type='reference account',
                                     requires=IS_NOT_EMPTY(),
                                     label='Account Name'))
        return form

    if ftype == 'sector':
        form = SQLFORM.factory(Field(fieldname='sector_id',
                                     type='reference sector',
                                     requires=IS_NOT_EMPTY(),
                                     label='Sector Name'))
        return form



def create_account():
    account_form = get_factory_form(ftype='account')
    account_form = process_form(form=account_form)
    return dict(form=account_form)


def add_sector():
    sector_form = get_factory_form(ftype='sector')
    sector_form = process_form(form=sector_form)
    return dict(form=sector_form)


def income():
    income_form = get_factory_form(ftype='income')
    income_form = process_form(form=income_form)
    return dict(form=income_form)


def outcome():
    outcome_form = get_factory_form(ftype='outcome')
    outcome_form = process_form(form=outcome_form)
    return dict(form=outcome_form)


def balance():
    balance_form = get_factory_form(ftype='balance')
    return dict(form=balance_form)


def process_form(form):
    if form.process().accepted:
        response.flash = 'New Record sucessfuly added!'
    elif form.errors:
        response.flash = 'Error! Please fill all required fields'
    return form


