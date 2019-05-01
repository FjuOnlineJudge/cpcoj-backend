#! /bin/sh
mysql -u root -proot << EOFMYSQL
use oj_0;
show tables;
EOFMYSQL