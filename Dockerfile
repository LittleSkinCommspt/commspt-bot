FROM python:latest

LABEL maintainer=me@xiaojin233.cn

RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/ && \
    pip config set install.trusted-host mirrors.cloud.tencent.com && \
    pip install graia-application-mirai

WORKDIR /app
CMD python3 main.py