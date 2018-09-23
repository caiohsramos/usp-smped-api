FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV LISTEN_PORT 3001

EXPOSE 3001

COPY ./app /app

RUN pip install -r /app/requirements.txt