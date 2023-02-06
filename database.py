# -*- coding: utf-8 -*-
"""
Created on Sun May  1 13:21:11 2022.

@author: Marcin Orzech
"""

import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd


load_dotenv()
# connection = psycopg2.connect(os.environ["DATABASE_URL"])

DATA_TABLE = "SELECT * FROM data ORDER BY id;"
PARAMETERS_TABLE = "SELECT * FROM parameters;"
INSERT_EMAIL = "INSERT INTO emails (cell_id, email) VALUES ((SELECT MAX(id) from data), %s)"
RESET_SEQUENCE = "SELECT setval('data_id_seq', (SELECT MAX(id) from data));"


def get_table(table):
    connection = psycopg2.connect(os.environ["DATABASE_URL"])
    try:
        if table == 'data':
            return pd.read_sql(DATA_TABLE, connection, index_col='id')
        elif table == 'parameters':
            return pd.read_sql(PARAMETERS_TABLE, connection, index_col=None)
    finally:
        connection.close()


def upload_row(cols, values):
    vals_str = ','.join(['%s' for i in range(len(values))])
    UPLOAD_DATA = f"INSERT INTO data ({cols}) VALUES ({vals_str});"
    connection = psycopg2.connect(os.environ["DATABASE_URL"])
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(RESET_SEQUENCE)
                cursor.execute(UPLOAD_DATA, values)
    finally:
        connection.close()


def save_email(address):
    connection = psycopg2.connect(os.environ["DATABASE_URL"])
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_EMAIL, (address,))
    finally:
        connection.close()
