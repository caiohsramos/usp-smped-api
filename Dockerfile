FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV LISTEN_PORT 3001

EXPOSE 3001

COPY ./app /app
COPY requirements.txt . 

RUN pip install -r requirements.txt