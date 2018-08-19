FROM python:3.6-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /usr/local/benedict
COPY . /usr/local/benedict
WORKDIR /usr/local/benedict

ENV FLASK_ENV Production
ENV REDIS_URL redis://redis_server:6379/0

EXPOSE 5000
CMD ["./run.sh"]