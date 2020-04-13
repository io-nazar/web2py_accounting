
if not configuration.get('app.production'):
    response.menu += [
        (T('Manage Account'), False, '#', [
            (T('Create Account'), False, URL('accounting', 'account',
                                             'create_account')),
            (T('Add Sector'), False, URL('accounting', 'account',
                                         'add_sector'))]),
        (T('Income'), False, URL('accounting', 'account', 'income')),
        (T('Outcome'), False, URL('accounting', 'account', 'outcome')),
        (T('Balance'), False, URL('accounting', 'account', 'balance')),
        (T('Dev Tools'), False, '#', [
            (T('Insert Test Data'), False, URL('accounting', 'dev_tools',
                                               'insert_test_data'))]),
    ]

if configuration.get('app.production'):
    response.menu += [
        (T('Manage Account'), False, '#', [
            (T('Create Account'), False, URL('accounting', 'account',
                                             'create_account')),
            (T('Add Sector'), False, URL('accounting', 'account',
                                         'add_sector'))]),
        (T('Income'), False, URL('accounting', 'account', 'income')),
        (T('Outcome'), False, URL('accounting', 'account', 'outcome')),
        (T('Balance'), False, URL('accounting', 'account', 'balance'))
    ]

