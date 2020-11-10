#!/usr/bin/env python3

import csv
import os


def get_location():
    location = os.path.realpath(
        os.path.join(
            os.getcwd(),
            os.path.dirname(__file__)
        )
    )
    return location


def load_csv(filename):
    columns = []
    with open(filename, 'r') as f:
        dr = csv.DictReader(f)
        if not columns:
            columns = dr.fieldnames
        to_db = []
        for r in dr:
            db_row = []
            for col in columns:
                db_row.append(r[col])
            to_db.append(db_row)
    return columns, to_db


def insert_db_query(columns):
    query = 'INSERT INTO data (\n'
    query += ",\n".join(columns)
    query += ') VALUES ('
    query += ",".join(['?'] * len(columns))
    query += ');'
    return query
