from gluon.tools import Auth
auth = Auth(db)
auth.enable_record_versioning(db)
auth.define_tables(signature=True)

db.define_table('account',
                Field(fieldname='account_name', type='string',
                      requires=IS_NOT_EMPTY(), label='Accounts Name'),
                auth.signature,
                format='%(account_name)s')

db.define_table('category',
                Field(fieldname='category', type='string',
                      requires=IS_NOT_EMPTY(), label='Category'),
                auth.signature,
                format='%(category)s')

db.define_table('income',
                Field(fieldname='account_id', type='reference account',
                      requires=IS_NOT_EMPTY(), label='Accounts Name'),
                Field(fieldname='category_id', type='reference category',
                      requires=IS_NOT_EMPTY(), label='Category'),
                Field(fieldname='income_date', type='datetime',
                      requires=IS_NOT_EMPTY(), label='Date'),
                Field(fieldname='amount', type='double',
                      requires=IS_NOT_EMPTY(), label='Amount'),
                Field(fieldname='comment_field', type='text', label='Comment'),
                auth.signature,
                format='%(amount)s')

db.define_table('outgoing',
                Field(fieldname='account_id', type='reference account',
                      requires=IS_NOT_EMPTY(), label='Accounts Name'),
                Field(fieldname='category_id', type='reference category',
                      requires=IS_NOT_EMPTY(), label='Category'),
                Field(fieldname='outgoing_date', type='datetime',
                      requires=IS_NOT_EMPTY(), label='Date'),
                Field(fieldname='amount', type='double',
                      requires=IS_NOT_EMPTY(), label='Amount'),
                Field(fieldname='comment_field', type='text',
                      requires=IS_NOT_EMPTY(), label='Comment'),
                auth.signature,
                format='%(amount)s')

db.define_table('balance',
                Field(fieldname='account_id', type='reference account',
                      requires=IS_NOT_EMPTY(), label='Accounts Name'),
                Field(fieldname='amount', type='double', readable=True,
                      writable=True, requires=IS_NOT_EMPTY(), label='Amount'),
                auth.signature,
                format='%(amount)s')

