# !/usr/bin/python
# -*-coding:utf-8-*-
import pymysql
from dbutils.pooled_db import PooledDB

config = {
    "host": "xxxx",
    "port": 3306,
    "user": "xxxxx",
    "passwd": "xxxxx",
    "db": "xxxxxx",
    "maxconnections": 10,
    "cursorclass": pymysql.cursors.DictCursor

}
pool = PooledDB(pymysql, **config)


def get_connection():
    try:
        return pool.connection()
    except ConnectionError:
        return None


def close(conn, cursor):
    cursor.close()
    conn.close()
