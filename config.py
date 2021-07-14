import os

DEBUG = True
SESSION_PROTECTION = 'strong'
# SECRET_KEY = os.urandom(24)
SECRET_KEY = 'aaa'
# WTF_CSRF_SECRET_KEY = os.urandom(24)
# CSRF_SESSION_KEY = os.urandom(24)

DIALECT  = os.environ['DIALECT'] or 'mysql'
DRIVER   = os.environ['DRIVER'] or 'mysqldb'
USERNAME = os.environ['USERNAME'] or 'test'
PASSWORD = os.environ['PASSWORD'] or 'test'
HOST     = os.environ['HOST'] or '127.0.0.1'
PORT     = os.environ['PORT'] or '3306'
DATABASE = os.environ['DATABASE'] or 'oj_0'

DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
