FROM python:latest

LABEL maintainer=i@xiaojin233.cn

COPY requirements.txt /tmp/requirements.txt

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set install.trusted-host mirrors.aliyun.com

RUN pip install -r /tmp/requirements.txt

WORKDIR /app
CMD python3 main.py