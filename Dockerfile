FROM python:3.6
WORKDIR /app
RUN pip install eve flask-sentinel
RUN pip install flask-pymongo==0.5.2

EXPOSE 5000