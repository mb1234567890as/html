FROM python:3.11.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY reg.txt .

RUN pip install --upgrade pip

RUN pip install -r reg.txt 

COPY  . .