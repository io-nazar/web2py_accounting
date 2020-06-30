from applications.accounting.modules.application.dev_tools.db_test_data import (
     InsertTestData)


def insert_test_data():
    insert = InsertTestData(db=db)
    insert.start_insertion()
