#!/bin/sh
mysql -u root -proot << EOFMYSQL
use oj_0;
drop table account;
drop table account_valid;
drop table alembic_version;
drop table problem;
drop table submission;
EOFMYSQL