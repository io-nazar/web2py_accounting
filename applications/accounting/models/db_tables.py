db.define_table('account',
                Field(fieldname='account_name', type='string'),
                format='%(account_name)s')

db.define_table('sector',
                Field(fieldname='sector_type', type='string'),
                format='%(sector_type)s')

db.define_table('income',
                Field(fieldname='account_id', type='reference account'),
                Field(fieldname='income_sector_type_id',
                      type='reference sector'),
                Field(fieldname='income_date', type='datetime'),
                Field(fieldname='amount', type='double'))

db.define_table('outcome',
                Field(fieldname='account_id', type='reference account'),
                Field(fieldname='outcome_sector_type_id',
                      type='reference sector'),
                Field(fieldname='income_date', type='datetime'),
                Field(fieldname='amount', type='double'))

db.define_table('balance',
                Field(fieldname='account_id', type='reference account'),
                Field(fieldname='amount', type='double', readable=True,
                      writable=True))


