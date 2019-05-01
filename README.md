# oj

## Member

* roy4801
* ICEJJ
* SunTalk
* halloworld

## Installation

```
$ sudo apt update && sudo apt upgrade && sudo apt install -y gcc g++ build-essential python3 python3-pip mysql-server libmysqlclient-dev libcap-dev
$ pip3 install flask Flask-MySQLdb flask-sqlalchemy sqlalchemy
$ pip3 install flask-script flask-migrate functools
$ pip3 install flask-login flask_bootstrap werkzeug flask_wtf wtforms
```

## Setting

`config.py` setting databases connection

* sql -> `create database oj_0 CHARSET=utf8mb4;`


## Build table

```
./rebuild_db.sh
```

