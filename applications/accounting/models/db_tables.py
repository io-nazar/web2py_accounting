from gluon.tools import Auth
auth = Auth(db)
auth.enable_record_versioning(db)
auth.define_tables(signature=True)

db.define_table('account',
                Field(fieldname='account_name', type='string'),
                auth.signature,
                format='%(account_name)s')

db.define_table('sector',
                Field(fieldname='sector_type', type='string'),
                auth.signature,
                format='%(sector_type)s')

db.define_table('income',
                Field(fieldname='account_id', type='reference account'),
                Field(fieldname='sector_type_id',
                      type='reference sector'),
                Field(fieldname='income_date', type='datetime'),
                Field(fieldname='amount', type='double'),
                auth.signature)

db.define_table('outgoing',
                Field(fieldname='account_id', type='reference account'),
                Field(fieldname='sector_type_id',
                      type='reference sector'),
                Field(fieldname='income_date', type='datetime'),
                Field(fieldname='amount', type='double'),
                auth.signature)

db.define_table('balance',
                Field(fieldname='account_id', type='reference account'),
                Field(fieldname='amount', type='double', readable=True,
                      writable=True),
                auth.signature)

