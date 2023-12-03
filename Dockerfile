FROM python:3.10-slim

LABEL maintainer=i@xiaojin233.cn

COPY poetry.lock /tmp/poetry.lock
COPY pyproject.toml /tmp/pyproject.toml

RUN cd /tmp && \
    pip config set global.index-url https://mirror.sjtu.edu.cn/pypi/web/simple && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction

WORKDIR /app
CMD python3 main.py