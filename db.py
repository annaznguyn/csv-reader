import csv
import sqlite3
import time


def get_connection():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    return conn, cursor

def close_connection(conn, cursor):
    cursor.close()
    conn.close()

def create_table():
    conn, cursor = get_connection()

    query = """
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            city TEXT,
            company TEXT
        )
        """
    cursor.execute(query)
    conn.commit()
    close_connection(conn, cursor)

def delete_table():
    conn, cursor = get_connection()
    cursor.execute("DROP TABLE IF EXISTS data")
    conn.commit()
    close_connection(conn, cursor)

def import_csv():
    conn, cursor = get_connection()

    batch_size = 50_000

    total_imported = 0

    INSERT_SQL = """
        INSERT INTO data (name, email, phone, city, company)
        VALUES (?, ?, ?, ?, ?)
    """

    with open("data.csv", "r") as f:
        reader = csv.reader(f)
        next(reader, None)

        batch = []
        started = time.perf_counter()

        for row in reader:
            cleaned_row = []

            for value in row:
                value = value.strip()
                if value == "":
                    value = None
                cleaned_row.append(value)

            batch.append(tuple(cleaned_row))

            if len(batch) >= batch_size:
                cursor.executemany(INSERT_SQL, batch)

                total_imported += len(batch)
                batch = []

        if batch:
            cursor.executemany(INSERT_SQL, batch)

    conn.commit()
    close_connection(conn, cursor)

    total_time = time.perf_counter() - started
    rows_per_second = total_imported / total_time

    print(f"Successfully imported {rows_per_second:,.0f} rows/s")

    return {"rows_per_second": rows_per_second}

def select_top_rows():
    conn, cursor = get_connection()

    cursor.execute(
        """
        SELECT id, name, email, phone, city, company
        FROM data
        LIMIT 10
        """
    )

    columns = ["id", "name", "email", "phone", "city", "company"]

    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    close_connection(conn, cursor)

    return rows

if __name__ == "__main__":
    print(select_top_rows())
