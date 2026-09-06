from fastapi import FastAPI, Query

from db import create_table, delete_table, import_csv, select_page

app = FastAPI()


# import csv file to SQLite database (no need to create table, just insert data)
# - 5 fields (fake data generator for testing)
# - 10mil rows
# print number of rows imported/second (total of rows/time taken)

# cases:
#  - empty cell -> store as NULL
@app.post("/import")
def read_csv():
    delete_table()
    create_table()
    return import_csv()

# handle pagination
# - 100 rows per page
@app.get("/display")
def display(page: int = Query(1, ge=1)):
    return select_page(page)
