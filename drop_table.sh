#!/bin/sh
mysql -u root -proot << EOFMYSQL
use oj_0;
drop table account;
drop table problem;
drop table submission;
drop table alembic_version;
EOFMYSQL