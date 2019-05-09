FROM ubuntu:18.04

RUN apt update && apt upgrade

RUN apt install -y gcc g++ build-essential python3 python3-pip mysql-server libmysqlclient-dev libcap-dev

# COPY requirement.txt 



