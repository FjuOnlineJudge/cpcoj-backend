# oj

## Member

* roy4801
* ICEJJ
* SunTalk
* halloworld

## Installation

```
$ sudo apt update && sudo apt upgrade && sudo apt install -y gcc g++ build-essential python3 python3-pip mysql-server libmysqlclient-dev libcap-dev
$ pip3 install -r requirement.txt
$ git clone https://github.com/roy4801/hoj-isolate.git
$ cd isolate
$ make isolate
$ sudo make install
```

## Setting

`config.py` setting databases connection


* sql -> `create database oj_0 CHARSET=utf8mb4;`
	  -> `SET GLOBAL sql_mode = '';`


## Build table

```
./rebuild_db.sh
```

