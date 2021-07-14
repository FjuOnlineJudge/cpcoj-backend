import os

DEBUG = True
SESSION_PROTECTION = 'strong'
# SECRET_KEY = os.urandom(24)
SECRET_KEY = 'aaa'
# WTF_CSRF_SECRET_KEY = os.urandom(24)
# CSRF_SESSION_KEY = os.urandom(24)

DIALECT  = os.environ.get('DIALECT') or 'mysql'
DRIVER   = os.environ.get('DRIVER') or 'mysqldb'
USERNAME = os.environ.get('USERNAME') or 'root'
PASSWORD = os.environ.get('PASSWORD') or 'root'
HOST     = os.environ.get('HOST') or '127.0.0.1'
PORT     = os.environ.get('PORT') or '3306'
DATABASE = os.environ.get('DATABASE') or 'oj_0'

DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
