FROM python:3.12-rc-slim-buster 
WORKDIR /

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/

COPY poetry.lock pyproject.toml ./ 

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root 