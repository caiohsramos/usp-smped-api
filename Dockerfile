FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV LISTEN_PORT 5000

EXPOSE 5000

COPY ./app /app

RUN pip install -r /app/requirements.txt