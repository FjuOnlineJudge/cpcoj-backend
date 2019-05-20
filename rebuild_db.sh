#!/bin/sh
mysql -u root -proot << EOFMYSQL
drop database oj_0;
create database oj_0;
EOFMYSQL