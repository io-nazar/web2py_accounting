from applications.accounting.modules.application.dev_tools import (
     InsertTestData)


def insert_test_data():
    insert = InsertTestData(db=db)
    insert.start_insertion()
