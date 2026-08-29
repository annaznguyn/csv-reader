from fastapi import FastAPI

from db import create_table, delete_table, import_csv

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
@app.post("/display")
async def display(content):
    return content
    # json = {}
    # headers = DATA[0]

    # for i in range(1, len(DATA)):
    #     temp = {}
    #     for j in range(len(DATA[i])):
    #         temp[headers[j]] = DATA[i][j]

    #     json[i] = temp
    
    # return json
