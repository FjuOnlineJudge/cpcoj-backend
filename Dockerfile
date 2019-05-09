FROM ubuntu:18.04

RUN apt update && apt upgrade -y

RUN apt install -y gcc g++ build-essential python3 python3-pip mysql-server libmysqlclient-dev libcap-dev git

RUN useradd -U -m -s /bin/bash oj

WORKDIR /home/oj

# Pull the oj repo
RUN git clone https://github.com/rishteam/oj.git
RUN cd oj

WORKDIR oj

RUN git checkout deploy
RUN git pull

RUN ls -al
RUN pip3 install -r requirement.txt

CMD ["python3", "app.py"]