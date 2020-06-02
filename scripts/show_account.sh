#! /bin/sh
mysql -u root -proot << EOFMYSQL
use oj_0;
SELECT * FROM account;
EOFMYSQL