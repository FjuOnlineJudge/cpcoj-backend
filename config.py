import os

DEBUG = True
SESSION_PROTECTION = 'strong'
# SECRET_KEY = os.urandom(24)
SECRET_KEY = 'aaa'
# WTF_CSRF_SECRET_KEY = os.urandom(24)
# CSRF_SESSION_KEY = os.urandom(24)

DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'test'
PASSWORD = 'test'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'oj_0'

DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
