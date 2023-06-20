FROM python:3.10-slim

LABEL maintainer=i@xiaojin233.cn

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR /app
CMD python3 main.py